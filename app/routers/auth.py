import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

router = APIRouter()

oauth = OAuth()

# Configure dynamically from env; if missing, routes will noop
if os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"):
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

if os.getenv("GITHUB_CLIENT_ID") and os.getenv("GITHUB_CLIENT_SECRET"):
    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "read:user user:email"},
    )

@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    if provider not in oauth:
        # Noop when not configured
        return {"status": "disabled", "provider": provider}
    redirect_uri = request.url_for("auth_callback", provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, str(redirect_uri))

@router.get("/callback/{provider}")
async def auth_callback(request: Request, provider: str):
    if provider not in oauth:
        return {"status": "disabled", "provider": provider}
    token = await oauth.create_client(provider).authorize_access_token(request)
    user = token.get("userinfo") or token
    return {"status": "ok", "provider": provider, "user": user}
