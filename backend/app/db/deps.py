from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 🔐 TOKEN'DAN USER ÇEKME
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = payload.get("user_id")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return {
        "user": user,
        "role": role
    }


# 👑 ADMIN CHECK
def require_admin(current=Depends(get_current_user)):
    if current["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current


# 👤 SADECE USER (opsiyonel kullanım)
def require_user(current=Depends(get_current_user)):
    if current["role"] not in ["user", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="User access required"
        )
    return current