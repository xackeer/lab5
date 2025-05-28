import requests
import pytest
from jsonschema import validate

API = "reqres-free-v1"
HEADER = {
    "x-api-key": API
}
schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "data": {"type": "array"}
    },
    "required": ["data"]
}

def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2", headers= HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    validate(instance=response.json(), schema=schema)

def test_create_user():
    payload = {"name": "Alice", "job": "Engineer"}
    response = requests.post("https://reqres.in/api/users", json=payload,  headers= HEADER)
    assert response.status_code == 201
    assert response.json().get("id") is not None

@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job},  headers= HEADER)
    assert response.status_code == 201

def test_invalid_login():
    response = requests.post("https://reqres.in/api/login", json={"email": "test@test"},  headers= HEADER)
    assert response.status_code == 400
    assert "error" in response.json()

def test_not_found():
    response = requests.get("https://reqres.in/api/users/999",  headers= HEADER)
    assert response.status_code == 404
