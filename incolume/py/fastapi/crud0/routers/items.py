from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from incolume.py.fastapi.crud0.db.connections import get_db_session
from incolume.py.fastapi.crud0 import schemas
from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.controllers.item import Item
from incolume.py.fastapi.crud0.models import ItemModel

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Item, summary="Create an Item")
def create_item(item: schemas.Item, session = Depends(get_db_session)):
    new_item: ItemModel = Item(session).create(item=item)
    return new_item