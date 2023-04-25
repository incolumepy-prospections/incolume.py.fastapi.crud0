import pytest
from incolume.py.fastapi.crud0.controllers.auth import Auth, AuthOTP



class TestCrlAuth:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_case1(self, entrance, expected):
        pass


class TestCrlAuthOTP:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_case1(self, entrance, expected):
        pass