import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "name": os.getenv("PRODUCT_NAME", "QCA"),
        "default_model": os.getenv("DEFAULT_MODEL", "QCA-4.9"),
        "versions": [
            "QCA-4.9","QCA-5.0","QCA-5.2","QCA-5.4","QCA-5.6",
            "QCA-5.8","QCA-6.0","QCA-6.2","QCA-6.5","QCA-6.8-SUPREME"
        ],
        "status": "ok"
    }
