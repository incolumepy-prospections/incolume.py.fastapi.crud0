import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from config import settings 
from incolume.py.fastapi.crud0.db.connections import get_db_session, Session
from incolume.py.fastapi.crud0.db.persistence import populate_db


settings.setenv('testing')


@pytest.fixture(scope="function")
def client() -> Generator:
    with settings.using_env('testing'):
        from incolume.py.fastapi.crud0.server import app 
        from incolume.py.fastapi.crud0.db.persistence import recreate_db 

        # populate_db(30)
        with TestClient(app) as cliente:
            yield cliente


@pytest.fixture(scope="module")
def db_session() -> Session:
    return get_db_session()