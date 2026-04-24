from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut
from app.core.security import hash_password

# ✅ PREFIX EKLENDİ (EN KRİTİK DÜZELTME)
router = APIRouter(prefix="/users", tags=["Users"])


# 👤 CREATE USER (REGISTER)
@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # 🔍 EMAIL KONTROL
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # 🔐 PASSWORD HASH
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# 📋 GET ALL USERS
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()