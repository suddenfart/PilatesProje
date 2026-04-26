from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    # 🏷️ opsiyonel ama çok faydalı
    title = Column(String(100), nullable=True)

    # 🕒 gerçek zaman alanı
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # 👥 kapasite
    capacity = Column(Integer, default=6, nullable=False)

    # 🧾 audit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher = relationship("User")
