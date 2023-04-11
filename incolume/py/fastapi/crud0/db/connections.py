from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()
engine = create_engine(settings.db_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

