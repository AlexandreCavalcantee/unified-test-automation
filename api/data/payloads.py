def pet_payload(pet_id: int, name: str = "Rex", status: str = "available") -> dict:
    return {
        "id": pet_id,
        "category": {"id": 1, "name": "dogs"},
        "name": name,
        "photoUrls": ["https://example.com/rex.png"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": status,
    }


def order_payload(order_id: int, pet_id: int, quantity: int = 1) -> dict:
    return {
        "id": order_id,
        "petId": pet_id,
        "quantity": quantity,
        "shipDate": "2026-01-01T00:00:00.000Z",
        "status": "placed",
        "complete": True,
    }


def user_payload(username: str, user_id: int = 1) -> dict:
    return {
        "id": user_id,
        "username": username,
        "firstName": "Alex",
        "lastName": "Test",
        "email": f"{username}@example.com",
        "password": "test123",
        "phone": "5511999999999",
        "userStatus": 1,
    }
