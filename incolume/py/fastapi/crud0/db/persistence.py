"""Module persistence."""

from passlib.context import CryptContext

from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers import utils
from incolume.py.fastapi.crud0.db.connections import (
    Base,
    Session,
    engine,
    get_db_session,
)
from incolume.py.fastapi.crud0.models import UserModel

crypt_context = CryptContext(schemes=["sha256_crypt"])


def create_db(engine: engine = engine):
    """Create database."""
    Base.metadata.create_all(bind=engine)


def drop_db(engine: engine = engine):
    """Drop database."""
    Base.metadata.drop_all(bind=engine)


def recreate_db(engine: engine = engine):
    """Recreate database."""
    drop_db(engine)
    create_db(engine)


def create_admin(engine: engine = engine):
    """Create admin user."""
    with Session() as db_session:
        admin_user = UserModel(
            username="admin",
            email="admin@example.com",
            full_name="Administrador do Sistema",
            roles=utils.Role.ADMINISTRATOR,
            pw_hash=crypt_context.hash("aaQQ!!11"),
        )
        db_session.add(admin_user)
        db_session.commit()
    return True


def populate_db(quantia: int = 10):
    """Populate database with fake users."""
    db_session = Session()
    fake_user_list = [
        UserModel(
            username=f"user{x:04}",
            email=f"user{x:04}@example.com",
            full_name=f"User{x:04} do Sistema",
            roles=utils.Role.USER,
            pw_hash=crypt_context.hash("aaQQ!!11"),
        )
        for x in range(1, quantia + 1)
    ]

    db_session.add_all(fake_user_list)
    db_session.commit()
    db_session.close()


if __name__ == "__main__":
    recreate_db()
    populate_db()
