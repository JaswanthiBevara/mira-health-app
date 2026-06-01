"""
database.py
───────────
MySQL connection setup using SQLAlchemy.
Reads credentials from .env via python-dotenv.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env file
load_dotenv()

# ── Build connection URL ──────────────────────────────────────────────────────
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "mira_db")
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

from urllib.parse import quote_plus

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── SQLAlchemy engine & session ───────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Auto-reconnect if MySQL drops idle connection
    echo=False,           # Set True to see raw SQL in terminal (debug only)
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# All ORM models will inherit from this base
Base = declarative_base()


# ── Dependency for FastAPI routes ─────────────────────────────────────────────
def get_db():
    """
    Yields a DB session per request, closes it after.
    Use as: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
