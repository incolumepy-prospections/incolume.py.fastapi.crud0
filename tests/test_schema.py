import re
import pytest
from incolume.py.fastapi.crud0 import schemas


class TestSchema:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param(
                schemas.Item(title='', id=0, owner_id=0), {}, 
                marks=pytest.mark.skip(reason='Not implemented ..')
            ),
            pytest.param(
                schemas.AccessToken(access_token='', expiration='', type=''), 
                {'access_token': '', 'expiration': '', 'type': ''}
            ),
            pytest.param(
                schemas.ItemBase(title='', description=''), {'title': '', 'description': ''}
            ),
            pytest.param(schemas.ItemBase(title=''), {'title': '', 'description': None}),
            pytest.param(schemas.ItemCreate(title=''), {'title': '', 'description': None}),
            pytest.param(schemas.ItemCreate(title='', description=''), {'title': '', 'description': ''}),
            pytest.param(schemas.Item(title='', id=0, owner_id=0), {'title': '', 'description': None, 'id': 0, 'owner_id': 0}),
            pytest.param(
                schemas.UserBase(username='', password=''), 
                {'username': '', 'email': None, 'full_name': None}
            ),
            pytest.param(
                schemas.UserIn(username='user_001', password='AaQq!1!1'), 
                {'username': 'user_001', 'email': None, 'full_name': None, 'password': 'AaQq!1!1'}
            ),
            pytest.param(
                schemas.UserOut(username='aaa', password='aaa', full_name='aaa', pw_hash='aaa'), 
                {'username': 'aaa', 'email': 'aaa', 'full_name': 'aaa', 'pw_hash': 'aaa'},
                marks=pytest.mark.skip(reason='Error several'),
            ),
            pytest.param(
                schemas.UserInDB(username='', password=''), 
                {'username': '', 'email': None, 'full_name': None, 'pw_hash': ''}
            ),
        ),
    )
    def test_instancia(self, entrance, expected):
        assert entrance.__dict__ == expected


    @pytest.mark.parametrize(
        ['schema', 'entrance', 'exc', 'match'],
        (
            pytest.param(
                schemas.UserIn, 
                {'username': 'user_001'}, 
                ValueError, 
                re.escape('1 validation error for UserIn\npassword\n  field required (type=value_error.missing)') 
            ),
            pytest.param(
                schemas.UserIn, 
                {'password': 'AaQq!1!1'}, 
                ValueError, 
                re.escape('1 validation error for UserIn\nusername\n  field required (type=value_error.missing)')
            ),
            pytest.param(
                schemas.UserIn,
                {'password': 'AaQq!1!1'}, 
                ValueError, 
                re.escape('1 validation error for UserIn\nusername\n  field required (type=value_error.missing)')
            ), 
            pytest.param(
                schemas.UserIn,
                {'username': 'User', 'password': 'AaQq!1!1'}, 
                ValueError, 
                re.escape('1 validation error for UserIn\nusername\n  Invalide format for username (type=value_error)')
            ),
            pytest.param(
                schemas.UserIn,
                {'username': 'user_001', 'password': 'AaQabc'}, 
                ValueError, 
                re.escape('1 validation error for UserIn\npassword\n  Invalide format for password (type=value_error)')
            ),
            pytest.param(
                schemas.UserIn,
                {'username': 'User_01', 'password': 'AaQabc'}, 
                ValueError, 
                re.escape('2 validation errors for UserIn\nusername\n  Invalide format for username (type=value_error)\npassword\n  Invalide format for password (type=value_error)')
            ),
        ),
    )
    def test_exceptions(self, schema, entrance, exc, match):
        with pytest.raises(exc, match=match) as e:
            schema(**entrance)
