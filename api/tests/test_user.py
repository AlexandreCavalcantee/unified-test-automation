import pytest

from api.data.payloads import user_payload
from api.data.schemas import USER_SCHEMA, assert_schema

pytestmark = pytest.mark.api


class TestUser:
    def _create(self, client, username, user_id):
        response = client.post("/user", json=user_payload(username, user_id))
        assert response.status_code == 200, response.text
        return response.json()

    def test_create_user(self, client, unique_id):
        username = f"user_{unique_id}"

        body = self._create(client, username, unique_id)

        assert body["code"] == 200
        assert body["message"] == str(unique_id)

    def test_get_user_by_username(self, client, unique_id):
        username = f"user_{unique_id}"
        self._create(client, username, unique_id)

        response = client.get(f"/user/{username}")

        assert response.status_code == 200
        body = response.json()
        assert_schema(body, USER_SCHEMA)
        assert body["username"] == username
        assert body["email"] == f"{username}@example.com"

    def test_update_user(self, client, unique_id):
        username = f"user_{unique_id}"
        self._create(client, username, unique_id)
        updated = user_payload(username, unique_id)
        updated["email"] = f"updated_{username}@example.com"

        response = client.put(f"/user/{username}", json=updated)
        assert response.status_code == 200

        get_response = client.get(f"/user/{username}")
        assert get_response.status_code == 200
        assert get_response.json()["email"] == f"updated_{username}@example.com"

    def test_login_returns_session(self, client, unique_id):
        username = f"user_{unique_id}"
        self._create(client, username, unique_id)

        response = client.get(
            "/user/login", params={"username": username, "password": "test123"}
        )

        assert response.status_code == 200
        assert "logged in user session" in response.json()["message"].lower()

    def test_logout(self, client):
        response = client.get("/user/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "ok"

    def test_create_users_with_list(self, client, unique_id):
        users = [
            user_payload(f"batch_{unique_id}_a", unique_id + 1),
            user_payload(f"batch_{unique_id}_b", unique_id + 2),
        ]

        response = client.post("/user/createWithList", json=users)

        assert response.status_code == 200
        assert response.json()["message"] == "ok"

    def test_delete_user(self, client, unique_id):
        username = f"user_{unique_id}"
        self._create(client, username, unique_id)

        delete_response = client.delete(f"/user/{username}")
        assert delete_response.status_code == 200

        get_response = client.get(f"/user/{username}")
        assert get_response.status_code == 404

    def test_get_nonexistent_user_returns_404(self, client, unique_id):
        response = client.get(f"/user/ghost_{unique_id}")

        assert response.status_code == 404
