import pytest
from typing import Generator
from fastapi.testclient import TestClient
from config import settings
from incolume.py.fastapi.crud0.db.connections import get_db_session, Session
from incolume.py.fastapi.crud0.db.persistence import crypt_context
from incolume.py.fastapi.crud0.controllers import utils
from incolume.py.fastapi.crud0.models import UserModel


@pytest.fixture(scope="function")
def client() -> Generator:
    settings.setenv("testing")
    with settings.using_env("testing"):
        from incolume.py.fastapi.crud0.server import app
        from incolume.py.fastapi.crud0.db.persistence import (
            populate_db,
            recreate_db,
            create_admin,
        )

        recreate_db()
        create_admin()
        populate_db()
        with TestClient(app) as cliente:
            yield cliente


@pytest.fixture(scope="module")
def db_session() -> Session:
    return get_db_session()


@pytest.fixture(scope="function")
def one_user() -> None:
    with Session() as db:
        db.add(
            UserModel(
                username="user",
                email="user@example.com",
                full_name="Usuário do Sistema",
                roles=utils.Role.USER,
                pw_hash=crypt_context.hash("aaQQ!!11"),
            )
        )
        db.commit()
