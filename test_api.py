import requests
import pytest
from jsonschema import validate

# Схема для валидации ответа GET /api/users
users_schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "per_page": {"type": "number"},
        "total": {"type": "number"},
        "total_pages": {"type": "number"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "number"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"]
            }
        },
        "support": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "text": {"type": "string"}
            },
            "required": ["url", "text"]
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data", "support"]
}

# Тестирование метода GET
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert validate(response.json(), users_schema) is None

# Тестирование метода POST
def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == payload["name"]
    assert response.json()["job"] == payload["job"]

@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["job"] == job

# Тестирование обработки ошибок
def test_invalid_login():
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"})
    assert response.status_code == 400
    assert "error" in response.json()

def test_not_found():
    response = requests.get("https://reqres.in/api/users/999")
    assert response.status_code == 404

# Тестирование метода PUT
def test_update_user():
    payload = {"name": "Alice Updated", "job": "Senior Engineer"}
    response = requests.put("https://reqres.in/api/users/2", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["job"] == payload["job"]

# Тестирование метода DELETE
def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/2")
    assert response.status_code == 204
