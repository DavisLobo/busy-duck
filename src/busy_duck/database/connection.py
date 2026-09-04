from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from busy_duck.database.models.base import Base

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_DIRECTORY = PROJECT_ROOT / "data"
DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

ENGINE = create_engine(f"sqlite:///{DATABASE_DIRECTORY / 'busy_duck.db'}")
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


def initialize_database() -> None:
    Base.metadata.create_all(bind=ENGINE)


def get_session() -> Session:
    return SessionLocal()