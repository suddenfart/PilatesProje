from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class PackageProduct(Base):
    __tablename__ = "package_products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)  # "8 Session Reformer"
    sessions = Column(Integer)  # 8
    price = Column(Float)  # 999.0