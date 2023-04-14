import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from config import settings 

from incolume.py.fastapi.crud0.server import app 
from incolume.py.fastapi.crud0.db.persistence import recreate_db 

@pytest.fixture(scope="function")
def client() -> Generator:
    recreate_db()
    with TestClient(app) as cliente:
        yield cliente
