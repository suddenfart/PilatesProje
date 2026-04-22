from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 🔐 JWT ayarları
SECRET_KEY = "supersecretkey123"  # sonra .env'e alınmalı
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔑 password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔒 token security scheme
security = HTTPBearer()


# -------------------------
# PASSWORD FUNCTIONS
# -------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------
# JWT FUNCTIONS
# -------------------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token")


# -------------------------
# PROTECTED ROUTE DEPENDENCY
# -------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Kimlik doğrulama başarısız")

    return {
        "user_id": user_id,
        "role": role
    }