"""Module for configuration switch tests."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from config import settings
from incolume.py.fastapi.crud0.controllers import utils
from incolume.py.fastapi.crud0.db.connections import Session, get_db_session
from incolume.py.fastapi.crud0.db.persistence import crypt_context
from incolume.py.fastapi.crud0.models import UserModel


@pytest.fixture(scope="function")
def client() -> Generator:
    """Client generator."""
    settings.setenv("testing")
    with settings.using_env("testing"):
        from incolume.py.fastapi.crud0.db.persistence import (
            create_admin,
            populate_db,
            recreate_db,
        )
        from incolume.py.fastapi.crud0.server import app

        recreate_db()
        create_admin()
        populate_db(3)
        with TestClient(app) as cliente:
            yield cliente


@pytest.fixture(scope="module")
def db_session() -> Session:
    """DB generator."""
    return get_db_session()
