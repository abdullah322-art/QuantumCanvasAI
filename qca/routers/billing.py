from __future__ import annotations

import os
from typing import Optional

import stripe
from fastapi import APIRouter, HTTPException, Request

from ..config import settings


router = APIRouter(prefix="/billing", tags=["billing"])


def _require_stripe():
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=400, detail="Stripe not configured")
    stripe.api_key = settings.stripe_secret_key


@router.post("/create-checkout-session")
def create_checkout_session(payload: dict):
    _require_stripe()
    price_id = payload.get("price_id") or settings.stripe_price_pro
    if not price_id:
        raise HTTPException(status_code=400, detail="Missing price id")
    promo_code = payload.get("promo_code")
    discounts = None
    if promo_code and promo_code.upper() == (settings.sa95_promo_code or "").upper():
        discounts = [{"coupon": "SA95_COUPON_PLACEHOLDER"}]  # create in Stripe dashboard
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=payload.get("success_url", "https://example.com/success"),
        cancel_url=payload.get("cancel_url", "https://example.com/cancel"),
        discounts=discounts,
    )
    return {"id": session.id}


@router.post("/webhook")
async def stripe_webhook(request: Request):
    _require_stripe()
    payload = await request.body()
    sig = request.headers.get("Stripe-Signature")
    webhook_secret = settings.stripe_webhook_secret
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig, webhook_secret)
        else:
            event = stripe.Event.construct_from(request.json(), stripe.api_key)  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))

    # Handle events (simplified)
    if event["type"] == "checkout.session.completed":
        pass
    return {"received": True}

