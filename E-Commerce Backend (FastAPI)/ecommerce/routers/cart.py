"""
routers/cart.py  —  Shopping Cart (per-user)
  GET    /cart          — view my cart
  POST   /cart          — add item
  PUT    /cart/{id}     — update quantity
  DELETE /cart/{id}     — remove item
  DELETE /cart          — clear entire cart
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database  import get_db
from core.security  import get_current_user
from models.user    import User
from models.cart    import CartItem
from models.product import Product
from schemas        import CartItemCreate, CartItemUpdate, CartItemOut, CartOut

router = APIRouter()


def _get_cart_total(items: list) -> float:
    return round(sum(i.product.price * i.quantity for i in items), 2)


@router.get("/", response_model=CartOut, summary="View my cart")
def view_cart(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return CartOut(
        items       = items,
        total_items = sum(i.quantity for i in items),
        total_price = _get_cart_total(items),
    )


@router.post("/", response_model=CartItemOut, status_code=201,
             summary="Add item to cart")
def add_to_cart(
    payload:      CartItemCreate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    product = db.query(Product).filter(
        Product.id == payload.product_id, Product.is_active == True  # noqa: E712
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < payload.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} units in stock",
        )

    # If already in cart — increment quantity
    existing = db.query(CartItem).filter(
        CartItem.user_id    == current_user.id,
        CartItem.product_id == payload.product_id,
    ).first()

    if existing:
        new_qty = existing.quantity + payload.quantity
        if new_qty > product.stock:
            raise HTTPException(status_code=400, detail="Exceeds available stock")
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(
        user_id    = current_user.id,
        product_id = payload.product_id,
        quantity   = payload.quantity,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=CartItemOut,
            summary="Update cart item quantity")
def update_cart_item(
    item_id:      int,
    payload:      CartItemUpdate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    item = db.query(CartItem).filter(
        CartItem.id      == item_id,
        CartItem.user_id == current_user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if payload.quantity > item.product.stock:
        raise HTTPException(status_code=400, detail="Exceeds available stock")
    item.quantity = payload.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", summary="Remove item from cart")
def remove_cart_item(
    item_id:      int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    item = db.query(CartItem).filter(
        CartItem.id      == item_id,
        CartItem.user_id == current_user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}


@router.delete("/", summary="Clear entire cart")
def clear_cart(
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
