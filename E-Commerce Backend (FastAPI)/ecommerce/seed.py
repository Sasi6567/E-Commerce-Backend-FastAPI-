"""
seed.py  —  Populates the database with sample data.
Run once after the app has created the tables:
    python seed.py
"""

from core.database  import SessionLocal, engine, Base
import models  # registers all models with Base

from models.user    import User
from models.product import Product
from core.security  import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_users():
    if db.query(User).count() > 0:
        print("  Users already seeded — skipping.")
        return
    users = [
        User(name="Admin User",  email="admin@shop.com",
             password=hash_password("admin123"), is_admin=True),
        User(name="Alice Smith", email="alice@example.com",
             password=hash_password("alice123")),
        User(name="Bob Jones",   email="bob@example.com",
             password=hash_password("bob123")),
    ]
    db.add_all(users)
    db.commit()
    print(f"  ✔ Created {len(users)} users")


def seed_products():
    if db.query(Product).count() > 0:
        print("  Products already seeded — skipping.")
        return
    products = [
        # Electronics
        Product(name="Wireless Headphones",  category="Electronics",
                price=59.99, stock=50,
                description="Noise-cancelling Bluetooth headphones with 30hr battery.",
                image_url="https://via.placeholder.com/400x300?text=Headphones"),
        Product(name="Mechanical Keyboard", category="Electronics",
                price=89.99, stock=30,
                description="TKL mechanical keyboard with RGB backlight.",
                image_url="https://via.placeholder.com/400x300?text=Keyboard"),
        Product(name="USB-C Hub",           category="Electronics",
                price=34.99, stock=100,
                description="7-in-1 USB-C hub with HDMI, SD card, and USB 3.0.",
                image_url="https://via.placeholder.com/400x300?text=USB-Hub"),
        # Clothing
        Product(name="Classic White T-Shirt", category="Clothing",
                price=19.99, stock=200,
                description="100% cotton, machine washable, unisex fit.",
                image_url="https://via.placeholder.com/400x300?text=T-Shirt"),
        Product(name="Slim Fit Jeans",        category="Clothing",
                price=49.99, stock=75,
                description="Stretch denim, available in multiple sizes.",
                image_url="https://via.placeholder.com/400x300?text=Jeans"),
        # Books
        Product(name="Clean Code",        category="Books",
                price=35.00, stock=40,
                description="A handbook of agile software craftsmanship by Robert C. Martin.",
                image_url="https://via.placeholder.com/400x300?text=Clean+Code"),
        Product(name="Python Crash Course", category="Books",
                price=29.99, stock=60,
                description="A hands-on, project-based introduction to programming.",
                image_url="https://via.placeholder.com/400x300?text=Python+Book"),
        # Home
        Product(name="Desk Lamp",    category="Home",
                price=24.99, stock=80,
                description="LED desk lamp with adjustable color temperature.",
                image_url="https://via.placeholder.com/400x300?text=Lamp"),
        Product(name="Yoga Mat",     category="Home",
                price=29.99, stock=55,
                description="Non-slip, eco-friendly yoga mat, 6mm thick.",
                image_url="https://via.placeholder.com/400x300?text=Yoga+Mat"),
        Product(name="Coffee Maker", category="Home",
                price=79.99, stock=25,
                description="12-cup programmable coffee maker with auto shut-off.",
                image_url="https://via.placeholder.com/400x300?text=Coffee+Maker"),
    ]
    db.add_all(products)
    db.commit()
    print(f"  ✔ Created {len(products)} products")


if __name__ == "__main__":
    print("\nSeeding database …\n")
    seed_users()
    seed_products()
    print("\n✅  Seed complete!\n")
    print("  Admin  → admin@shop.com   / admin123")
    print("  User 1 → alice@example.com / alice123")
    print("  User 2 → bob@example.com   / bob123\n")
    db.close()
