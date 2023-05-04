import re
import pytest
from incolume.py.fastapi.crud0 import schemas


class TestSchema:
    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param(
                schemas.Item(
                    title="",
                    id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    owner_id=0,
                ),
                {},
                marks=pytest.mark.skip(reason="Not implemented .."),
            ),
            pytest.param(
                schemas.AccessToken(access_token="", expiration="", type=""),
                {"access_token": "", "expiration": "", "type": ""},
            ),
            pytest.param(
                schemas.ItemBase(title="", description=""),
                {"title": "", "description": ""},
                marks=pytest.mark.skip,
            ),
            pytest.param(
                schemas.ItemBase(title=""),
                {"title": "", "description": None},
                marks=pytest.mark.skip,
            ),
            pytest.param(
                schemas.ItemCreate(title=""),
                {"title": "", "description": None},
                marks=pytest.mark.skip,
            ),
            pytest.param(
                schemas.ItemCreate(title="", description=""),
                {"title": "", "description": ""},
                marks=pytest.mark.skip,
            ),
            pytest.param(
                schemas.Item(
                    title="",
                    id="3fa85f64-5717-4562-b3fc-2c963f66afa9",
                    owner_id=0,
                ),
                {
                    "title": "",
                    "description": "",
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                    "owner_id": 0,
                },
                marks=pytest.mark.skip,
            ),
            pytest.param(
                schemas.UserBase(username="aaa", password=""),
                {
                    "username": "aaa",
                    "email": None,
                    "full_name": None,
                    "roles": 0,
                    "is_active": True,
                },
            ),
            pytest.param(
                schemas.UserIn(username="user_001", password="AaQq!1!1"),
                {
                    "username": "user_001",
                    "email": None,
                    "full_name": None,
                    "roles": 0,
                    "is_active": True,
                    "password": "AaQq!1!1",
                },
            ),
            pytest.param(
                schemas.UserOut(
                    username="aaa",
                    password="aaa",
                    full_name="AAAA AA AAAAAA",
                    pw_hash="aaa",
                ),
                {
                    "username": "aaa",
                    "email": "aaa",
                    "roles": 0,
                    "full_name": "aaa",
                    "pw_hash": "aaa",
                },
                marks=pytest.mark.skip(reason="Error several"),
            ),
            pytest.param(
                schemas.UserInDB(username="aaa", password="aaQQ!!11"),
                {
                    "username": "aaa",
                    "email": None,
                    "full_name": None,
                    "pw_hash": "aaQQ!!11",
                    "roles": 0,
                    "is_active": True,
                },
            ),
            pytest.param(
                schemas.UserCreate(username="aaa", password="aaQQ!!11"),
                {
                    "username": "aaa",
                    "email": None,
                    "full_name": None,
                    "password": "aaQQ!!11",
                    "roles": 0,
                    "is_active": True,
                },
            ),
        ),
    )
    def test_instancia(self, entrance, expected):
        assert entrance.__dict__ == expected

    @pytest.mark.parametrize(
        ["schema", "entrance", "exc", "match"],
        (
            pytest.param(
                schemas.UserIn,
                {"username": "user_001"},
                ValueError,
                re.escape(
                    "1 validation error for UserIn\npassword\n  field required (type=value_error.missing)"
                ),
            ),
            pytest.param(
                schemas.UserIn,
                {"password": "AaQq!1!1"},
                ValueError,
                re.escape(
                    "1 validation error for UserIn\nusername\n  field required (type=value_error.missing)"
                ),
            ),
            pytest.param(
                schemas.UserIn,
                {"password": "AaQq!1!1"},
                ValueError,
                re.escape(
                    "1 validation error for UserIn\nusername\n  field required (type=value_error.missing)"
                ),
            ),
            pytest.param(
                schemas.UserIn,
                {"username": "User", "password": "AaQq!1!1"},
                ValueError,
                re.escape(
                    "1 validation error for UserIn\nusername\n  Invalide format for username (type=value_error)"
                ),
            ),
            pytest.param(
                schemas.UserIn,
                {"username": "user_001", "password": "AaQabc"},
                ValueError,
                re.escape(
                    "1 validation error for UserIn\npassword\n  ensure this "
                    "value has at least 8 characters (type=value_error."
                    "any_str.min_length; limit_value=8)"
                ),
            ),
            pytest.param(
                schemas.UserIn,
                {"username": "User_01", "password": "AaQabc"},
                ValueError,
                re.escape(
                    "2 validation errors for UserIn\nusername\n  Invalide"
                    " format for username (type=value_error)\npassword\n  "
                    "ensure this value has at least 8 characters (type=value_"
                    "error.any_str.min_length; limit_value=8)"
                ),
            ),
        ),
    )
    def test_exceptions(self, schema, entrance, exc, match):
        with pytest.raises(exc, match=match) as e:
            schema(**entrance)
