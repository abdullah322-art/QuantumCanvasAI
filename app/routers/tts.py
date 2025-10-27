import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: str | None = None

@router.post("/tts")
def tts(req: TTSRequest):
    if os.getenv("ENABLE_TTS", "true").lower() != "true":
        return {"status": "disabled"}
    # Stub: return a faux url and base64 payload placeholder
    return {
        "status": "ok",
        "voice": req.voice or "default",
        "audio": "data:audio/wav;base64,",
    }
