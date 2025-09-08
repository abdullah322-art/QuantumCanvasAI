import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title=os.getenv("PRODUCT_NAME", "QCA"))

origins = os.getenv("ALLOWED_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.split(",") if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import health, models, chat, auth, billing, tts  # noqa: E402

app.include_router(health.router)
app.include_router(models.router, prefix="/v1")
app.include_router(chat.router, prefix="/v1")
app.include_router(auth.router, prefix="/auth")
app.include_router(billing.router, prefix="/billing")
app.include_router(tts.router, prefix="/v1")

