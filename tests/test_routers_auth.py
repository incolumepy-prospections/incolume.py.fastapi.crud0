import pytest
from incolume.py.fastapi.crud0.routers.auth import router


class TestRouterAuth:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            pytest.param('', '', marks=pytest.mark.skip(reason='Not implemented ..')),
        ),
    )
    def test_case1(self, entrance, expected):
        pass