import pytest 
from fastapi.testclient import TestClient

@pytest.mark.parametrize(
    ['entrance', 'expected'],
    (
        ('/', 200),
    ),
)
def test_endpoint_status_code(entrance, expected , client: TestClient) -> None:
    response = client.get(entrance)
    assert response.status_code == expected

@pytest.mark.parametrize(
    ['entrance', 'expected'],
    (
        ('/', 'Ambiente de testting!'),
    ),
)
def test_endpoint_result(entrance, expected, client: TestClient) -> None:
    response = client.get(entrance)
    body = response.json()
    assert body["mensagem"] == expected 
