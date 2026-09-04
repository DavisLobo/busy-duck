from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from busy_duck.database.models.base import Base
from busy_duck.database.models import account_model, calendar_model, event_model, provider_model


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_DIRECTORY = PROJECT_ROOT / "database"
DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIRECTORY / "busy_duck.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def initialize_database() -> None:
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()