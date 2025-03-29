import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_user(client: TestClient):
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data
    assert "id" in data

def test_create_user_duplicate_email(client: TestClient):
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    # Create first user
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    # Try to create user with same email
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_users(client: TestClient):
    # Create test users
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data1 = {
        "email": "test1@example.com",
        "full_name": "Test User 1",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    user_data2 = {
        "email": "test2@example.com",
        "full_name": "Test User 2",
        "phone": "0987654321",
        "address": "321 Test St",
        "medical_class": "Class 2",
        "medical_expiry": medical_expiry,
        "ratings": "Commercial Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    client.post("/api/v1/users/", json=user_data1)
    client.post("/api/v1/users/", json=user_data2)
    
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == user_data1["email"]
    assert data[1]["email"] == user_data2["email"]

def test_get_user(client: TestClient):
    # Create test user
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]

def test_get_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user(client: TestClient):
    # Create test user
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Update user
    updated_data = user_data.copy()
    updated_data["full_name"] = "Updated User"
    updated_data["phone"] = "9876543210"
    
    response = client.put(f"/api/v1/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == updated_data["full_name"]
    assert data["phone"] == updated_data["phone"]

def test_update_user_not_found(client: TestClient):
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.put("/api/v1/users/999", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user(client: TestClient):
    # Create test user
    medical_expiry = (datetime.now() + timedelta(days=365)).isoformat()
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": medical_expiry,
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    
    # Verify user is deleted
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404

def test_delete_user_not_found(client: TestClient):
    response = client.delete("/api/v1/users/999")
    assert response.status_code == 404 