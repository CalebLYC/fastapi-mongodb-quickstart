import pytest
from fastapi.testclient import TestClient
from main import app
from models.user import CreateUserModel
from services.token_service import TokenService
from services.user_service import UserService
from config.enviro import env
from config.database import db, client

client = TestClient(app)

@pytest.fixture(scope='function')
async def dab():
    async with client.start_session() as session:
        async with session.start_transaction():
            yield db  # Donne accès à la base de données pour les tests

            # La transaction sera annulée, donc aucune donnée ne sera persistée


def test_add_role():
    role_data = {
        "description": "A test role",
        "name": "test"
    }

    # Envoi de la requête POST
    response = client.post("/roles", json = role_data)

    # Assertions
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["role"]['name'] == role_data['name']

def test_get_roles():
    # Envoi de la requête POST
    response = client.get("/roles")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["roles"] is dict

def test_get_role():
    # Envoi de la requête POST
    response = client.get("/role/test")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["role"]['name'] == "test"

def test_update_role():
    # Données de test
    role_data = {
      "description": "A test role",
      "name": "test"
    }

    # Envoi de la requête POST
    response = client.put("/roles/test", json=role_data)

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["role"]['name'] == role_data['name']

def test_delete_role():
    # Envoi de la requête POST
    response = client.delete("/roles/test")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Role deleted successfully"