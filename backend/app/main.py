from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base

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

# 🧭 ROUTES (PREFIXLER ROUTER'DA)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(class_routes.router)
app.include_router(booking_routes.router)
app.include_router(user_package_routes.router)
app.include_router(stripe_routes.router)

# 🏠 ROOT
@app.get("/")
def root():
    return {"message": "Pilates API running 🚀"}

# 🧱 DB INIT (dev)
Base.metadata.create_all(bind=engine)