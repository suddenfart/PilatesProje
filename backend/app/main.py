from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.api.routes import user_routes, class_routes, booking_routes
from app.api.routes import auth_routes


app = FastAPI(title="Pilates Proje API")

# DB tablolarını oluşturur (prod’da genelde kaldırılır, burada dev için OK)
Base.metadata.create_all(bind=engine)


# ROUTES
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(class_routes.router, prefix="/classes", tags=["Classes"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["Bookings"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    return {
        "message": "Pilates API çalışıyor 🚀",
        "docs": "/docs"
    }