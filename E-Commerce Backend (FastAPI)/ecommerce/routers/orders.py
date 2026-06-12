"""
routers/orders.py  —  Orders
  POST   /orders              — place order from cart
  GET    /orders              — my order history
  GET    /orders/{id}         — order detail
  PATCH  /orders/{id}/cancel  — cancel order (user)
  GET    /orders/all          — [admin] all orders
  PATCH  /orders/{id}/status  — [admin] update status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database  import get_db
from core.security  import get_current_user, get_current_admin
from models.user    import User
from models.cart    import CartItem
from models.order   import Order, OrderItem, OrderStatus
from schemas        import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter()


# ── Place order from cart ─────────────────────────────────────
@router.post("/", response_model=OrderOut, status_code=201,
             summary="Place order from current cart")
def place_order(
    payload:      OrderCreate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Validate stock & compute total
    total = 0.0
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{item.product.name}'",
            )
        total += item.product.price * item.quantity

    # Create order
    order = Order(
        user_id          = current_user.id,
        total_amount     = round(total, 2),
        shipping_address = payload.shipping_address,
    )
    db.add(order)
    db.flush()  # get order.id before adding items

    # Create order items + deduct stock
    for item in cart_items:
        order_item = OrderItem(
            order_id   = order.id,
            product_id = item.product_id,
            quantity   = item.quantity,
            unit_price = item.product.price,
        )
        db.add(order_item)
        item.product.stock -= item.quantity

    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)
    return order


# ── My orders ─────────────────────────────────────────────────
@router.get("/", response_model=List[OrderOut], summary="My order history")
def my_orders(
    skip:         int     = 0,
    limit:        int     = 20,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    return (
        db.query(Order)
          .filter(Order.user_id == current_user.id)
          .order_by(Order.created_at.desc())
          .offset(skip).limit(limit)
          .all()
    )


@router.get("/all", response_model=List[OrderOut],
            summary="[Admin] List all orders")
def all_orders(
    skip:  int     = 0,
    limit: int     = 50,
    db:    Session = Depends(get_db),
    _:     User    = Depends(get_current_admin),
):
    return (
        db.query(Order)
          .order_by(Order.created_at.desc())
          .offset(skip).limit(limit)
          .all()
    )


@router.get("/{order_id}", response_model=OrderOut, summary="Order detail")
def get_order(
    order_id:     int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return order


@router.patch("/{order_id}/cancel", response_model=OrderOut,
              summary="Cancel my order (only if pending)")
def cancel_order(
    order_id:     int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    order = db.query(Order).filter(
        Order.id      == order_id,
        Order.user_id == current_user.id,
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != OrderStatus.pending:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel an order with status '{order.status}'",
        )

    # Restore stock
    for item in order.items:
        if item.product:
            item.product.stock += item.quantity

    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order


@router.patch("/{order_id}/status", response_model=OrderOut,
              summary="[Admin] Update order status")
def update_order_status(
    order_id: int,
    payload:  OrderStatusUpdate,
    db:       Session = Depends(get_db),
    _:        User    = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        order.status = OrderStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {payload.status}")

    db.commit()
    db.refresh(order)
    return order
