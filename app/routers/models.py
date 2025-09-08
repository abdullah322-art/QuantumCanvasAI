from fastapi import APIRouter
from ..models.registry import list_models

router = APIRouter()

@router.get("/models")
def models():
    return {"data": [{"id": m} for m in list_models()]}
