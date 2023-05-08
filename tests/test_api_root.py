import pytest
from fastapi.testclient import TestClient


class TestAPI:
    @pytest.mark.parametrize(
        "endpoint status json_data expected".split(),
        (
            # pytest.param('/users', 422, {"username": "user", "email": "user@example.com", "full_name": "Administrador do Sistema"}, {'detail': [{'loc': ['body', 'username'], 'msg': 'Invalide format for username', 'type': 'value_error'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]}, marks=''),
            pytest.param(
                "/users",
                422,
                {
                    "username": "user_002",
                    "email": "user02@example.com",
                    "full_name": "Usuário do Sistema",
                },
                {
                    "detail": [
                        {
                            "loc": ["body", "password"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ]
                },
                # marks=pytest.mark.skip
            ),
            pytest.param(
                "/users",
                201,
                {
                    "username": "user_003",
                    "password": "aaQQ1!1!",
                    "email": "user03@example.com",
                    "full_name": "Usuário do Sistema",
                },
                {
                    "username": "user_003",
                    "email": "user03@example.com",
                    "full_name": "Usuário do Sistema",
                    "is_active": True,
                    "roles": 0,
                },
                # marks=pytest.mark.skip
            ),
            pytest.param(
                '/users', 
                201, 
                {"username": "user", "email": "user@example.com", "password": "aaQQ1!1!", "full_name": "Usuário do Sistema"}, 
                {'username': 'user', 'email': 'user@example.com', 'full_name': 'Usuário do Sistema', 'roles': 0, 'is_active': True},
                # marks=pytest.mark.skip
            ),
            pytest.param(
                '/users', 
                409, 
                {"username": "user0001", "email": "xpto@example.com", "password": "aaQQ1!1!", "full_name": "Usuário do Sistema"}, 
                {"detail":"User already exists. E-mail:'xpto@example.com' and/or username: 'user0001' already registered."},
                # marks=pytest.mark.skip
            ),
            pytest.param(
                '/users', 
                409, 
                {"username": "xpto", "email": "user0001@example.com", "password": "aaQQ1!1!", "full_name": "Usuário do Sistema"}, 
                {"detail":"User already exists. E-mail:'user0001@example.com' and/or username: 'xpto' already registered."},
                # marks=pytest.mark.skip
            ),
        ),
    )
    def test_post_endpoint_result(
        self, endpoint, json_data, status, expected, client: TestClient
    ) -> None:
        """Test for result post on endpoints."""
        response = client.post(endpoint, json=json_data)
        assert response.status_code == status, response.text

        result = response.json()
        assert result == expected

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param("/", 200),
            pytest.param("/doc", 200),
            pytest.param("/favicon.ico", 200),
            pytest.param("/users", 202),
            pytest.param("/users/1", 202, marks=""),
            pytest.param("/users/admin?q=username", 202, marks=""),
            pytest.param("/users/admin%40example.com?q=email", 202),
            pytest.param("/users/1?q=username", 404, marks=""),
            pytest.param("/users/1?q=user", 422, marks=""),
            pytest.param("/users/user0001", 404, marks=""),
            pytest.param("/users/user0101%40example.com?q=email", 404),
        ),
    )
    def test_get_endpoint_status_code(
        self, entrance, expected, client: TestClient
    ) -> None:
        """Test for status_code post on endpoints."""
        response = client.get(entrance)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        ["entrance", "expected"],
        (
            pytest.param("/", {"message": "Ambiente de testes"}),
            pytest.param(
                "/users",
                [
                    {
                        "username": "admin",
                        "email": "admin@example.com",
                        "full_name": "Administrador do Sistema",
                        "is_active": True,
                        "roles": 16,
                    },
                    {
                        "username": "user0001",
                        "email": "user0001@example.com",
                        "full_name": "User0001 do Sistema",
                        "is_active": True,
                        "roles": 0,
                    },
                    {
                        "username": "user0002",
                        "email": "user0002@example.com",
                        "full_name": "User0002 do Sistema",
                        "is_active": True,
                        "roles": 0,
                    },
                    {
                        "username": "user0003",
                        "email": "user0003@example.com",
                        "full_name": "User0003 do Sistema",
                        "is_active": True,
                        "roles": 0,
                    },
                ],
            ),
            pytest.param(
                "/users/1",
                {
                    "email": "admin@example.com",
                    "full_name": "Administrador do Sistema",
                    "username": "admin",
                    "is_active": True,
                    "roles": 16,
                },
                marks="",
            ),
            pytest.param(
                "/users/admin?q=username",
                {
                    "email": "admin@example.com",
                    "full_name": "Administrador do Sistema",
                    "username": "admin",
                    "is_active": True,
                    "roles": 16,
                },
                marks="",
            ),
            pytest.param(
                "/users/admin%40example.com?q=email",
                {
                    "email": "admin@example.com",
                    "full_name": "Administrador do Sistema",
                    "username": "admin",
                    "is_active": True,
                    "roles": 16,
                },
            ),
            pytest.param(
                "/users/1?q=username", {"detail": "User not found."}, marks=""
            ),
            pytest.param(
                "/users/1?q=user",
                {
                    "detail": [
                        {
                            "ctx": {
                                "enum_values": ["email", "id", "username"]
                            },
                            "loc": ["query", "q"],
                            "msg": "value is not a valid enumeration member; permitted: 'email', 'id', 'username'",
                            "type": "type_error.enum",
                        }
                    ]
                },
                marks="",
            ),
            pytest.param(
                "/users/user0001", {"detail": "User not found."}, marks=""
            ),
            pytest.param(
                "/users/user0101%40example.com?q=email",
                {"detail": "User not found."},
            ),
        ),
    )
    def test_get_endpoint_result(
        self, entrance, expected, client: TestClient
    ) -> None:
        response = client.get(entrance)
        body = response.json()
        assert body == expected

    @pytest.mark.parametrize(
        "endpoint status json_data expected".split(),
        (
            pytest.param(
                "/users/user0001",
                404,
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    "full_name": "Administrador do Sistema",
                },
                {"detail": "User not found."},
                # marks=pytest.mark.skip
            ),
            pytest.param(
                "/users/1?q=id",
                409,
                {
                    "username": "user0001",
                    "email": "admin@example.com",
                    "full_name": "Administrador do Sistema",
                },
                {
                    "detail": "'user0001' or 'admin@example.com' already registered."
                },
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                "/users/user0001?q=username",
                202,
                {
                    "username": "user0001",
                    "email": "fake@example.com",
                    "full_name": "fake@example.com",
                },
                {
                    "username": "user0001",
                    "email": "fake@example.com",
                    "full_name": "fake@example.com",
                    "is_active": True,
                    "roles": 0,
                },
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                "users/admin?q=username",
                202,
                {
                    "username": "admin",
                    "email": "admin@acme.com",
                    "full_name": "Administrador da API (Aplication Program Interface).",
                },
                {
                    "username": "admin",
                    "email": "admin@acme.com",
                    "full_name": "Administrador da API (Aplication Program Interface).",
                    "is_active": True,
                    "roles": 16,
                },
                # marks=pytest.mark.skip,
            ),
            pytest.param(
                "/users/user0001?q=username",
                202,
                {
                    "username": "user0001",
                    "email": "fake@example.com",
                    "full_name": "fake@example.com",
                },
                {
                    "username": "user0001",
                    "email": "fake@example.com",
                    "full_name": "fake@example.com",
                    "is_active": True,
                    "roles": 0,
                },
                # marks=pytest.mark.skip,
            ),
        ),
    )
    def test_put_endpoint_result(
        self, endpoint, status, json_data, expected, client: TestClient
    ) -> None:
        # print(client.get('/users').json())
        response = client.put(endpoint, json=json_data)
        assert response.status_code == status, response.text

        result = response.json()
        assert result == expected

    @pytest.mark.parametrize(
        "entrance status expected".split(),
        (
            pytest.param(
                "/users/xpto?q=username",
                404,
                {"detail": "User not found."},
                # marks=pytest.mark.skip(reason="Not implemented!"),
            ),
            pytest.param(
                "/users/xpto?q=id",
                404,
                {"detail": "User not found."},
                # marks=pytest.mark.skip(reason="Not implemented!"),
            ),
            pytest.param(
                "/users/xpto?q=email",
                404,
                {"detail": "User not found."},
                # marks=pytest.mark.skip(reason="Not implemented!"),
            ),
            pytest.param(
                "/users/xpto@example.com?q=username",
                404,
                {"detail": "User not found."},
                # marks=pytest.mark.skip(reason="Not implemented!"),
            ),
            pytest.param(
                "/users/1",
                202,
                {
                    "username": "admin",
                    "roles": 16,
                    "email": "admin@example.com",
                    "id": 1,
                    "full_name": "Administrador do Sistema",
                    "is_active": True,
                },
                # marks=pytest.mark.skip(reason="Not implemented!"),
            ),
        ),
    )
    def test_delete_endpoint_result(
        self,
        entrance,
        status,
        expected,
        client: TestClient,
    ) -> None:
        """Test endpoint delete."""

        response = client.delete(entrance)
        assert response.status_code == status

        result = response.json()
        assert expected.items() <= result.items()
