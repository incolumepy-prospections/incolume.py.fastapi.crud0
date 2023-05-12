import datetime as dt

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from .controllers.utils import Role
from .db.connections import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(
        "id",
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        index=True,
    )
    username = Column(
        "username", String, nullable=False, unique=True, index=True
    )
    pw_hash = Column("pw_hash", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True, index=True)
    full_name = Column("full_name", String, nullable=False)
    is_active = Column(Boolean, default=True)
    roles = Column("roles", Integer)
    items = relationship("ItemModel", back_populates="owner")

    def __str__(self):
        return f"UserModel(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active}, roles={self.roles})"


class ItemModel(Base):
    __tablename__ = "items"

    id = Column("id", String, primary_key=True, index=True)
    title = Column("title", String, index=True)
    description = Column("description", String, index=True)
    created = Column(
        "created", DateTime(timezone=False), default=dt.datetime.utcnow
    )
    updated = Column(
        DateTime(timezone=False),
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,
    )
    owner_id = Column("owner_id", Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="items")
