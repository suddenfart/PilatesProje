from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.deps import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

# 🔥 PREFIX EKLENDİ
router = APIRouter(prefix="/auth", tags=["Auth"])


# 📦 REQUEST MODELS
class AuthRequest(BaseModel):
    email: str
    password: str


# ---------------- REGISTER ----------------
@router.post("/register")
def register(data: AuthRequest, db: Session = Depends(get_db)):

    user_exists = db.query(User).filter(User.email == data.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }


# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: AuthRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id
    }