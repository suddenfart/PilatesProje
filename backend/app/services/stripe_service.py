import stripe
from app.core.settings import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(package, user_id):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "try",
                "product_data": {
                    "name": package.name,
                },
                "unit_amount": int(package.price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
        metadata={
            "user_id": user_id,
            "package_id": package.id
        }
    )

    return session