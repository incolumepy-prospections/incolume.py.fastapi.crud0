import pytest

from incolume.py.fastapi.crud0.controllers.utils import (
    QueryUser,
    Role,
    Sort,
    ToggleBool,
)


class TestEnumRole:
    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            (Role.USER, "USER"),
            (Role.READER, "READER"),
            (Role.EDITOR, "EDITOR"),
            (Role.PROOFREADER, "PROOFREADER"),
            (Role.MANAGER, "MANAGER"),
            (Role.ADMINISTRATOR, "ADMINISTRATOR"),
        ),
    )
    def test_roles_name(self, entrance, expected):
        assert entrance.name == expected

    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            (Role.USER, 0),
            (Role.READER, 1),
            (Role.EDITOR, 2),
            (Role.PROOFREADER, 4),
            (Role.MANAGER, 8),
            (Role.ADMINISTRATOR, 16),
        ),
    )
    def test_roles_value(self, entrance, expected):
        assert entrance.value == expected

    @pytest.mark.parametrize(
        "entrance1 operator entrance2 expected".split(),
        (
            (Role.USER, '>', Role.READER, False),
            (Role.USER, '>', Role.EDITOR, False),
            (Role.USER, '>', Role.PROOFREADER, False),
            (Role.USER, '>', Role.MANAGER, False),
            (Role.USER, '>', Role.ADMINISTRATOR, False),
            (Role.READER, '>', Role.EDITOR, False),
            (Role.READER, '>', Role.PROOFREADER, False),
            (Role.READER, '>', Role.MANAGER, False),
            (Role.READER, '>', Role.ADMINISTRATOR, False),
            (Role.EDITOR, '>', Role.PROOFREADER, False),
            (Role.EDITOR, '>', Role.MANAGER, False),
            (Role.EDITOR, '>', Role.ADMINISTRATOR, False),
            (Role.PROOFREADER, '>', Role.MANAGER, False),
            (Role.PROOFREADER, '>', Role.ADMINISTRATOR, False),
            (Role.MANAGER, '>', Role.ADMINISTRATOR, False),
            (Role.USER, '<', Role.READER, True),
            (Role.USER, '<', Role.EDITOR, True),
            (Role.USER, '<', Role.PROOFREADER, True),
            (Role.USER, '<', Role.MANAGER, True),
            (Role.USER, '<', Role.ADMINISTRATOR, True),
            (Role.READER, '<', Role.EDITOR, True),
            (Role.READER, '<', Role.PROOFREADER, True),
            (Role.READER, '<', Role.MANAGER, True),
            (Role.READER, '<', Role.ADMINISTRATOR, True),
            (Role.EDITOR, '<', Role.PROOFREADER, True),
            (Role.EDITOR, '<', Role.MANAGER, True),
            (Role.EDITOR, '<', Role.ADMINISTRATOR, True),
            (Role.PROOFREADER, '<', Role.MANAGER, True),
            (Role.PROOFREADER, '<', Role.ADMINISTRATOR, True),
            (Role.MANAGER, '<', Role.ADMINISTRATOR, True),
            pytest.param(Role.USER, 'in', Role.READER, False, marks=pytest.mark.skip),
            pytest.param(Role.USER, 'in', Role.EDITOR, False, marks=pytest.mark.skip),
            pytest.param(Role.USER, 'in', Role.PROOFREADER, False, marks=pytest.mark.skip),
            pytest.param(Role.USER, 'in', Role.MANAGER, False, marks=pytest.mark.skip),
            pytest.param(Role.USER, 'in', Role.ADMINISTRATOR, False, marks=pytest.mark.skip),
            pytest.param(Role.READER, 'in', Role.EDITOR, False, marks=pytest.mark.skip),
            pytest.param(Role.READER, 'in', Role.PROOFREADER, False, marks=pytest.mark.skip),
            pytest.param(Role.READER, 'in', Role.MANAGER, False, marks=pytest.mark.skip),
            pytest.param(Role.READER, 'in', Role.ADMINISTRATOR, False, marks=pytest.mark.skip),
            pytest.param(Role.EDITOR, 'in', Role.PROOFREADER, False, marks=pytest.mark.skip),
            pytest.param(Role.EDITOR, 'in', Role.MANAGER, False, marks=pytest.mark.skip),
            pytest.param(Role.EDITOR, 'in', Role.ADMINISTRATOR, False, marks=pytest.mark.skip),
            pytest.param(Role.PROOFREADER, 'in', Role.MANAGER, False, marks=pytest.mark.skip),
            pytest.param(Role.PROOFREADER, 'in', Role.ADMINISTRATOR, False, marks=pytest.mark.skip),
            pytest.param(Role.MANAGER, 'in', Role.ADMINISTRATOR, False, marks=pytest.mark.skip),
        ),
    )
    def test_roles_major(self, entrance1, operator, entrance2, expected):
        match operator:
            case '>':
                assert (entrance1 > entrance2) == expected
            case '<':
                assert (entrance1 < entrance2) == expected
            case 'in':
                assert (entrance1 in entrance2) == expected


class TestEnumQueryUser:
    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            (QueryUser.USER_ID, "id"),
            (QueryUser.ID, "id"),
            (QueryUser.USER_EMAIL, "email"),
            (QueryUser.EMAIL, "email"),
            (QueryUser.NAME, "username"),
            (QueryUser.USERNAME, "username"),
        ),
    )
    def test_query_user(self, entrance, expected):
        assert entrance.value == expected


class TestSortEnum:
    @pytest.fixture(scope='function')
    def numbers(self):
        return [5, 2, 7, 6, 3, 9, 8, 4]

    def test_ascending(self, numbers):
        assert Sort.ASCENDING(numbers) == [2, 3, 4, 5, 6, 7, 8, 9]

    def test_descending(self, numbers):
        assert Sort.DESCENDING(numbers) == [9, 8, 7, 6, 5, 4, 3, 2]


class TestToggleBool:
    @pytest.mark.parametrize(
        'entrance expected'.split(),
        (
            (ToggleBool.OFF, False),
            (ToggleBool.ON, True),
        )
    )
    def test_values(self, entrance, expected):
        assert entrance.value == expected

    @pytest.mark.parametrize(
        'entrance expected'.split(),
        (
            (ToggleBool.OFF, 'OFF'),
            (ToggleBool.ON, 'ON'),
        )
    )
    def test_name(self, entrance, expected):
        assert entrance.name == expected
