from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session



DATABASE_DIRECTORY = Path("database")
DATABASE_DIRECTORY.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIRECTORY / "busy_duck.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()