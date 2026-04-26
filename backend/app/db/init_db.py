from app.db.base import Base
from app.db.session import engine

# 🔥 BU IMPORTLAR ZORUNLU (yoksa tablo oluşmaz)
import app.models.user
import app.models.class_model
import app.models.booking
import app.models.user_package
import app.models.package_product

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")