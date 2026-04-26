from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# 🔥 PostgreSQL engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True  # ✅ SQLAlchemy 2.0 uyumluluk (ÖNERİLİR)
)

# 🔥 Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # ✅ response objelerinde bug önler
    future=True              # ✅ SQLAlchemy 2.0 uyumluluk
)

# 🔥 FastAPI DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()