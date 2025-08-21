"""
Simple OCR simulator module for contract text extraction.
"""
from typing import Optional


def perform_ocr(file_bytes: bytes, filename: Optional[str] = None) -> str:
    """
    Simulate OCR text extraction from a PDF file.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        filename: Optional filename to influence simulation content
        
    Returns:
        Simulated extracted text from the document
    """
    # In a real implementation, we would use PyTesseract or another OCR library here
    # For simulation, we'll return different text based on keywords in the filename
    
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
        
        "[COMPANY NAME]\n\n"
        "By: ____________________\n"
        "Name: [REPRESENTATIVE NAME]\n"
        "Title: [REPRESENTATIVE TITLE]\n\n"
        
        "EMPLOYEE\n\n"
        "____________________\n"
        "[EMPLOYEE NAME]"
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
