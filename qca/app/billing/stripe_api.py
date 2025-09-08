import stripe
from fastapi import APIRouter
from ..config import settings

router = APIRouter(prefix="/billing")

@router.get("/config")
async def config():
    return {
        "publishable_key": settings.stripe_publishable_key,
        "ksa95_promo": {"code": "KSA95", "discount_pct": 35},
    }

@router.on_event("startup")
async def setup_stripe():
    if settings.stripe_secret_key:
        stripe.api_key = settings.stripe_secret_key
