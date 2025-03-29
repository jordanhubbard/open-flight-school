import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_aircraft(client: TestClient):
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["type"] == aircraft_data["type"]
    assert data["model"] == aircraft_data["model"]
    assert "id" in data

def test_create_aircraft_duplicate_registration(client: TestClient):
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    # Create first aircraft
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    
    # Try to create aircraft with same registration
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration already registered"

def test_get_aircrafts(client: TestClient):
    # Create test aircraft
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data1 = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft 1"
    }
    aircraft_data2 = {
        "registration": "N54321",
        "type": "Piper",
        "model": "PA-28",
        "year": 2019,
        "serial_number": "28201234",
        "total_time": 1500,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft 2"
    }
    client.post("/api/v1/aircraft/", json=aircraft_data1)
    client.post("/api/v1/aircraft/", json=aircraft_data2)
    
    response = client.get("/api/v1/aircraft/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["registration"] == aircraft_data1["registration"]
    assert data[1]["registration"] == aircraft_data2["registration"]

def test_get_aircraft(client: TestClient):
    # Create test aircraft
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    aircraft_id = response.json()["id"]
    
    response = client.get(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["type"] == aircraft_data["type"]
    assert data["model"] == aircraft_data["model"]

def test_get_aircraft_not_found(client: TestClient):
    response = client.get("/api/v1/aircraft/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"

def test_update_aircraft(client: TestClient):
    # Create test aircraft
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    aircraft_id = response.json()["id"]
    
    # Update aircraft
    updated_data = aircraft_data.copy()
    updated_data["total_time"] = 1100
    updated_data["notes"] = "Updated aircraft"
    
    response = client.put(f"/api/v1/aircraft/{aircraft_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_time"] == updated_data["total_time"]
    assert data["notes"] == updated_data["notes"]

def test_update_aircraft_not_found(client: TestClient):
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    response = client.put("/api/v1/aircraft/999", json=aircraft_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"

def test_delete_aircraft(client: TestClient):
    # Create test aircraft
    last_maintenance = (datetime.now() - timedelta(days=30)).isoformat()
    next_maintenance = (datetime.now() + timedelta(days=30)).isoformat()
    aircraft_data = {
        "registration": "N12345",
        "type": "Cessna",
        "model": "172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": last_maintenance,
        "next_maintenance": next_maintenance,
        "status": "Available",
        "category": "airplane",
        "class_type": "single-engine land",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 201
    aircraft_id = response.json()["id"]
    
    # Delete aircraft
    response = client.delete(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 200
    
    # Verify aircraft is deleted
    response = client.get(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 404

def test_delete_aircraft_not_found(client: TestClient):
    response = client.delete("/api/v1/aircraft/999")
    assert response.status_code == 404 