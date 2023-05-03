import pytest
from incolume.py.fastapi.crud0.db.connections import Session
from incolume.py.fastapi.crud0.controllers.user import User
from incolume.py.fastapi.crud0.models import UserModel
from incolume.py.fastapi.crud0.schemas import UserIn


class TestCrlUser:
    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param(
                UserIn(username="user_001", password="AaQq!1!1"),
                "",
                marks=pytest.mark.skip,
            ),
        ),
    )
    def test_create(self, entrance, expected, db_session: Session):
        user = User(db_session).create(user=entrance)
        assert isinstance(user, UserModel)

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param("", ""),
        ),
    )
    def test_read_by_id(self, entrance, expected):
        pass

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param("", ""),
        ),
    )
    def test_read_by_username(self, entrance, expected):
        pass

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param("", ""),
        ),
    )
    def test_read_by_email(self, entrance, expected):
        pass

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param("", ""),
        ),
    )
    def test_update(self, entrance, expected):
        pass

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                "", "", marks=pytest.mark.skip(reason="Not implemented ..")
            ),
            pytest.param("", ""),
        ),
    )
    def test_delete(self, entrance, expected):
        pass
