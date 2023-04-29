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
            (QueryUser.USER_ID, 'id'),
            (QueryUser.ID, 'id'),
            (QueryUser.USER_EMAIL, 'email'),
            (QueryUser.EMAIL, 'email'),
            (QueryUser.NAME, 'username'),
            (QueryUser.USERNAME, 'username'),
        ),
    )
    def test_query_user(self, entrance, expected):
        assert entrance.value == expected
