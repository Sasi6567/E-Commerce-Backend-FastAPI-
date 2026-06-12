"""
schemas/  —  All Pydantic request/response models in one file
             (split into separate files for larger projects).
"""

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator


# ═══════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None


# ═══════════════════════════════════════════════════════
# USER
# ═══════════════════════════════════════════════════════

class UserCreate(BaseModel):
    name:     str       = Field(..., min_length=2, max_length=100)
    email:    EmailStr
    password: str       = Field(..., min_length=6)

class UserUpdate(BaseModel):
    name:  Optional[str]      = None
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    is_active:  bool
    is_admin:   bool
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════
# PRODUCT
# ═══════════════════════════════════════════════════════

class ProductCreate(BaseModel):
    name:        str   = Field(..., min_length=2, max_length=200)
    description: Optional[str]  = None
    price:       float = Field(..., gt=0)
    stock:       int   = Field(default=0, ge=0)
    category:    Optional[str]  = None
    image_url:   Optional[str]  = None

class ProductUpdate(BaseModel):
    name:        Optional[str]   = None
    description: Optional[str]   = None
    price:       Optional[float] = Field(default=None, gt=0)
    stock:       Optional[int]   = Field(default=None, ge=0)
    category:    Optional[str]   = None
    image_url:   Optional[str]   = None
    is_active:   Optional[bool]  = None

class ProductOut(BaseModel):
    id:          int
    name:        str
    description: Optional[str]
    price:       float
    stock:       int
    category:    Optional[str]
    image_url:   Optional[str]
    is_active:   bool
    created_at:  datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════
# CART
# ═══════════════════════════════════════════════════════

class CartItemCreate(BaseModel):
    product_id: int
    quantity:   int = Field(default=1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItemOut(BaseModel):
    id:         int
    product_id: int
    quantity:   int
    product:    ProductOut
    added_at:   datetime

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    items:       List[CartItemOut]
    total_items: int
    total_price: float


# ═══════════════════════════════════════════════════════
# ORDER
# ═══════════════════════════════════════════════════════

class OrderCreate(BaseModel):
    shipping_address: Optional[str] = None

class OrderItemOut(BaseModel):
    id:         int
    product_id: Optional[int]
    quantity:   int
    unit_price: float
    product:    Optional[ProductOut]

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id:               int
    user_id:          int
    total_amount:     float
    status:           str
    shipping_address: Optional[str]
    created_at:       datetime
    items:            List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description="pending | confirmed | shipped | delivered | cancelled")
