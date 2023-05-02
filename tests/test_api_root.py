import pytest
from fastapi.testclient import TestClient


class TestAPI:
    @pytest.mark.parametrize(
        'endpoint status json_data expected'.split(),
        (
            # pytest.param('/users', 422, {"username": "user", "email": "user@example.com", "full_name": "Administrador do Sistema"}, {'detail': [{'loc': ['body', 'username'], 'msg': 'Invalide format for username', 'type': 'value_error'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]}, marks=''),
            pytest.param(
                '/users', 
                422, 
                {"username": "user_002", "email": "user02@example.com", "full_name": "Usuário do Sistema"},
                {'detail': [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]},
                # marks=pytest.mark.skip
            ),
            pytest.param(
                '/users', 
                201, 
                {"username": "user_003", 'password': 'aaQQ1!1!', "email": "user03@example.com", "full_name": "Usuário do Sistema"},
                {'username': 'user_003', 'email': 'user03@example.com', 'full_name': 'Usuário do Sistema', 'is_active': True},
                # marks=pytest.mark.skip
            ),
            pytest.param(
                "/users/{username_or_email: str}?username_or_email=user0101%40example.com",
                404,
            ),
            pytest.param("/", 200),
        ),
    )
    def test_get_endpoint_status_code(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.get(entrance)
        # print(entrance)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (("/", "Ambiente de testes"),),
    )
    def test_get_endpoint_result(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.get(entrance)
        body = response.json()
        assert body["message"] == expected

    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            pytest.param(
                "/",
                "Ambiente de testes",
                marks=pytest.mark.skip(reason="Not implemented!"),
            ),
        ),
    )
    def test_delete_endpoint_result(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.delete(entrance)
        assert response.status_code == 204

        result = response.json()
        assert result["detail"] == expected

    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            pytest.param(
                "/",
                "Ambiente de testes",
                marks=pytest.mark.skip(reason="Not implemented!"),
            ),
        ),
    )
    def test_post_endpoint_result(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.post(entrance)
        assert response.status_code == 202

        result = response.json()
        assert result["detail"] == expected

    @pytest.mark.parametrize(
        "entrance expected".split(),
        (
            pytest.param(
                "/",
                "Ambiente de testes",
                marks=pytest.mark.skip(reason="Not implemented!"),
            ),
        ),
    )
    def test_put_endpoint_result(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.put(entrance)
        assert response.status_code == 202

        result = response.json()
        assert result["detail"] == expected
