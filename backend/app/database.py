from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


# ---- Engine ----
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # reconnect on stale connections
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,      # print SQL in debug mode
)

# ---- Session factory ----
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ---- Base class for all models ----
class Base(DeclarativeBase):
    pass


# ---- Dependency for FastAPI routes ----
def get_db():
    """Yield a database session, close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
