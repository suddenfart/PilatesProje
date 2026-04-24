import os
import stripe

from fastapi import APIRouter, HTTPException, Request

from app.core.plans import PLANS
from app.db.session import SessionLocal
from app.models.user_package import UserPackage

router = APIRouter(prefix="/stripe", tags=["Stripe"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# 💳 CREATE CHECKOUT SESSION
@router.post("/checkout")
def create_checkout(user_id: int, plan: str):

    # 🔍 plan validation
    if plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Pilates Package - {plan}"
                        },
                        "unit_amount": PLANS[plan]["price"],
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            metadata={
                "user_id": str(user_id),
                "sessions": str(PLANS[plan]["sessions"])
            }
        )

        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ⚡ STRIPE WEBHOOK (PAYMENT SUCCESS → PACKAGE CREATE)
@router.post("/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 💥 PAYMENT SUCCESS EVENT
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        user_id = int(session["metadata"]["user_id"])
        sessions = int(session["metadata"]["sessions"])

        db = SessionLocal()

        # 🔍 check existing package
        existing = db.query(UserPackage).filter(
            UserPackage.user_id == user_id
        ).first()

        # 📦 create package if not exists
        if not existing:
            package = UserPackage(
                user_id=user_id,
                total_sessions=sessions,
                remaining_sessions=sessions
            )

            db.add(package)
            db.commit()

        db.close()

    return {"status": "success"}