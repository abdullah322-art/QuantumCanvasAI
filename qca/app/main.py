from fastapi import FastAPI
from .api.routes import router as api_router
from .auth.oauth import router as oauth_router
from .billing.stripe_api import router as billing_router
from .config import settings

app = FastAPI(title=f"{settings.app_name} API")
app.include_router(api_router)
app.include_router(oauth_router)
app.include_router(billing_router)

@app.get("/")
async def root():
    return {"name": settings.app_name, "versions": settings.versions}
