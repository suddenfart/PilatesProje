from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    auth_routes,
    class_routes,
    booking_routes,
    user_routes
)

app = FastAPI()

# CORS (frontend için şart)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(auth_routes.router)
app.include_router(class_routes.router)
app.include_router(booking_routes.router)
app.include_router(user_routes.router)


@app.get("/")
def root():
    return {"status": "ok"}