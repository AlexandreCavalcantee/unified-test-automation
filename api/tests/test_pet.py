import pytest

from api.data.payloads import pet_payload
from api.data.schemas import PET_SCHEMA, assert_schema

pytestmark = pytest.mark.api


class TestPet:
    def _create(self, client, pet_id):
        response = client.post("/pet", json=pet_payload(pet_id))
        assert response.status_code == 200, response.text
        return response.json()

    def test_create_pet(self, client, unique_id):
        body = self._create(client, unique_id)

        assert_schema(body, PET_SCHEMA)
        assert body["id"] == unique_id
        assert body["name"] == "Rex"
        assert body["status"] == "available"
        assert body["category"]["name"] == "dogs"

    def test_get_pet_by_id(self, client, unique_id):
        self._create(client, unique_id)

        response = client.get(f"/pet/{unique_id}")

        assert response.status_code == 200
        assert response.json()["id"] == unique_id

    def test_update_pet(self, client, unique_id):
        self._create(client, unique_id)
        updated = pet_payload(unique_id, name="Rex Updated", status="sold")

        response = client.put("/pet", json=updated)

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Rex Updated"
        assert body["status"] == "sold"

    def test_find_by_status(self, client, unique_id):
        self._create(client, unique_id)

        response = client.get("/pet/findByStatus", params={"status": "available"})

        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert len(pets) > 0
        assert all(p.get("status") == "available" for p in pets)

    def test_delete_pet(self, client, unique_id):
        self._create(client, unique_id)

        delete_response = client.delete(f"/pet/{unique_id}")
        assert delete_response.status_code == 200

        get_response = client.get(f"/pet/{unique_id}")
        assert get_response.status_code == 404

    def test_get_nonexistent_pet_returns_404(self, client):
        response = client.get("/pet/0")

        assert response.status_code == 404

    def test_find_by_tags(self, client, unique_id):
        self._create(client, unique_id)

        response = client.get("/pet/findByTags", params={"tags": "friendly"})

        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert all(
            any(t.get("name") == "friendly" for t in p.get("tags", []))
            for p in pets
        )

    def test_create_pet_with_invalid_payload_is_rejected(self, client):
        response = client.post("/pet", json={"id": "not-an-integer", "name": 123})

        assert response.status_code >= 400

    def test_delete_pet_is_idempotent_returns_404_on_second_call(
        self, client, unique_id
    ):
        self._create(client, unique_id)

        first = client.delete(f"/pet/{unique_id}")
        assert first.status_code == 200

        second = client.delete(f"/pet/{unique_id}")
        assert second.status_code == 404
