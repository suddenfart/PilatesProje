from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class UserPackage(Base):
    __tablename__ = "user_packages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    total_sessions = Column(Integer, default=10)
    remaining_sessions = Column(Integer, default=10)