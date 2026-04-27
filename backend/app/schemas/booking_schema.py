from pydantic import BaseModel

class BookingCreate(BaseModel):
    class_id: int   # ✅ SADECE BU

class BookingOut(BaseModel):
    id: int
    user_id: int
    class_id: int

    class Config:
        from_attributes = True