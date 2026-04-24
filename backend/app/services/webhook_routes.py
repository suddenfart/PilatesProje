import stripe
from fastapi import APIRouter, Request
from app.core.settings import settings
from app.models.user_package import UserPackage
from app.models.package_product import PackageProduct
from app.db.session import SessionLocal

router = APIRouter()


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except Exception as e:
        return {"error": str(e)}


    # -------------------------
    # PAYMENT SUCCESS
    # -------------------------
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]
        package_id = session["metadata"]["package_id"]

        db = SessionLocal()

        package = db.query(PackageProduct).filter(
            PackageProduct.id == package_id
        ).first()

        user_package = db.query(UserPackage).filter(
            UserPackage.user_id == user_id
        ).first()

        # -------------------------
        # CREATE OR UPDATE PACKAGE
        # -------------------------
        if user_package:
            user_package.total_sessions += package.sessions
            user_package.remaining_sessions += package.sessions
        else:
            user_package = UserPackage(
                user_id=user_id,
                total_sessions=package.sessions,
                remaining_sessions=package.sessions
            )
            db.add(user_package)

        db.commit()
        db.close()

    return {"status": "success"}