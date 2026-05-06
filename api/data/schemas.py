from jsonschema import validate

PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["available", "pending", "sold"]},
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
    },
}

ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "shipDate": {"type": "string"},
        "status": {"type": "string", "enum": ["placed", "approved", "delivered"]},
        "complete": {"type": "boolean"},
    },
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "username"],
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "phone": {"type": "string"},
        "userStatus": {"type": "integer"},
    },
}

API_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["code", "type", "message"],
    "properties": {
        "code": {"type": "integer"},
        "type": {"type": "string"},
        "message": {"type": "string"},
    },
}


def assert_schema(payload, schema) -> None:
    validate(instance=payload, schema=schema)
