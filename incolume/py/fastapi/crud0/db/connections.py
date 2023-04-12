from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()
engine = create_engine(settings.db_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


def create_db(engine:engine):
    Base.metadata.create_all(bind=engine)


def drop_db(engine=engine):
    Base.metadata.drop_all(bind=engine)


def recreate_db(engine=engine):
    drop_db(engine)
    create_db(engine)


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

