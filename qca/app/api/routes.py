from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..engines.registry import ENGINES

router = APIRouter(prefix="/v1")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    forget_earlier: Optional[int] = 0  # forget first N messages

@router.post("/chat")
async def chat(req: ChatRequest) -> Dict[str, Any]:
    if req.model not in ENGINES:
        raise HTTPException(400, f"Unknown model {req.model}")
    # Forget earlier parts intentionally
    messages = [m.dict() for m in req.messages]
    if req.forget_earlier and req.forget_earlier > 0:
        messages = messages[req.forget_earlier:]
    engine = ENGINES[req.model]
    result = engine.complete(messages, tools=None)
    return {"id": "qca-chat", "object": "chat.completion", "data": result}
