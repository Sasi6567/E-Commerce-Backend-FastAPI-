"""
models/product.py  —  Product table
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price       = Column(Float,  nullable=False)
    stock       = Column(Integer, default=0)
    category    = Column(String(100), nullable=True, index=True)
    image_url   = Column(String(500), nullable=True)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cart_items  = relationship("CartItem",  back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
