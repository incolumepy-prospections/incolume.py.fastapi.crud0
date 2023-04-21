from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()
engine = create_engine(settings.db_url, pool_pre_ping=True, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session():
    try:
        yield session:=Session()
    finally:
        session.close()

