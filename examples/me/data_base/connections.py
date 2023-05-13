"""Connections module."""
from typing import List

from incolume.py.fastapi.crud2.schemas import Gender, Role, User

db: List[User] = [
    User(
        id="965efc19-15c7-40ef-9167-608ce97c8dad",
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id="4b433115-a723-4c8f-b6ca-d33a6a85f9d5",
        first_name="Jane",
        last_name="Doe",
        gender=Gender.female,
        roles=[Role.user],
    ),
    User(
        id="3146a04e-7db2-4ebc-8191-1380f5824f82",
        first_name="James",
        last_name="Gabriel",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id="54ae226d-1bb4-4c4e-9639-a3305f68d27b",
        first_name="Eunit",
        last_name="Eunit",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]
