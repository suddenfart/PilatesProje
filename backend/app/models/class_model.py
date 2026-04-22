from sqlalchemy import Column, Integer, Date, Time
from app.db.base import Base

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    capacity = Column(Integer, default=6)