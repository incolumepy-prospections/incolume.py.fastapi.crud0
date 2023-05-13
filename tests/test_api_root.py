import pytest
from fastapi.testclient import TestClient


class TestAPI:
    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param("/", 200),
            pytest.param("/doc", 200),
            pytest.param("/favicon.ico", 200),
        ),
    )
    def test_get_endpoint_status_code(
        self, entrance, expected, client: TestClient
    ) -> None:
        """Test for status_code post on endpoints."""
        response = client.get(entrance)
        assert response.status_code == expected
