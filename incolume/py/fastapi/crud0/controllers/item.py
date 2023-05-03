import logging
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from incolume.py.fastapi.crud0.schemas import Item, ItemCreate
from incolume.py.fastapi.crud0.db.connections import Session
from incolume.py.fastapi.crud0.models import ItemModel


class Item:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create(self, item: ItemCreate) -> ItemModel:
        item_model = ItemModel(**item.dict())
        try:
            self.db_session.add(item)
            self.db_session.commit()
            self.db_session.reflash(item)
        except IntegrityError as e:
            logging.error(e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.",
            )
        return item_model

    def list(self, item: Item):
        pass

    def update(self, item: Item):
        pass

    def delete(self, item: Item):
        pass
