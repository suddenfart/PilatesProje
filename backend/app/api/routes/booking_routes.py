from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user_package import UserPackage

from app.schemas.booking_schema import BookingCreate, BookingOut
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=BookingOut)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    # 1. ders var mı?
    class_obj = db.query(Class).filter(Class.id == data.class_id).first()

    if not class_obj:
        raise HTTPException(status_code=404, detail="Ders bulunamadı")

    # 2. aynı kullanıcı aynı derse kayıtlı mı?
    existing_booking = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.class_id == data.class_id
    ).first()

    if existing_booking:
        raise HTTPException(status_code=400, detail="Zaten bu derse kayıtlısın")

    # 3. kapasite kontrol (6 kişi vb.)
    current_count = db.query(Booking).filter(
        Booking.class_id == data.class_id
    ).count()

    if current_count >= class_obj.capacity:
        raise HTTPException(status_code=400, detail="Ders dolu")

    # 4. paket kontrol
    package = db.query(UserPackage).filter(
        UserPackage.user_id == user_id
    ).first()

    if not package:
        raise HTTPException(status_code=400, detail="Paket bulunamadı")

    if package.remaining_sessions <= 0:
        raise HTTPException(status_code=400, detail="Kalan ders hakkın yok")

    # 5. booking oluştur
    booking = Booking(
        user_id=user_id,
        class_id=data.class_id
    )

    db.add(booking)

    # 6. paket düş
    package.remaining_sessions -= 1

    db.commit()
    db.refresh(booking)

    return booking


# OPTIONAL: kullanıcının booking'lerini görme
@router.get("/my", response_model=list[BookingOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Booking).filter(
        Booking.user_id == current_user["user_id"]
    ).all()