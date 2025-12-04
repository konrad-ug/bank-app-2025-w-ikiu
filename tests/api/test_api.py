import pytest
from app.api import app, registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts = []

# testy

def test_create_account(client):
    response = client.post("/api/accounts", json={
        "name": "John", "surname": "Doe", "pesel": "11111111111"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Account created"
    assert registry.number_of_accounts() == 1

def test_get_account_by_pesel(client):
    client.post("/api/accounts", json={"name": "Jane", "surname": "Smith", "pesel": "22222222222"})
    
    # Act: Pobierz
    response = client.get("/api/accounts/22222222222")
    
    # Assert
    assert response.status_code == 200
    assert response.json["name"] == "Jane"
    assert response.json["balance"] == 0.0

def test_get_account_not_found(client):
    response = client.get("/api/accounts/00000000000")
    assert response.status_code == 404

def test_update_account(client):
    client.post("/api/accounts", json={"name": "Rob", "surname": "Green", "pesel": "33333333333"})
    
    response = client.patch("/api/accounts/33333333333", json={"name": "Robert"})
    
    assert response.status_code == 200
    acc = registry.get_account_by_pesel("33333333333")
    assert acc.first_name == "Robert"
    assert acc.last_name == "Green"

def test_delete_account(client):
    client.post("/api/accounts", json={"name": "Lars", "surname": "Ulrich", "pesel": "44444444444"})
    assert registry.number_of_accounts() == 1
    
    response = client.delete("/api/accounts/44444444444")
    
    assert response.status_code == 200
    assert registry.number_of_accounts() == 0

def test_delete_account_not_found(client):
    response = client.delete("/api/accounts/99999999999")
    assert response.status_code == 404


# etc/hosts