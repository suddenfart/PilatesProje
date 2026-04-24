from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# 🔥 PostgreSQL connection (tek doğru kaynak: settings.py)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # bağlantı koparsa otomatik kontrol eder
    pool_size=10,
    max_overflow=20
)

# 🔥 DB session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🔥 FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()