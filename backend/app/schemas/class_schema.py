from pydantic import BaseModel
from datetime import datetime

class ClassCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int = 6


class ClassOut(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    capacity: int

    class Config:
        from_attributes = True