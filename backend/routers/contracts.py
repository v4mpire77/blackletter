"""
Router for contract-related endpoints.
"""
import os
import uuid
import tempfile
from typing import Dict, Any
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException

# Import schemas with proper error handling
try:
    from ..models.schemas import UploadResponse
except ImportError:
    from backend.models.schemas import UploadResponse

# Import services with fallback for disabled features
try:
    from ..app.core.llm_adapter import LLMAdapter, analyze_contract_with_llm
    from ..app.core.ocr import OCRProcessor
    from ..app.services.vague_detector import VagueTermsDetector
    from ..app.services.rag_store import rag_store
    from ..app.services.gemini_judge import gemini_judge
    
    # Initialize services
    llm_adapter = LLMAdapter()
    ocr_processor = OCRProcessor()
    vague_detector = VagueTermsDetector()
    advanced_features_available = True
except ImportError:
    # Fallback for basic functionality
    from backend.app.core.llm_adapter import analyze_contract_with_llm
    advanced_features_available = False

router = APIRouter(prefix="/api", tags=["contracts"])

# Simple in-memory storage for uploaded documents
# In a real app, this would be replaced with a database
UPLOADED_DOCUMENTS: Dict[str, Dict[str, Any]] = {}
upload_storage = {}
analysis_storage = {}

# Create a temp directory for uploads
UPLOAD_DIR = tempfile.mkdtemp(prefix="blackletter_uploads_")

# In-memory storage for upload tracking (use database in production)
upload_storage = {}
analysis_storage = {}

def _map_risk_to_severity(risk: str) -> str:
    """Map LLM risk levels to severity."""
    mapping = {
        "low": "Low",
        "medium": "Medium", 
        "high": "High"
    }
    return mapping.get(risk.lower(), "Medium")

@router.post("/upload", response_model=UploadResponse)
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a contract file for later analysis.
    
    Args:
        file: The PDF contract file to upload
        
    Returns:
        UploadResponse containing filename, size, and document ID
    """
    try:
        # Validate file
        if file.filename and not file.filename.lower().endswith(('.pdf', '.txt', '.doc', '.docx')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, TXT, DOC, or DOCX files.")
        
        content = await file.read()
        file_size = len(content)
        
        # File size validation
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Generate a unique ID for this document
        doc_id = str(uuid.uuid4())
        safe_filename = file.filename or "unknown.pdf"
        
        # Store in both storage systems for compatibility
        upload_info = {
            "doc_id": doc_id,
            "filename": safe_filename,
            "size": file_size,
            "content": content,
            "upload_time": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }
        
        # Save to file system
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{safe_filename}")
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Store in both storage systems
        UPLOADED_DOCUMENTS[doc_id] = {
            "filename": safe_filename,
            "path": file_path,
            "size": file_size,
            "upload_time": upload_info["upload_time"]
        }
        upload_storage[doc_id] = upload_info
        
        return UploadResponse(
            filename=safe_filename,
            size=file_size,
            doc_id=doc_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.post("/analyze/{doc_id}")
async def analyze_contract(doc_id: str):
    """
    Analyze a previously uploaded contract by its document ID.
    
    Args:
        doc_id: The document ID from the upload response
        
    Returns:
        Analysis results with issues found
    """
    # Check if document exists
    if doc_id not in UPLOADED_DOCUMENTS and doc_id not in upload_storage:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Get document info from either storage system
        if doc_id in upload_storage:
            upload_info = upload_storage[doc_id]
            filename = upload_info["filename"]
            file_size = upload_info["size"]
            content = upload_info["content"]
        else:
            doc_info = UPLOADED_DOCUMENTS[doc_id]
            filename = doc_info["filename"]
            file_size = doc_info["size"]
            # Read the file content
            with open(doc_info["path"], "rb") as f:
                content = f.read()
        
        # Text extraction with fallback
        if advanced_features_available:
            try:
                extracted_text = await ocr_processor.extract_text(content)
                
                # Store in RAG store for advanced analysis
                rag_store.store_document(doc_id, extracted_text, {
                    "filename": filename,
                    "size": file_size,
                    "upload_time": datetime.utcnow().isoformat()
                })
                
                # Advanced vague terms analysis
                vague_hits = vague_detector.find_vague_spans(extracted_text)
                issues = []
                
                for hit in vague_hits:
                    # Get context around the vague term
                    context = rag_store.get_context_around_position(
                        doc_id, hit["start"], window_size=1200
                    )
                    
                    # Create citations
                    citations = [{
                        "doc_id": filename,
                        "page": context.get("page", 1),
                        "start": hit["start"],
                        "end": hit["end"]
                    }]
                    
                    # Get LLM judgment
                    judgment = await gemini_judge.judge_vague_term(hit, context.get("context", ""), citations)
                    
                    # Convert to Issue format
                    issue = {
                        "id": str(uuid.uuid4()),
                        "docId": doc_id,
                        "docName": filename,
                        "type": "Other",
                        "clausePath": f"Page {context.get('page', 1)}",
                        "citation": "Vague Terms Analysis",
                        "severity": _map_risk_to_severity(judgment.get("risk", "medium")),
                        "confidence": 0.85,
                        "status": "Open",
                        "snippet": hit['text'],
                        "recommendation": "\n".join(judgment.get("improvements", [])),
                        "createdAt": datetime.utcnow().isoformat()
                    }
                    issues.append(issue)
                
                summary = f"Analyzed {filename} and found {len(vague_hits)} vague terms requiring attention."
                risks = [f"Vague {hit['category']} term: {hit['text']}" for hit in vague_hits[:5]]
                
            except Exception as e:
                print(f"Advanced analysis failed, falling back to basic: {e}")
                extracted_text = "Advanced OCR failed. Using basic analysis."
                issues = analyze_contract_with_llm(extracted_text, filename)
                summary = f"Basic analysis completed for {filename}"
                risks = ["Advanced analysis unavailable"]
        else:
            # Basic analysis fallback
            extracted_text = "OCR is currently disabled. Using placeholder text."
            issues = analyze_contract_with_llm(extracted_text, filename)
            summary = f"Basic analysis completed for {filename}"
            risks = ["Advanced features unavailable"]
        
        # Store analysis results
        analysis_result = {
            "doc_id": doc_id,
            "filename": filename,
            "size": file_size,
            "issues": issues,
            "summary": summary,
            "risks": risks,
            "metadata": {
                "analysis_time": datetime.utcnow().isoformat(),
                "advanced_features": advanced_features_available
            }
        }
        
        analysis_storage[doc_id] = analysis_result
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing contract: {str(e)}")

@router.get("/analyze/{doc_id}/status")
async def get_analysis_status(doc_id: str):
    """Get the status of document analysis."""
    
    if doc_id not in upload_storage and doc_id not in UPLOADED_DOCUMENTS:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if doc_id in analysis_storage:
        return {
            "doc_id": doc_id,
            "status": "completed",
            "progress": 1.0,
            "message": "Analysis completed successfully"
        }
    else:
        return {
            "doc_id": doc_id,
            "status": "pending",
            "progress": 0.0,
            "message": "Analysis not started"
        }

@router.get("/contracts/{doc_id}/findings")
async def get_findings(doc_id: str):
    """Get detailed findings for a specific document."""
    if doc_id in analysis_storage:
        return analysis_storage[doc_id]
    return {"doc_id": doc_id, "findings": []}
