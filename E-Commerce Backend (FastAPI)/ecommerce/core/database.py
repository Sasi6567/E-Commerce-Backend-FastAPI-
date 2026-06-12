"""
core/database.py
─────────────────
SQLite database setup via SQLAlchemy.
Switch DATABASE_URL to PostgreSQL/MySQL for production.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite — zero config, perfect for learning/local dev
DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ── Dependency injected into every route that needs DB ───────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
