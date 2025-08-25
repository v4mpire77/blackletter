"""
Minimal FastAPI server for testing purposes.
This provides a simple API endpoint for testing the frontend-backend communication.
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json

# Import our simple analysis function
from utils import analyze_contract

app = FastAPI(title="Blackletter GDPR Processor (Test Server)")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Blackletter GDPR Processor Test Server"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/v1/compliance")
async def get_compliance_info():
    return {
        "articles": [
            {
                "id": "28-3-a",
                "title": "Article 28(3)(a)",
                "description": "Processing only on documented instructions",
                "category": "Processor Obligations"
            },
            {
                "id": "28-3-b",
                "title": "Article 28(3)(b)",
                "description": "Confidentiality obligation",
                "category": "Processor Obligations"
            }
        ]
    }

@app.post("/api/v1/analyze")
async def analyze_document(file: UploadFile = File(...)):
    # Read the file content
    content = await file.read()
    content_str = content.decode('utf-8')
    
    # Analyze the contract
    result = analyze_contract(content_str)
    
    return {
        "job_id": "test-job-123",
        "status": "completed",
        "results": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)