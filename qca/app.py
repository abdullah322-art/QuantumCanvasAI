from __future__ import annotations

import json
import time
import uuid
from typing import AsyncGenerator

import orjson
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from .config import settings
from .memory import memory
from .schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    ModelInfo,
    StreamChunk,
)
from .models.registry import get_model_spec, list_models
from .engines import GeneralStubEngine, ProgrammingStubEngine
from .routers import public_router, auth_router, billing_router
from .routers.media import router as media_router
from .routers.plan_gating import router as plan_router


app = FastAPI(title="QCA Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_ENGINES = {
    "general": GeneralStubEngine(),
    "programming": ProgrammingStubEngine(),
}


# Routers
app.include_router(public_router)
app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(media_router)
app.include_router(plan_router)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}


@app.get("/v1/models", response_model=list[ModelInfo])
def get_models():
    return list_models()


def _run_engine(req: ChatCompletionRequest) -> tuple[str, str]:
    spec = get_model_spec(req.model)
    engine = _ENGINES.get(spec.engine)
    if engine is None:
        raise HTTPException(status_code=400, detail=f"Engine not available: {spec.engine}")

    messages = []
    if req.system_prompt:
        messages.append(ChatMessage(role="system", content=req.system_prompt))
    if req.session_id:
        messages.extend(memory.get(req.session_id))
    messages.extend(req.messages)

    text = engine.complete(messages, max_tokens=req.max_tokens, temperature=req.temperature)
    return text, spec.model_info.id


def _stream_engine(req: ChatCompletionRequest) -> AsyncGenerator[bytes, None]:
    spec = get_model_spec(req.model)
    engine = _ENGINES.get(spec.engine)
    if engine is None:
        raise HTTPException(status_code=400, detail=f"Engine not available: {spec.engine}")

    messages = []
    if req.system_prompt:
        messages.append(ChatMessage(role="system", content=req.system_prompt))
    if req.session_id:
        messages.extend(memory.get(req.session_id))
    messages.extend(req.messages)

    gen = engine.stream_complete(messages, max_tokens=req.max_tokens, temperature=req.temperature)
    completion_id = f"cmpl_{uuid.uuid4().hex[:12]}"

    async def iterator():
        idx = 0
        for token in gen:
            chunk = StreamChunk(
                id=completion_id,
                model=spec.model_info.id,
                delta=ChatMessage(role="assistant", content=token),
                index=idx,
                done=False,
            )
            idx += 1
            yield f"data: {orjson.dumps(chunk.model_dump()).decode()}\n\n".encode()
            time.sleep(0.01)
        final = StreamChunk(
            id=completion_id,
            model=spec.model_info.id,
            delta=ChatMessage(role="assistant", content=""),
            index=idx,
            done=True,
        )
        yield f"data: {orjson.dumps(final.model_dump()).decode()}\n\n".encode()

    return iterator()


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    if req.stream:
        return StreamingResponse(_stream_engine(req), media_type="text/event-stream")

    text, model_id = _run_engine(req)
    completion_id = f"cmpl_{uuid.uuid4().hex[:12]}"
    assistant_msg = ChatMessage(role="assistant", content=text)

    if req.session_id:
        for msg in req.messages:
            memory.append(req.session_id, msg)
        memory.append(req.session_id, assistant_msg)

    resp = ChatCompletionResponse(
        id=completion_id,
        model=model_id,
        choices=[
            ChatCompletionResponseChoice(index=0, message=assistant_msg, finish_reason="stop")
        ],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    )
    return JSONResponse(content=json.loads(orjson.dumps(resp.model_dump())))

