<<<<<<< HEAD
from fastapi import APIRouter, UploadFile, HTTPException
from typing import List, Dict, Any
import uuid
from datetime import datetime

from ..app.core.llm_adapter import LLMAdapter
from ..app.core.ocr import OCRProcessor
from ..app.services.vague_detector import VagueTermsDetector
from ..app.services.rag_store import rag_store
from ..app.services.gemini_judge import gemini_judge
from ..models.schemas import ReviewResult, Issue, IssueType, Severity, UploadResponse, AnalysisResult, AnalysisProgress
=======
"""
Router for contract-related endpoints.
"""
import os
import uuid
from typing import Dict, Any, Optional
import tempfile
from datetime import datetime
>>>>>>> adf109136d992a65760cbd36af2e98e5ef674ae2

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

<<<<<<< HEAD
# Initialize services
llm_adapter = LLMAdapter()
ocr_processor = OCRProcessor()
vague_detector = VagueTermsDetector()
=======
from backend.models.schemas import UploadResponse, AnalysisResponse
# from backend.app.core.ocr import OCRProcessor, ocr_available # OCR DISABLED
from backend.app.core.llm_adapter import analyze_contract_with_llm

router = APIRouter(prefix="/api", tags=["contracts"])

# Simple in-memory storage for uploaded documents
# In a real app, this would be replaced with a database
# Format: {doc_id: {"filename": str, "path": str, "size": int}}
UPLOADED_DOCUMENTS: Dict[str, Dict[str, Any]] = {}

# Create a temp directory for uploads
UPLOAD_DIR = tempfile.mkdtemp(prefix="blackletter_uploads_")
>>>>>>> adf109136d992a65760cbd36af2e98e5ef674ae2

# In-memory storage for upload tracking (use database in production)
upload_storage = {}
analysis_storage = {}

