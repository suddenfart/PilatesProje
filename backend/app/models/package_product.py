from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.db.base import Base


class PackageProduct(Base):
    __tablename__ = "package_products"

    id = Column(Integer, primary_key=True, index=True)

    # 🏷️ paket adı
    name = Column(String(100), nullable=False)

    # 🔢 kaç session
    sessions = Column(Integer, nullable=False)

    # 💰 fiyat (Stripe uyumlu → cent bazlı önerilir)
    price = Column(Integer, nullable=False)  
    # örnek: 99900 = 999.00 TL

    # 📦 aktif/pasif ürün
    is_active = Column(Boolean, default=True)

    # 🧾 audit
    created_at = Column(DateTime, default=datetime.utcnow)