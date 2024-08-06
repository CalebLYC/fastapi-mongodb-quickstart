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


def test_add_user():
    # Données de test
    user_data = {
        "email": "test4@example.com",
        "name": "John",
        "password": "12345678",
        "surname": "Doe"
    }

    # Envoi de la requête POST
    response = client.post("/users", json=user_data)

    # Assertions
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["message"] == "User registered successfully"
    assert response_json["user"]["email"] == user_data["email"]

    # Vérifier que l'ID est présent et est un entier
    assert "_id" in response_json["user"]
    assert isinstance(response_json["user"]["_id"], str)

def test_register_email_already_exists():
    # Données de test
    user_data = {
        "email": "test@example.com",
        "name": "John",
        "password": "12345678",
        "surname": "Doe"
    }

    # Envoi de la requête POST
    response = client.post("/users", json=user_data)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}

def test_get_users():
    # Envoi de la requête POST
    response = client.get("/users")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["users"] is dict

def test_get_user():
    # Envoi de la requête POST
    response = client.get("/users/{id}")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["user"]['email'] is str

def test_update_user():
    # Données de test
    user_data = {
        "email": "test@example.com",
        "name": "John",
        "surname": "Doe"
    }

    # Envoi de la requête POST
    response = client.put("/users/{id}", json=user_data)

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["user"]['email'] == user_data['email']

def test_update_user_password():
    # Données de test
    user_data = {
        "password": "12345678"
    }

    # Envoi de la requête POST
    response = client.put("/users/password", json=user_data)

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["user"]['email'] == user_data['email']

def test_delete_user():
    # Envoi de la requête DELETE
    response = client.delete("/users/{id}")

    # Assertions
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Account deleted successfully"