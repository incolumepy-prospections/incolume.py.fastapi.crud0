import pytest 
from fastapi.testclient import TestClient


class TestAPI:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            ('/', 200),
            ('/users', 202),
            # ('/users/user0001', 202),
        ),
    )
    def test_endpoint_status_code(self, entrance, expected , client: TestClient) -> None:
        response = client.get(entrance)
        print(entrance)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            ('/', 'Ambiente de testes'),
        ),
    )
    def test_endpoint_result(self, entrance, expected, client: TestClient) -> None:
        response = client.get(entrance)
        body = response.json()
        assert body["message"] == expected 
