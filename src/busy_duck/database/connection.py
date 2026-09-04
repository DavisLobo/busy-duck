from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from busy_duck.config import settings
from busy_duck.database.models.base import Base

database_path = Path(settings.DB_PATH)
database_path.parent.mkdir(parents=True, exist_ok=True)

ENGINE = create_engine(
    f"sqlite:///{database_path}",
    future=True,
)

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False,
)


def initialize_database() -> None:
    Base.metadata.create_all(bind=ENGINE)


def get_session() -> Session:
    return SessionLocal()