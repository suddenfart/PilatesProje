from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime

from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    class_id = Column(
        Integer,
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🚨 KRİTİK: duplicate booking engeli
    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uq_user_class_booking"),
    )