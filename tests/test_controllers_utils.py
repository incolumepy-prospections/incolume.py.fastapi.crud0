import pytest
from incolume.py.fastapi.crud0.controllers.utils import Role, QueryUser


class TestEnums:
    @pytest.mark.parametrize(
        'entrance expected'.split(),
        (
            (Role.USER, 'USER'),
            (Role.READER, 'READER'),
            (Role.EDITOR, 'EDITOR'),
            (Role.PROOFREADER, 'PROOFREADER'),
            (Role.ADMINISTRATOR, 'ADMINISTRATOR'),
        ),
    )
    def test_roles_value(self, entrance, expected):
        assert entrance.name == expected

    @pytest.mark.parametrize(
        'entrance expected'.split(),
        (
            (QueryUser.USER_ID, 'ID'),
            (QueryUser.ID, 'ID'),
            (QueryUser.USER_EMAIL, 'EMAIL'),
            (QueryUser.EMAIL, 'EMAIL'),
            (QueryUser.NAME, 'USERNAME'),
            (QueryUser.USERNAME, 'USERNAME'),
        ),
    )
    def test_query_user(self, entrance, expected):
        assert entrance.name == expected
