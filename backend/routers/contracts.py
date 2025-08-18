from fastapi import APIRouter, UploadFile, HTTPException
from pypdf import PdfReader
from io import BytesIO
import openai
from models.schemas import ReviewResult

router = APIRouter()

# LLM Prompt templates
SYSTEM_PROMPT = 'You are a UK legal assistant helping with quick, non-binding contract triage. Be concise.'
USER_PROMPT = '''Summarise this contract for a non-lawyer. Then list the top 3–5 risks with short reasoning. 
If text is incomplete, say so. Text: {text}'''

@router.post("/review", response_model=ReviewResult)
async def review_contract(file: UploadFile):
    # Validate file type
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    try:
        # Read file content
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
            
        # Extract text from PDF
        pdf = PdfReader(BytesIO(content))
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            
        # Truncate text to ~6000 chars
        text = text[:6000] + ("..." if len(text) > 6000 else "")
        
        # Call OpenAI for analysis
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT.format(text=text)}
            ]
        )
        
        # Parse response
        response = completion.choices[0].message.content
        
        # Split into summary and risks
        parts = response.split("\n\n")
        summary = parts[0]
        risks = [r.strip("- ") for r in parts[1:] if r.strip()]
        
        return ReviewResult(summary=summary, risks=risks)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
