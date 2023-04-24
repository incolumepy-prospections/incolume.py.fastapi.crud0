import pytest
from incolume.py.fastapi.crud0.controllers.user import User


class TestCrlUser:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_create(self, entrance, expected):
        pass

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_read_by_id(self, entrance, expected):
        pass
    
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_read_by_username(self, entrance, expected):
        pass
    
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_read_by_email(self, entrance, expected):
        pass
    
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_update(self, entrance, expected):
        pass
    
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_delete(self, entrance, expected):
        pass
