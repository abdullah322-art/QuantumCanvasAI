from __future__ import annotations

from fastapi import APIRouter

from ..models.registry import list_models
from ..schemas import ModelInfo


router = APIRouter(prefix="", tags=["public"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/v1/models", response_model=list[ModelInfo])
def models():
    return list_models()

