"""
E-Commerce Backend — FastAPI (Basic Level)
==========================================
Entry point: runs the FastAPI app, registers all routers,
creates DB tables on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import engine, Base
from routers import auth, users, products, cart, orders


# ── Create all tables on startup ────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# ── App instance ─────────────────────────────────────────────
app = FastAPI(
    title="🛒 E-Commerce API",
    description=(
        "A basic e-commerce backend built with FastAPI.\n\n"
        "**Features:** User auth (JWT), Products CRUD, "
        "Shopping Cart, Orders.\n\n"
        "Use `/docs` for interactive Swagger UI."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (allow all origins for dev) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────
app.include_router(auth.router,     prefix="/auth",     tags=["Auth"])
app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(cart.router,     prefix="/cart",     tags=["Cart"])
app.include_router(orders.router,   prefix="/orders",   tags=["Orders"])


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the E-Commerce API 🛒",
        "docs":    "/docs",
        "redoc":   "/redoc",
    }
