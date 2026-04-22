from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.class_model import Class
from app.models.booking import Booking
from app.models.user_package import UserPackage

print("📦 Tablolar oluşturuluyor...")

Base.metadata.create_all(bind=engine)

print("✅ Tüm tablolar oluşturuldu")