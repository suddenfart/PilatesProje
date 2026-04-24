from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.deps import get_db
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/")
def create_class(data: ClassCreate, db: Session = Depends(get_db)):

    # datetime birleştirme
    start_dt = datetime.combine(data.date, data.start_time)
    end_dt = datetime.combine(data.date, data.end_time)

    if start_dt >= end_dt:
        raise HTTPException(status_code=400, detail="Invalid time range")

    # overlap check
    existing = db.query(Class).filter(
        Class.start_time < end_dt,
        Class.end_time > start_dt
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Time slot occupied")

    new_class = Class(
        start_time=start_dt,
        end_time=end_dt,
        capacity=data.capacity
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class


@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    return db.query(Class).all()