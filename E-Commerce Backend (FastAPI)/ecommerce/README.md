# 🛒 E-Commerce Backend (FastAPI) — Basic Level

A complete e-commerce REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

---

## Features

| Module     | Endpoints                                      |
|------------|------------------------------------------------|
| **Auth**   | Register, Login (JWT)                          |
| **Users**  | Profile CRUD, Admin user management            |
| **Products** | Browse, Search, Filter by category (CRUD for admins) |
| **Cart**   | Add / Update / Remove / Clear cart             |
| **Orders** | Place order, View history, Cancel, Admin status update |

---

## Project Structure

```
ecommerce/
├── main.py                  # FastAPI app + router registration
├── seed.py                  # Populate DB with sample data
├── requirements.txt
│
├── core/
│   ├── database.py          # SQLAlchemy engine + session
│   └── security.py          # JWT + bcrypt + auth dependencies
│
├── models/
│   ├── user.py              # User table
│   ├── product.py           # Product table
│   ├── cart.py              # CartItem table
│   └── order.py             # Order + OrderItem tables
│
├── schemas/
│   └── __init__.py          # All Pydantic request/response models
│
└── routers/
    ├── auth.py              # POST /auth/register, /auth/login
    ├── users.py             # GET|PUT /users/me, admin CRUD
    ├── products.py          # GET /products (public), CRUD (admin)
    ├── cart.py              # Shopping cart endpoints
    └── orders.py            # Place & manage orders
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed sample data
```bash
python seed.py
```

### 3. Start the server
```bash
uvicorn main:app --reload
```

### 4. Open the API docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:**       http://localhost:8000/redoc

---

## API Usage Examples

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"john123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=john@example.com&password=john123"
# → returns: {"access_token": "eyJ...", "token_type": "bearer"}
```

### Browse products
```bash
curl http://localhost:8000/products
curl "http://localhost:8000/products?category=Electronics&search=keyboard"
```

### Add to cart (requires auth)
```bash
curl -X POST http://localhost:8000/cart \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Place order
```bash
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"shipping_address": "123 Main St, Mumbai"}'
```

---

## Seed Credentials

| Role  | Email                 | Password  |
|-------|-----------------------|-----------|
| Admin | admin@shop.com        | admin123  |
| User  | alice@example.com     | alice123  |
| User  | bob@example.com       | bob123    |

---

## Tech Stack

| Library          | Purpose                          |
|------------------|----------------------------------|
| FastAPI          | Web framework + automatic docs   |
| SQLAlchemy       | ORM + database layer             |
| SQLite           | Database (swap for Postgres/MySQL)|
| Pydantic v2      | Request/response validation      |
| python-jose      | JWT token creation/verification  |
| passlib + bcrypt | Password hashing                 |
| uvicorn          | ASGI server                      |

---

## Switching to PostgreSQL

In `core/database.py`, replace:
```python
DATABASE_URL = "sqlite:///./ecommerce.db"
```
with:
```python
DATABASE_URL = "postgresql://user:password@localhost/ecommerce_db"
```
Then `pip install psycopg2-binary`.
