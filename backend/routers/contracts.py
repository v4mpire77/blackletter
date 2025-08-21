"""
Router for contract-related endpoints.
"""
import os
import uuid
from typing import Dict, Any, Optional
import tempfile
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

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
