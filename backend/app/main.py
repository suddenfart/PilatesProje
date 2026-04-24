from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import user_routes, class_routes, booking_routes, user_package_routes, stripe_routes, auth_routes

app = FastAPI()

# 🔥 CORS (frontend bağlanması için şart)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 ROUTES
app.include_router(user_routes.router)
app.include_router(class_routes.router)
app.include_router(booking_routes.router)
app.include_router(user_package_routes.router)
app.include_router(stripe_routes.router)
app.include_router(auth_routes.router) 

@app.get("/")
def root():
    return {"message": "API running 🚀"}