from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassOut

router = APIRouter()


@router.post("/", response_model=ClassOut)
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    new_class = Class(
        date=class_data.date,
        start_time=class_data.start_time,
        end_time=class_data.end_time,
        capacity=class_data.capacity
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class