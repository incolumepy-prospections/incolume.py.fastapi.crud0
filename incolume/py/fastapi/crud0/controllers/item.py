"""Module controllers.item."""
import inspect
import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from incolume.py.fastapi.crud0.db.connections import Session
from incolume.py.fastapi.crud0.models import ItemModel
from incolume.py.fastapi.crud0.schemas import Item, ItemCreate


class Item:
    """Class Item."""

    def __init__(self, db_session: Session) -> None:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        self.db_session = db_session

    def create(self, item: ItemCreate) -> ItemModel:
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
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
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        pass

    def update(self, item: Item):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        pass

    def delete(self, item: Item):
        """Run {}.{}.""".format(self.__class__.__name__, inspect.stack()[0][3])
        pass
