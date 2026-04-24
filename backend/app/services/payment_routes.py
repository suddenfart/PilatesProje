from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.package_product import PackageProduct
from app.services.stripe_service import create_checkout_session

router = APIRouter()


@router.post("/checkout")
def checkout(package_id: int, user_id: int, db: Session = Depends(get_db)):

    package = db.query(PackageProduct).filter(
        PackageProduct.id == package_id
    ).first()

    session = create_checkout_session(package, user_id)

    return {
        "checkout_url": session.url
    }