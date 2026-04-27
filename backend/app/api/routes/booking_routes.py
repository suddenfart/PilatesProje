from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user_package import UserPackage
from app.schemas.booking_schema import BookingCreate
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/")
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 📦 PACKAGE CHECK / AUTO CREATE
    package = db.query(UserPackage).filter(
        UserPackage.user_id == current_user.id
    ).first()

    if not package:
        package = UserPackage(
            user_id=current_user.id,
            total_sessions=10,
            remaining_sessions=10
        )
        db.add(package)
        db.commit()
        db.refresh(package)

    if package.remaining_sessions <= 0:
        raise HTTPException(
            status_code=400,
            detail="No sessions left"
        )

    # 📅 CLASS CHECK
    class_obj = db.query(Class).filter(
        Class.id == data.class_id
    ).first()

    if not class_obj:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    # 🚨 DUPLICATE BOOKING CHECK
    existing = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.class_id == data.class_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already booked"
        )

    # 📌 CREATE BOOKING
    booking = Booking(
        user_id=current_user.id,
        class_id=data.class_id
    )

    # 📉 SESSION DECREASE
    package.remaining_sessions -= 1

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking created successfully",
        "booking_id": booking.id,
        "remaining_sessions": package.remaining_sessions
    }