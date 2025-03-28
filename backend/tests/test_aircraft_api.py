import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_aircraft(client: TestClient):
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["make_model"] == aircraft_data["make_model"]
    assert "id" in data

def test_create_aircraft_duplicate_registration(client: TestClient):
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    # Create first aircraft
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 200
    
    # Try to create aircraft with same registration
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration already registered"

def test_get_aircrafts(client: TestClient):
    # Create test aircraft
    aircraft_data1 = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft 1"
    }
    aircraft_data2 = {
        "registration": "N54321",
        "make_model": "Piper PA-28",
        "year": 2019,
        "serial_number": "28201234",
        "total_time": 1500,
        "last_maintenance": "2023-11-01T00:00:00",
        "next_maintenance": "2024-11-01T00:00:00",
        "status": "Active",
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
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    aircraft_id = response.json()["id"]
    
    response = client.get(f"/api/v1/aircraft/{aircraft_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["registration"] == aircraft_data["registration"]
    assert data["make_model"] == aircraft_data["make_model"]

def test_get_aircraft_not_found(client: TestClient):
    response = client.get("/api/v1/aircraft/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"

def test_update_aircraft(client: TestClient):
    # Create test aircraft
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
    aircraft_id = response.json()["id"]
    
    # Update aircraft
    updated_data = aircraft_data.copy()
    updated_data["total_time"] = 1100
    updated_data["status"] = "Maintenance"
    
    response = client.put(f"/api/v1/aircraft/{aircraft_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_time"] == updated_data["total_time"]
    assert data["status"] == updated_data["status"]

def test_update_aircraft_not_found(client: TestClient):
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    response = client.put("/api/v1/aircraft/999", json=aircraft_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"

def test_delete_aircraft(client: TestClient):
    # Create test aircraft
    aircraft_data = {
        "registration": "N12345",
        "make_model": "Cessna 172",
        "year": 2020,
        "serial_number": "17201234",
        "total_time": 1000,
        "last_maintenance": "2023-12-01T00:00:00",
        "next_maintenance": "2024-12-01T00:00:00",
        "status": "Active",
        "notes": "Test aircraft"
    }
    response = client.post("/api/v1/aircraft/", json=aircraft_data)
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
    assert response.json()["detail"] == "Aircraft not found" 