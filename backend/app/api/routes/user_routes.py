from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut
from app.core.security import hash_password

# ⚠️ ADMIN ROUTE OLMALI
router = APIRouter(prefix="/users", tags=["Users"])


# 👤 CREATE USER (SADECE ADMIN KULLANMALI)
@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    email = user_data.email.lower().strip()

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=user_data.name,
        email=email,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# 📋 GET ALL USERS (ADMIN ONLY)
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users