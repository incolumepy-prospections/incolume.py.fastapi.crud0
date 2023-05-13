from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

DB_URL = settings.db_url

engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
