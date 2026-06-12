# models package — import all so Base.metadata knows about every table
from models.user    import User       # noqa: F401
from models.product import Product    # noqa: F401
from models.cart    import CartItem   # noqa: F401
from models.order   import Order, OrderItem  # noqa: F401
