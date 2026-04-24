from sqlalchemy import Column, Integer, DateTime
from app.db.base import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    # 🔥 DB tarafı: tek gerçek kaynak datetime
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # 🧠 Studio kapasitesi
    capacity = Column(Integer, default=6, nullable=False)