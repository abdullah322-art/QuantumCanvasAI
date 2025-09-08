# OAuth placeholders using env; real flows should be implemented on frontend
from fastapi import APIRouter
from ..config import settings

router = APIRouter(prefix="/auth")

@router.get("/providers")
async def providers():
    return {
        "google": {"client_id": settings.google_client_id},
        "github": {"client_id": settings.github_client_id},
    }
