"""Module connections."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

Base = declarative_base()
engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session():
    """Database session generate."""
    session = Session()
    try:
        yield session
    finally:
        session.close()
