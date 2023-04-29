from incolume.py.fastapi.crud0.models import UserModel
from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.db.connections import (
    Base,
    engine,
    Session,
    get_db_session,
)
from passlib.context import CryptContext


crypt_context = CryptContext(schemes=["sha256_crypt"])


def create_db(engine: engine = engine):
    Base.metadata.create_all(bind=engine)


def drop_db(engine: engine = engine):
    Base.metadata.drop_all(bind=engine)


def recreate_db(engine: engine = engine):
    drop_db(engine)
    create_db(engine)


def create_admin(engine: engine = engine):
    with Session() as db:
        admin_user = UserModel(
            username="admin",
            email="admin@example.com",
            full_name="Administrador do Sistema",
            is_admin=True,
            pw_hash=crypt_context.hash("aaQQ!!11"),
        )
        db.add(admin_user)
        db.commit()
    return True


def populate_db(quantia: int = 10):
    db = Session()
    fake_user_list = [
        UserModel(
            username=f"user{x:04}",
            email=f"user{x:04}@example.com",
            full_name=f"string {x:04}",
            pw_hash=crypt_context.hash("aaQQ!!11"),
        )
        for x in range(1, quantia + 1)
    ]

    db.add_all(fake_user_list)
    db.commit()
    db.close()


if __name__ == "__main__":
    recreate_db()
    populate_db()