<<<<<<< HEAD
@router.post("/review", response_model=ReviewResult)
async def review_contract(file: UploadFile):
    """Review contract for vague terms and compliance issues."""
    
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files supported")
        
        # Read file content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Extract text using OCR
        extracted_text = await ocr_processor.extract_text(content)
        
        # Store in RAG store
        rag_store.store_document(doc_id, extracted_text, {
            "filename": file.filename,
            "size": len(content),
            "upload_time": datetime.utcnow().isoformat()
        })
        
        # Find vague terms
        vague_hits = vague_detector.find_vague_spans(extracted_text)
        
        # Process each vague term with LLM judgment
        findings = []
        for hit in vague_hits:
            # Get context around the vague term
            context = rag_store.get_context_around_position(
                doc_id, hit["start"], window_size=1200
            )
            
            # Create citations
            citations = [{
                "doc_id": file.filename,
                "page": context["page"],
                "start": hit["start"],
                "end": hit["end"]
            }]
            
            # Get LLM judgment
            judgment = await gemini_judge.judge_vague_term(hit, context["context"], citations)
            
            # Convert to Issue format
            issue = Issue(
                id=str(uuid.uuid4()),
                type=IssueType.OTHER,  # Could map categories to specific types
                title=f"Vague {hit['category']} term: {hit['text']}",
                description=judgment["rationale"],
                severity=self._map_risk_to_severity(judgment["risk"]),
                clause=f"Page {context['page']}",
                page_number=context["page"],
                remediation="\n".join(judgment["improvements"]),
                timestamp=datetime.utcnow()
            )
            
            findings.append({
                "issue": issue,
                "vague_term": hit,
                "judgment": judgment,
                "context": context,
                "citations": citations
            })
        
        # Convert findings to issues
        issues = [finding["issue"] for finding in findings]
        
        return ReviewResult(
            filename=file.filename,
            size=len(content),
            issues=issues,
            metadata={
                "doc_id": doc_id,
                "vague_terms_found": len(vague_hits),
                "findings": findings
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")

def _map_risk_to_severity(risk: str) -> Severity:
    """Map LLM risk levels to severity enum."""
    mapping = {
        "low": Severity.LOW,
        "medium": Severity.MEDIUM,
        "high": Severity.HIGH
    }
    return mapping.get(risk, Severity.MEDIUM)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile):
    """Upload a document for later analysis."""
    
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files supported")
        
        # Read file content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Store upload info
        upload_info = {
            "doc_id": doc_id,
            "filename": file.filename,
            "size": len(content),
            "content": content,
            "upload_time": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }
        upload_storage[doc_id] = upload_info
        
        return UploadResponse(
            doc_id=doc_id,
            filename=file.filename,
            size=len(content),
            upload_time=upload_info["upload_time"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/analyze/{doc_id}", response_model=AnalysisResult)
async def analyze_document(doc_id: str):
    """Analyze a previously uploaded document."""
    
    try:
        # Check if document exists
        if doc_id not in upload_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        upload_info = upload_storage[doc_id]
        content = upload_info["content"]
        
        # Extract text using OCR
        extracted_text = await ocr_processor.extract_text(content)
        
        # Store in RAG store
        rag_store.store_document(doc_id, extracted_text, {
            "filename": upload_info["filename"],
            "size": upload_info["size"],
            "upload_time": upload_info["upload_time"]
        })
        
        # Find vague terms
        vague_hits = vague_detector.find_vague_spans(extracted_text)
        
        # Process each vague term with LLM judgment
        findings = []
        issues = []
        
        for hit in vague_hits:
            # Get context around the vague term
            context = rag_store.get_context_around_position(
                doc_id, hit["start"], window_size=1200
            )
            
            # Create citations
            citations = [{
                "doc_id": upload_info["filename"],
                "page": context["page"],
                "start": hit["start"],
                "end": hit["end"]
            }]
            
            # Get LLM judgment
            judgment = await gemini_judge.judge_vague_term(hit, context["context"], citations)
            
            # Convert to Issue format
            issue = Issue(
                id=str(uuid.uuid4()),
                docId=doc_id,
                docName=upload_info["filename"],
                type=IssueType.OTHER,  # Could map categories to specific types
                clausePath=f"Page {context['page']}",
                citation="Vague Terms Analysis",
                severity=_map_risk_to_severity(judgment["risk"]),
                confidence=0.85,
                status="Open",
                snippet=hit['text'],
                recommendation="\n".join(judgment["improvements"]),
                createdAt=datetime.utcnow().isoformat()
            )
            
            issues.append(issue)
            findings.append({
                "issue": issue,
                "vague_term": hit,
                "judgment": judgment,
                "context": context,
                "citations": citations
            })
        
        # Generate summary and risks
        summary = f"Analyzed {upload_info['filename']} and found {len(vague_hits)} vague terms requiring attention."
        risks = [f"Vague {hit['category']} term: {hit['text']}" for hit in vague_hits[:5]]  # Top 5 risks
        
        # Store analysis results
        analysis_result = AnalysisResult(
            doc_id=doc_id,
            filename=upload_info["filename"],
            issues=issues,
            summary=summary,
            risks=risks,
            metadata={
                "vague_terms_found": len(vague_hits),
                "findings": findings
            }
        )
        
        analysis_storage[doc_id] = analysis_result
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/analyze/{doc_id}/status", response_model=AnalysisProgress)
async def get_analysis_status(doc_id: str):
    """Get the status of document analysis."""
    
    if doc_id not in upload_storage:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if doc_id in analysis_storage:
        return AnalysisProgress(
            doc_id=doc_id,
            status="completed",
            progress=1.0,
            message="Analysis completed successfully"
        )
    else:
        return AnalysisProgress(
            doc_id=doc_id,
            status="pending",
            progress=0.0,
            message="Analysis not started"
        )

@router.get("/contracts/{doc_id}/findings")
async def get_findings(doc_id: str):
    """Get detailed findings for a specific document."""
    if doc_id in analysis_storage:
        return analysis_storage[doc_id]
    return {"doc_id": doc_id, "findings": []}
=======
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
        content = await file.read()
        file_size = len(content)
        
        # Generate a unique ID for this document
        doc_id = str(uuid.uuid4())
        
        # Save the file to a temporary location
        safe_filename = file.filename or "unknown.pdf"
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{safe_filename}")
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Store metadata in our simple "database"
        UPLOADED_DOCUMENTS[doc_id] = {
            "filename": safe_filename,
            "path": file_path,
            "size": file_size,
            "upload_time": datetime.utcnow().isoformat()
        }
        
        return UploadResponse(
            filename=safe_filename,
            size=file_size,
            doc_id=doc_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/analyze/{doc_id}", response_model=AnalysisResponse)
async def analyze_contract(doc_id: str):
    """
    Analyze a previously uploaded contract by its document ID.
    
    Args:
        doc_id: The document ID from the upload response
        
    Returns:
        AnalysisResponse containing filename, size, and list of issues
    """
    # Check if document exists
    if doc_id not in UPLOADED_DOCUMENTS:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        doc_info = UPLOADED_DOCUMENTS[doc_id]
        filename = doc_info["filename"]
        file_size = doc_info["size"]
        file_path = doc_info["path"]
        
        # Read the file content
        with open(file_path, "rb") as f:
            content = f.read()
        
        # Perform simulated OCR to extract text -- DISABLED
        # if not ocr_available():
        #     raise HTTPException(status_code=501, detail="OCR functionality is not enabled or dependencies are missing.")
        # ocr_processor = OCRProcessor()
        # extracted_text = await ocr_processor.extract_text(content)
        extracted_text = "OCR is currently disabled. Using placeholder text."
        
        # Perform simulated LLM analysis
        issues = analyze_contract_with_llm(extracted_text, filename)
        
        return AnalysisResponse(
            filename=filename,
            size=file_size,
            issues=issues
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing contract: {str(e)}")
>>>>>>> adf109136d992a65760cbd36af2e98e5ef674ae2
