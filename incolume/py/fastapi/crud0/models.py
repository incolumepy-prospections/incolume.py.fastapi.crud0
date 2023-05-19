"""Module models."""

import datetime as dt
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from .controllers.utils import Role
from .db.connections import Base
from uuid import UUID, uuid4


class UserModel(Base):
    """Data model user."""

    __tablename__ = "users"
    id = Column(
        "id",
        UUID,
        primary_key=True,
        nullable=False,
        index=True,
        server_default=uuid4,
    )
    username = Column(
        "username", String, nullable=False, unique=True, index=True
    )
    pw_hash = Column("pw_hash", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True, index=True)
    full_name = Column("full_name", String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    create_at = Column(DateTime, default=dt.datetime.utcnow)
    update_at = Column(DateTime, default=dt.datetime.utcnow)
    roles = Column("roles", Integer, default=Role.USER)
    items = relationship("ItemModel", back_populates="owner")

    def __str__(self):
        """Over writing __str__."""
        return (
            f"UserModel(id={self.id}, username={self.username}, "
            f"email={self.email}, is_active={self.is_active}, "
            f"roles={self.roles})"
        )


class ItemModel(Base):
    """Data model Item."""

    __tablename__ = "items"

    id = Column("id", UUID, primary_key=True, index=True)
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
