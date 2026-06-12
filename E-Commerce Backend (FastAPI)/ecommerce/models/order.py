"""
models/order.py  —  Order + OrderItem tables
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from core.database import Base


class OrderStatus(str, enum.Enum):
    pending    = "pending"
    confirmed  = "confirmed"
    shipped    = "shipped"
    delivered  = "delivered"
    cancelled  = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_amount    = Column(Float, nullable=False)
    status          = Column(Enum(OrderStatus), default=OrderStatus.pending)
    shipping_address = Column(String(500), nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user  = relationship("User",      back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id",   ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float,   nullable=False)  # snapshot at time of order

    # Relationships
    order   = relationship("Order",   back_populates="items")
    product = relationship("Product", back_populates="order_items")
