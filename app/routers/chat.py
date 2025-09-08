from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..models.registry import get_engine, list_models

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = Field(default_factory=lambda: list_models()[0])
    messages: List[Message]
    max_tokens: int | None = None
    memory_window: int = 12  # keep last N messages
    forget_earliest: bool = True  # if True, drop earliest messages first
    system_prompt: str | None = None

class ChatResponse(BaseModel):
    model: str
    message: Message

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if req.model not in list_models():
        raise HTTPException(status_code=400, detail="Unknown model")

    msgs: List[Dict[str, Any]] = [m.model_dump() for m in req.messages]

    if req.forget_earliest and len(msgs) > req.memory_window:
        msgs = msgs[-req.memory_window:]

    engine = get_engine(req.model)
    out = engine.generate(messages=msgs, system_prompt=req.system_prompt)
    return ChatResponse(model=req.model, message=Message(**out))
