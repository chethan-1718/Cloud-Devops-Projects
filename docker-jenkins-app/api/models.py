
from sqlalchemy import Column, Float, Integer, String
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default="pending"
    )
    task_id = Column(String(100), nullable=True, index=True)
