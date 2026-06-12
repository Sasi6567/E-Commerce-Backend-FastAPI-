"""
routers/products.py  —  Product CRUD
  GET    /products          — list (public, with filters)
  GET    /products/{id}     — detail (public)
  POST   /products          — create (admin)
  PUT    /products/{id}     — full update (admin)
  PATCH  /products/{id}     — partial update (admin)
  DELETE /products/{id}     — delete (admin)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database  import get_db
from core.security  import get_current_admin
from models.user    import User
from models.product import Product
from schemas        import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()


# ── Public: browse products ───────────────────────────────────
@router.get("/", response_model=List[ProductOut], summary="List products")
def list_products(
    skip:     int            = Query(0,    ge=0),
    limit:    int            = Query(20,   ge=1, le=100),
    category: Optional[str] = Query(None, description="Filter by category"),
    search:   Optional[str] = Query(None, description="Search in name/description"),
    db:       Session        = Depends(get_db),
):
    q = db.query(Product).filter(Product.is_active == True)  # noqa: E712
    if category:
        q = q.filter(Product.category == category)
    if search:
        like = f"%{search}%"
        q = q.filter(
            Product.name.ilike(like) | Product.description.ilike(like)
        )
    return q.offset(skip).limit(limit).all()


@router.get("/categories", summary="List all distinct categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Product.category).distinct().filter(
        Product.category != None  # noqa: E711
    ).all()
    return {"categories": [r[0] for r in rows]}


@router.get("/{product_id}", response_model=ProductOut, summary="Get product detail")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id, Product.is_active == True  # noqa: E712
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ── Admin: manage products ────────────────────────────────────
@router.post("/", response_model=ProductOut, status_code=201,
             summary="[Admin] Create product")
def create_product(
    payload: ProductCreate,
    db:      Session = Depends(get_db),
    _:       User    = Depends(get_current_admin),
):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut,
            summary="[Admin] Full update product")
def update_product(
    product_id: int,
    payload:    ProductCreate,
    db:         Session = Depends(get_db),
    _:          User    = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in payload.model_dump().items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}", response_model=ProductOut,
              summary="[Admin] Partial update product")
def patch_product(
    product_id: int,
    payload:    ProductUpdate,
    db:         Session = Depends(get_db),
    _:          User    = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", summary="[Admin] Delete product")
def delete_product(
    product_id: int,
    db:         Session = Depends(get_db),
    _:          User    = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted"}
