import logging
from config import settings
from incolume.py.fastapi.crud0.server import app


logging.basicConfig(level=logging.DEBUG, format=settings.log_format)
