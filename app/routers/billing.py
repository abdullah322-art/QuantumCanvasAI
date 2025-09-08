import os, time
from fastapi import APIRouter
from pydantic import BaseModel
import stripe

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

PLANS = [
    {"id": "free", "name": "Free", "price": 0, "models": ["QCA-4.9", "QCA-5.0"]},
    {"id": "starter", "name": "Starter", "price": 9, "models": ["QCA-5.2", "QCA-5.4"]},
    {"id": "pro", "name": "Pro", "price": 29, "models": ["QCA-5.6", "QCA-5.8"]},
    {"id": "elite", "name": "Elite", "price": 79, "models": ["QCA-6.0", "QCA-6.2"]},
    {"id": "supreme", "name": "QCA 6.8 SUPREME", "price": 149, "models": ["QCA-6.5", "QCA-6.8-SUPREME"]},
]

SAUDI_95_EVENT = {
    "active": True,
    "percent_off": 25,
    "code": "SAUDI95",
}

@router.get("/prices")
def prices():
    now = int(time.time())
    prices = []
    for p in PLANS:
        price = p["price"]
        discount = 0
        if SAUDI_95_EVENT["active"]:
            discount = int(price * SAUDI_95_EVENT["percent_off"] / 100)
        prices.append({
            "id": p["id"],
            "name": p["name"],
            "price": price,
            "discount": discount,
            "final": max(0, price - discount),
            "models": p["models"],
        })
    return {"currency": "USD", "plans": prices, "event": SAUDI_95_EVENT}

class CheckoutRequest(BaseModel):
    plan_id: str
    success_url: str
    cancel_url: str

@router.post("/create-checkout-session")
def create_checkout_session(req: CheckoutRequest):
    if not stripe.api_key:
        return {"status": "mock", "checkout_url": req.success_url + "?session_id=dummy"}
    plan = next((p for p in PLANS if p["id"] == req.plan_id), None)
    if not plan:
        return {"error": "unknown plan"}
    amount = plan["price"] * 100
    if SAUDI_95_EVENT["active"]:
        amount = int(amount * (100 - SAUDI_95_EVENT["percent_off"]) / 100)
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price_data": {"currency": "usd", "product_data": {"name": plan["name"]}, "unit_amount": amount}, "quantity": 1}],
        success_url=req.success_url,
        cancel_url=req.cancel_url,
    )
    return {"status": "ok", "id": session.id, "checkout_url": session.url}
