import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_instructor(client: TestClient):
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    response = client.post("/api/v1/instructors/", json=instructor_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == instructor_data["email"]
    assert data["name"] == instructor_data["name"]
    assert "id" in data

def test_create_instructor_duplicate_email(client: TestClient):
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    # Create first instructor
    response = client.post("/api/v1/instructors/", json=instructor_data)
    assert response.status_code == 200
    
    # Try to create instructor with same email
    response = client.post("/api/v1/instructors/", json=instructor_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_instructors(client: TestClient):
    # Create test instructors
    instructor_data1 = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor 1"
    }
    instructor_data2 = {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "0987654321",
        "ratings": "CFI, CFII",
        "endorsements": "Complex",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Weekends",
        "notes": "Test instructor 2"
    }
    client.post("/api/v1/instructors/", json=instructor_data1)
    client.post("/api/v1/instructors/", json=instructor_data2)
    
    response = client.get("/api/v1/instructors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == instructor_data1["email"]
    assert data[1]["email"] == instructor_data2["email"]

def test_get_instructor(client: TestClient):
    # Create test instructor
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = response.json()["id"]
    
    response = client.get(f"/api/v1/instructors/{instructor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == instructor_data["email"]
    assert data["name"] == instructor_data["name"]

def test_get_instructor_not_found(client: TestClient):
    response = client.get("/api/v1/instructors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Instructor not found"

def test_update_instructor(client: TestClient):
    # Create test instructor
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = response.json()["id"]
    
    # Update instructor
    updated_data = instructor_data.copy()
    updated_data["phone"] = "9876543210"
    updated_data["availability"] = "Weekends only"
    
    response = client.put(f"/api/v1/instructors/{instructor_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == updated_data["phone"]
    assert data["availability"] == updated_data["availability"]

def test_update_instructor_not_found(client: TestClient):
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    response = client.put("/api/v1/instructors/999", json=instructor_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Instructor not found"

def test_delete_instructor(client: TestClient):
    # Create test instructor
    instructor_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "ratings": "CFI, CFII, MEI",
        "endorsements": "Complex, High Performance",
        "flight_reviews": "Current",
        "currency": "Current",
        "availability": "Mon-Fri 9am-5pm",
        "notes": "Test instructor"
    }
    response = client.post("/api/v1/instructors/", json=instructor_data)
    instructor_id = response.json()["id"]
    
    # Delete instructor
    response = client.delete(f"/api/v1/instructors/{instructor_id}")
    assert response.status_code == 200
    
    # Verify instructor is deleted
    response = client.get(f"/api/v1/instructors/{instructor_id}")
    assert response.status_code == 404

def test_delete_instructor_not_found(client: TestClient):
    response = client.delete("/api/v1/instructors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Instructor not found" 