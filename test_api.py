import requests
import pytest
from jsonschema import validate

#задание 2
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "data": {"type": "array"},
        "per_page": {"type": "number"},
        "total": {"type": "number"},
        "total_pages": {"type": "number"}
    },
    "required": ["page", "data", "per_page", "total", "total_pages"]
}

def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert validate(response.json(), schema) is None

#задание 3
def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] is not None

@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["job"] == job

#задание 4
def test_invalid_login():
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"})
    assert response.status_code == 400
    assert "error" in response.json()

def test_not_found():
    response = requests.get("https://reqres.in/api/users/999")
    assert response.status_code == 404

def test_delete_user():
    # Сначала создаем пользователя
    create_response = requests.post("https://reqres.in/api/users", json={"name": "Temp", "job": "Temp"})
    user_id = create_response.json()["id"]
    
    # Затем удаляем его
    delete_response = requests.delete(f"https://reqres.in/api/users/{user_id}")
    assert delete_response.status_code == 204
    
    # Проверяем, что пользователь действительно удален
    get_response = requests.get(f"https://reqres.in/api/users/{user_id}")
    assert get_response.status_code == 404
