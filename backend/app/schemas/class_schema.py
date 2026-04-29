from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClassCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int = 6


class ClassOut(BaseModel):
    id: int

    # 🕒 backend compatibility
    start_time: datetime
    end_time: datetime

    # 📅 NEW: calendar fields
    day: Optional[int] = None
    hour: Optional[int] = None

    capacity: int

    class Config:
        from_attributes = True