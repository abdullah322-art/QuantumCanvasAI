from __future__ import annotations

import os
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import RedirectResponse

from ..config import settings


router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()

if settings.google_client_id and settings.google_client_secret:
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

if settings.github_client_id and settings.github_client_secret:
    oauth.register(
        name="github",
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "read:user user:email"},
    )


@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    if provider not in oauth:
        raise HTTPException(status_code=400, detail="Provider not configured")
    redirect_uri = request.url_for("auth_callback", provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}")
async def auth_callback(request: Request, provider: str):
    if provider not in oauth:
        raise HTTPException(status_code=400, detail="Provider not configured")
    token = await oauth.create_client(provider).authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        # For providers like GitHub: fetch user
        if provider == "github":
            resp = await oauth.github.get("user", token=token)
            userinfo = resp.json()
    # In a real app, issue your own session/jwt
    return {
        "provider": provider,
        "profile": userinfo,
        "token": {k: v for k, v in token.items() if k != "access_token"},
    }

