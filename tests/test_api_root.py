import pytest 
from fastapi.testclient import TestClient


class TestAPI:
    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        (
            ('/', 200),
            ('/users', 202),
            pytest.param('/users/{username_or_email: str}?username_or_email=user0001', 202, marks=pytest.mark.skip(reason='Error on input data ..')),
            pytest.param('/users/{username_or_email: str}?username_or_email=user0001%40example.com', 202, marks=pytest.mark.skip(reason='Error on input data ..')),
            ('/users/{username_or_email: str}?username_or_email=user0101%40example.com', 404),
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
