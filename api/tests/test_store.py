import pytest

from api.data.payloads import order_payload, pet_payload
from api.data.schemas import ORDER_SCHEMA, assert_schema

pytestmark = pytest.mark.api


class TestStore:
    def _create_pet(self, client, pet_id):
        response = client.post("/pet", json=pet_payload(pet_id))
        assert response.status_code == 200
        return response.json()

    def _place_order(self, client, order_id, pet_id):
        response = client.post(
            "/store/order", json=order_payload(order_id, pet_id)
        )
        assert response.status_code == 200, response.text
        return response.json()

    def test_place_order(self, client, unique_id):
        pet = self._create_pet(client, unique_id)

        body = self._place_order(client, unique_id, pet["id"])

        assert_schema(body, ORDER_SCHEMA)
        assert body["id"] == unique_id
        assert body["petId"] == pet["id"]
        assert body["quantity"] == 1
        assert body["status"] == "placed"

    def test_get_order_by_id(self, client, unique_id):
        pet = self._create_pet(client, unique_id)
        self._place_order(client, unique_id, pet["id"])

        response = client.get(f"/store/order/{unique_id}")

        assert response.status_code == 200
        assert response.json()["id"] == unique_id

    def test_delete_order(self, client, unique_id):
        pet = self._create_pet(client, unique_id)
        self._place_order(client, unique_id, pet["id"])

        delete_response = client.delete(f"/store/order/{unique_id}")
        assert delete_response.status_code == 200

        get_response = client.get(f"/store/order/{unique_id}")
        assert get_response.status_code == 404

    def test_get_inventory(self, client):
        response = client.get("/store/inventory")

        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, dict)
        assert len(inventory) > 0
        assert all(isinstance(v, int) for v in inventory.values())

    def test_get_order_invalid_id_returns_404(self, client):
        response = client.get("/store/order/0")

        assert response.status_code == 404

    def test_place_order_with_invalid_payload_is_rejected(self, client):
        response = client.post(
            "/store/order", json={"id": "abc", "petId": "xyz", "quantity": "many"}
        )

        assert response.status_code >= 400
