"""
ImaraFund Database Configuration
SQLAlchemy setup optimized for the matching algorithm
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database engine with SQLite optimization
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Database dependency for FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ ImaraFund database tables created successfully!")


def drop_all_tables():
    """Development helper - use with caution!"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped!")