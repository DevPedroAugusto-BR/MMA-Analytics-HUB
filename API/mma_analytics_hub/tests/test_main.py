from http import HTTPStatus

from fastapi.testclient import TestClient

from src.mma_analytics_hub.main import app


def test_read_root(client):
    response = client.get("/root")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_create_user():
    client = TestClient(app)

    response = client.post(
        "/create_user",
        json={
            "username": "John Doe",
            "email": "johndoe@test.com",
            "password": "123456",
            "perfil": "usuario",
            "ativo": True
            },
        )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "John Doe",
        "email": "test@test.com",
    }


def test_update_user(client):
    response = client.put(
        "/update_user/1",
        json={
            "username": "John Doe",
            "email": "johndoe@test.com",
            "password": "123456",
            "perfil": "usuario",
            "ativo": True
            },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "John Doe",
        "email": "test@test.com"
    }
