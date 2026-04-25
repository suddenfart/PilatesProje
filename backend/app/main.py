from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base

# MODELS (DB init için)
from app.models import user, class_model, booking, user_package

# ROUTES (DOĞRU PATH)
from app.api.routes import (
    auth_routes,
    user_routes,
    class_routes,
    booking_routes,
    user_package_routes,
    stripe_routes,
)

app = FastAPI(title="Pilates API", version="0.1.0")

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧭 ROUTES INCLUDE
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(class_routes.router, prefix="/classes", tags=["Classes"])
app.include_router(booking_routes.router, prefix="/bookings", tags=["Bookings"])
app.include_router(user_package_routes.router, prefix="/packages", tags=["Packages"])
app.include_router(stripe_routes.router, prefix="/stripe", tags=["Stripe"])

# 🏠 ROOT
@app.get("/")
def root():
    return {"message": "Pilates API running 🚀"}

# 🧱 DB INIT (dev için)
Base.metadata.create_all(bind=engine)
