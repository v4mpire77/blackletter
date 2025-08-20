from fastapi import FastAPI, UploadFile, File
import datetime

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "service": "blackletter", "ts": datetime.datetime.utcnow().isoformat()}

@app.post("/api/review")
async def review(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content), "analysis": "stub response"}
