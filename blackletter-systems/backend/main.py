from fastapi import FastAPI, UploadFile, File, HTTPException
import datetime
import os
import uuid
import tempfile
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Blackletter API", 
              description="API for contract analysis and compliance checking",
              version="0.1.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class IssueType(str, Enum):
    DATA_PROTECTION = "data_protection"
    CONSUMER_RIGHTS = "consumer_rights"
    EMPLOYMENT = "employment"
    GDPR = "gdpr"
    IP_RIGHTS = "ip_rights"
    ANTI_MONEY_LAUNDERING = "anti_money_laundering"
    COMPETITION_LAW = "competition_law"
    ENVIRONMENTAL = "environmental"
    TAX = "tax"
    OTHER = "other"

class Severity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Issue(BaseModel):
    id: str
    type: IssueType
    title: str
    description: str
    severity: Severity
    clause: Optional[str] = None
    page_number: Optional[int] = None
    remediation: Optional[str] = None
    timestamp: datetime

class AnalysisResponse(BaseModel):
    filename: str
    size: int
    issues: List[Issue]

# Simulated OCR function
def perform_ocr(file_bytes: bytes, filename: Optional[str] = None) -> str:
    basic_text = (
        "EMPLOYMENT CONTRACT\n\n"
        "THIS EMPLOYMENT AGREEMENT (the 'Agreement') is made and entered into on [DATE], "
        "by and between [COMPANY NAME], a corporation organized and existing under the laws "
        "of [JURISDICTION] ('Employer'), and [EMPLOYEE NAME] ('Employee').\n\n"
        
        "WHEREAS, Employer desires to employ Employee on the terms and conditions set forth "
        "herein; and WHEREAS, Employee desires to be employed by Employer on such terms and conditions.\n\n"
        
        "1. POSITION AND DUTIES\n\n"
        "Employee shall be employed as [POSITION TITLE] and shall perform such duties as are "
        "assigned by Employer and are consistent with such position.\n\n"
        
        "2. TERM\n\n"
        "The term of employment shall commence on [START DATE] and shall continue until "
        "terminated in accordance with the provisions of this Agreement.\n\n"
        
        "3. COMPENSATION\n\n"
        "Employer shall pay Employee a base salary of [AMOUNT] per [PERIOD], subject to "
        "applicable withholding taxes and other deductions.\n\n"
        
        "4. BENEFITS\n\n"
        "Employee shall be entitled to participate in benefit programs provided by Employer "
        "to its employees, subject to the terms and conditions of such programs.\n\n"
        
        "5. CONFIDENTIAL INFORMATION\n\n"
        "Employee acknowledges that the Confidential Information of Employer is valuable, "
        "and therefore agrees not to disclose such Confidential Information to anyone outside "
        "of Employer during or after employment.\n\n"
        
        "6. DATA PROTECTION\n\n"
        "Employer will process Employee's personal data for administrative purposes "
        "and to comply with employment and legal requirements. Employee consents to the collection, "
        "storage, processing, and transfer of personal data as described in this Agreement.\n\n"
        
        "7. TERMINATION\n\n"
        "Employment may be terminated by either party with [NOTICE PERIOD] notice in writing. "
        "Employer reserves the right to pay Employee in lieu of notice.\n\n"
        
        "8. GOVERNING LAW\n\n"
        "This Agreement shall be governed by and construed in accordance with the laws of [JURISDICTION].\n\n"
        
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.\n\n"
    )
    
    # If this is an NDA or privacy related document, inject GDPR-specific content
    if filename and ("nda" in filename.lower() or "privacy" in filename.lower()):
        return basic_text + "\n\n9. GDPR COMPLIANCE\n\nThe parties agree to comply with the General Data Protection Regulation (GDPR) and any applicable data protection laws. Each party shall implement appropriate technical and organizational measures to protect personal data."
    
    # If this looks like a lease or property contract
    if filename and ("lease" in filename.lower() or "property" in filename.lower()):
        return basic_text.replace("EMPLOYMENT CONTRACT", "COMMERCIAL LEASE AGREEMENT").replace(
            "Employee", "Tenant").replace("Employer", "Landlord") + "\n\n9. ENVIRONMENTAL COMPLIANCE\n\nTenant shall comply with all applicable environmental regulations and laws."
    
    # For a regular employment contract
    return basic_text

# Simulated LLM analysis function
def analyze_contract_with_llm(contract_text: str, filename: Optional[str] = None) -> List[Issue]:
    issues = []
    now = datetime.utcnow()
    
    # Check for common contract issues
    if "CONFIDENTIAL INFORMATION" in contract_text or "confidential" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.IP_RIGHTS,
            title="Incomplete Confidentiality Clause",
            description="The confidentiality clause lacks specific remedies for breach.",
            severity=Severity.MEDIUM,
            clause="Section 5",
            page_number=1,
            remediation="Add specific remedies and liquidated damages for confidentiality breaches.",
            timestamp=now
        ))
    
    if "DATA PROTECTION" in contract_text or "data" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.DATA_PROTECTION,
            title="Vague Data Protection Terms",
            description="Data protection provisions lack specificity on data types and processing purposes.",
            severity=Severity.HIGH,
            clause="Section 6",
            page_number=1,
            remediation="Specify data types, processing purposes, and retention periods explicitly.",
            timestamp=now
        ))
    
    if "GDPR" in contract_text or "gdpr" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.GDPR,
            title="Missing Data Subject Rights",
            description="The contract doesn't address data subject rights under GDPR Article 15-22.",
            severity=Severity.HIGH,
            clause="Section 9",
            page_number=2,
            remediation="Add provisions for data subject access, rectification, erasure, and portability rights.",
            timestamp=now
        ))
    
    if "TERMINATION" in contract_text or "terminat" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.EMPLOYMENT,
            title="Inadequate Notice Period",
            description="The termination notice period may not comply with local employment regulations.",
            severity=Severity.MEDIUM,
            clause="Section 7",
            page_number=1,
            remediation="Review and align termination notice period with local employment laws.",
            timestamp=now
        ))
    
    # Always add at least one random issue
    if not issues:
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.EMPLOYMENT,
            title="Working Hours Not Specified",
            description="The contract does not clearly define working hours or overtime policy.",
            severity=Severity.MEDIUM,
            clause="Section 2",
            page_number=1,
            remediation="Add specific working hours, days, and overtime compensation policy.",
            timestamp=now
        ))
    
    return issues

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint providing a simple service message."""
    return {"message": "Blackletter API running"}

@app.get("/health")
def health():
    return {"ok": True, "service": "blackletter", "ts": datetime.utcnow().isoformat()}

@app.post("/api/review", response_model=AnalysisResponse)
async def review_contract(file: UploadFile = File(...)):
    """
    Combined endpoint for upload and analyze in one step.
    """
    try:
        content = await file.read()
        file_size = len(content)
        safe_filename = file.filename or "unknown.pdf"
        
        # Perform simulated OCR to extract text
        extracted_text = perform_ocr(content, safe_filename)
        
        # Perform simulated LLM analysis
        issues = analyze_contract_with_llm(extracted_text, safe_filename)
        
        return AnalysisResponse(
            filename=safe_filename,
            size=file_size,
            issues=issues
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")
