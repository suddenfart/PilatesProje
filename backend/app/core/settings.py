import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # -------------------------
    # DATABASE
    # -------------------------
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:1234@localhost:5432/pilates_db"
    )

    # -------------------------
    # JWT AUTH
    # -------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # -------------------------
    # STRIPE
    # -------------------------
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # -------------------------
    # APP SETTINGS
    # -------------------------
    APP_NAME: str = "Pilates Studio API"
    DEBUG: bool = True


settings = Settings()