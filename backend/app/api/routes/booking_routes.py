from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user_package import UserPackage
from datetime import datetime

router = APIRouter()


@router.post("/book")
def create_booking(user_id: int, class_id: int, db: Session = Depends(get_db)):

    # 🔒 TRANSACTION BAŞLAT
    try:
        with db.begin():

            # 1. CLASS kilitle (race condition önlemek için)
            class_obj = db.execute(
                select(Class)
                .where(Class.id == class_id)
                .with_for_update()
            ).scalar_one_or_none()

            if not class_obj:
                raise HTTPException(status_code=404, detail="Class not found")

            # 2. USER PACKAGE kilitle
            package = db.execute(
                select(UserPackage)
                .where(UserPackage.user_id == user_id)
                .with_for_update()
            ).scalar_one_or_none()

            if not package:
                raise HTTPException(status_code=400, detail="User package not found")

            if package.remaining_sessions <= 0:
                raise HTTPException(status_code=400, detail="No remaining sessions")

            # 3. ZATEN BOOKING VAR MI?
            existing = db.execute(
                select(Booking).where(
                    Booking.user_id == user_id,
                    Booking.class_id == class_id
                )
            ).scalar_one_or_none()

            if existing:
                raise HTTPException(status_code=400, detail="Already booked")

            # 4. CAPACITY KONTROL
            booked_count = db.query(func.count(Booking.id)).filter(
                Booking.class_id == class_id
            ).scalar()

            if booked_count >= class_obj.capacity:
                raise HTTPException(status_code=400, detail="Class is full")

            # 5. BOOKING OLUŞTUR
            booking = Booking(
                user_id=user_id,
                class_id=class_id,
                created_at=datetime.utcnow()
            )
            db.add(booking)

            # 6. PACKAGE DÜŞ
            package.remaining_sessions -= 1

            db.add(package)

        return {"message": "Booking successful"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))