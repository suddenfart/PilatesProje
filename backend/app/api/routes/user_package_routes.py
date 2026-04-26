from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.deps import get_db
from app.models.user_package import UserPackage
from app.models.user import User

router = APIRouter(prefix="/packages", tags=["User Packages"])


# 📦 CREATE PACKAGE (ADMIN ONLY OLDUĞUNU FARZ EDİYORUZ)
@router.post("/create")
def create_package(
    user_id: int,
    sessions: int = 10,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    package = UserPackage(
        user_id=user_id,
        total_sessions=sessions,
        remaining_sessions=sessions,
        expiry_date=None
    )

    db.add(package)
    db.commit()
    db.refresh(package)

    return {
        "message": "Package created",
        "package_id": package.id
    }


# 📊 GET ALL USER PACKAGES
@router.get("/user/{user_id}")
def get_user_packages(user_id: int, db: Session = Depends(get_db)):

    packages = db.query(UserPackage).filter(
        UserPackage.user_id == user_id
    ).all()

    return packages


# ⚠️ BU ENDPOINT KALDIRILMALI (DEPRECATED)
@router.post("/decrease/{user_id}")
def decrease_session(user_id: int, db: Session = Depends(get_db)):
    raise HTTPException(
        status_code=410,
        detail="Deprecated. Use /bookings instead"
    )