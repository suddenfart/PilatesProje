from pydantic import BaseModel


# 🔐 Client sadece class_id gönderir
class BookingCreate(BaseModel):
    class_id: int


# 📦 Response modeli
class BookingOut(BaseModel):
    id: int
    user_id: int
    class_id: int

    class Config:
        from_attributes = True