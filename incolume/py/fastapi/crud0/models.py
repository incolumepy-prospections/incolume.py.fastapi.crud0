from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from incolume.py.fastapi.crud0.db.connections import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    username = Column('username', String, nullable=False, unique=True, index=True)
    pw_hash = Column('pw_hash', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True, index=True)
    full_name = Column('full_name', String, nullable=False)
    is_active = Column(Boolean, default=True)
    items = relationship("ItemModel", back_populates="owner")


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="items")