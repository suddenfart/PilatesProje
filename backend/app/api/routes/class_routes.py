from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.deps import get_db
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate

router = APIRouter(prefix="/classes", tags=["Classes"])


# 🧘 CREATE CLASS
@router.post("/")
def create_class(data: ClassCreate, db: Session = Depends(get_db)):

    start_dt = datetime.combine(data.date, data.start_time)
    end_dt = datetime.combine(data.date, data.end_time)

    if start_dt >= end_dt:
        raise HTTPException(400, "Invalid time range")

    if data.capacity <= 0:
        raise HTTPException(400, "Invalid capacity")

    # 👇 TEACHER CONFLICT CHECK (KRİTİK)
    existing = db.query(Class).filter(
        Class.teacher_id == data.teacher_id,
        Class.start_time < end_dt,
        Class.end_time > start_dt
    ).first()

    if existing:
        raise HTTPException(400, "Teacher already has class in this time slot")

    new_class = Class(
        start_time=start_dt,
        end_time=end_dt,
        capacity=data.capacity,
        teacher_id=data.teacher_id,
        status="active"
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class


# 📋 GET CLASSES (OPTIONAL FILTER)
@router.get("/")
def get_classes(date: str = None, db: Session = Depends(get_db)):

    query = db.query(Class)

    if date:
        query = query.filter(
            Class.start_time >= date + " 00:00:00",
            Class.start_time <= date + " 23:59:59"
        )

    return query.all()