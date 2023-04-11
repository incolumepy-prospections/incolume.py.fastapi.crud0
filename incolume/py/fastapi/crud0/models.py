from sqlalchemy import Column, String, Integer
from incolume.py.fastapi.crud0.db.connections import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column('username', String, nullable=False, unique=True)
    pw_hash = Column('pw_hash', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
