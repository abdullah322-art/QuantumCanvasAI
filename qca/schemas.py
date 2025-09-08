from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    id: str
    family: str = "qca"
    version: str
    display_name: str
    description: str
    context_window: int
    max_output_tokens: int
    pricing_tier: Literal["free", "pro", "enterprise"]


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="QCA model id, e.g., qca-4.9 or qca-6.8-supereme")
    messages: List[ChatMessage]
    temperature: float = 0.2
    top_p: float = 0.95
    max_tokens: int = 2048
    stream: bool = False
    user: Optional[str] = None
    session_id: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[str] = None
    system_prompt: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter"]


class ChatCompletionResponse(BaseModel):
    id: str
    model: str
    object: Literal["chat.completion"] = "chat.completion"
    choices: List[ChatCompletionResponseChoice]
    usage: Dict[str, int]


class StreamChunk(BaseModel):
    id: str
    model: str
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    delta: ChatMessage
    index: int = 0
    done: bool = False

