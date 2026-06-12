"""
models/cart.py  —  CartItem table (one row per user+product)
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id",    ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity   = Column(Integer, default=1)
    added_at   = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user    = relationship("User",    back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
