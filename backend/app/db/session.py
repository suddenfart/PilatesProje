from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
print("DEBUG DB:", DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL log görmek için
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)