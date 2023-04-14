import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from config import settings 

settings.setenv('testing')


@pytest.fixture(scope="function")
def client() -> Generator:
    with settings.using_env('testing'):
        from incolume.py.fastapi.crud0.server import app 
        from incolume.py.fastapi.crud0.db.persistence import recreate_db 

        recreate_db()
        with TestClient(app) as cliente:
            yield cliente
