from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.deps import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Kayıt olma (Register) için kullanılan Pydantic modeli
class UserRegister(BaseModel):
    email: EmailStr
    password: str

# Token yanıtı için standart format
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    # Kullanıcı zaten var mı kontrol et
    user_exists = db.query(User).filter(User.email == data.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already exists"
        )

    # Yeni kullanıcı oluştur
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user_id": new_user.id}

@router.post("/login", response_model=Token)
def login(
    data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Swagger 'Authorize' butonu ile uyumlu login endpoint'i.
    Swagger'daki 'username' alanına kullanıcının email adresi girilmelidir.
    """
    # OAuth2PasswordRequestForm veriyi 'username' ve 'password' olarak getirir
    user = db.query(User).filter(User.email == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT Token oluştur
    token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id
    }