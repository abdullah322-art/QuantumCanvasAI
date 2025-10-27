from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models.registry import get_model_spec


router = APIRouter(prefix="/v1", tags=["plans"])


@router.get("/access")
def access(model_id: str, plan: str = "free"):
    spec = get_model_spec(model_id)
    tier_order = {"free": 0, "pro": 1, "enterprise": 2}
    if tier_order.get(plan, 0) < tier_order[spec.model_info.pricing_tier]:
        raise HTTPException(status_code=402, detail=f"Plan '{plan}' cannot access {model_id}")
    return {"allowed": True, "model": spec.model_info.id}

