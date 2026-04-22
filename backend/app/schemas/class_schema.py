from pydantic import BaseModel
from datetime import date, time

class ClassCreate(BaseModel):
    date: date
    start_time: time
    end_time: time
    capacity: int = 6


class ClassOut(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time
    capacity: int

    class Config:
        from_attributes = True