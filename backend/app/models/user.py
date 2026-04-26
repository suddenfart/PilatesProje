from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=True)

    email = Column(String(150), unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String(20), default="user", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
