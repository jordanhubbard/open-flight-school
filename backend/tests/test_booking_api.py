import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def create_test_user(client: TestClient):
    user_data = {
        "email": "student@example.com",
        "full_name": "Test Student",
        "phone": "1234567890",
        "address": "123 Test St",
        "medical_class": "Class 1",
        "medical_expiry": "2023-12-31T00:00:00",
        "ratings": "Private Pilot",
        "endorsements": "None",
        "flight_reviews": "None",
        "currency": "Current",
        "notes": "Test notes",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.json()["id"]

def create_test_instructor(client: TestClient):
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
    return response.json()["id"]

def create_test_aircraft(client: TestClient):
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
    return response.json()["id"]

def test_create_booking(client: TestClient):
    student_id = create_test_user(client)
    instructor_id = create_test_instructor(client)
    aircraft_id = create_test_aircraft(client)
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking"
    }
    response = client.post("/api/v1/bookings/", json=booking_data)
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == booking_data["student_id"]
    assert data["instructor_id"] == booking_data["instructor_id"]
    assert data["aircraft_id"] == booking_data["aircraft_id"]
    assert "id" in data

def test_get_bookings(client: TestClient):
    student_id = create_test_user(client)
    instructor_id = create_test_instructor(client)
    aircraft_id = create_test_aircraft(client)
    
    start_time1 = datetime.now() + timedelta(days=1)
    end_time1 = start_time1 + timedelta(hours=2)
    start_time2 = datetime.now() + timedelta(days=2)
    end_time2 = start_time2 + timedelta(hours=2)
    
    booking_data1 = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time1.isoformat(),
        "end_time": end_time1.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking 1"
    }
    booking_data2 = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time2.isoformat(),
        "end_time": end_time2.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking 2"
    }
    client.post("/api/v1/bookings/", json=booking_data1)
    client.post("/api/v1/bookings/", json=booking_data2)
    
    response = client.get("/api/v1/bookings/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["notes"] == booking_data1["notes"]
    assert data[1]["notes"] == booking_data2["notes"]

def test_get_booking(client: TestClient):
    student_id = create_test_user(client)
    instructor_id = create_test_instructor(client)
    aircraft_id = create_test_aircraft(client)
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking"
    }
    response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = response.json()["id"]
    
    response = client.get(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == booking_data["student_id"]
    assert data["instructor_id"] == booking_data["instructor_id"]
    assert data["aircraft_id"] == booking_data["aircraft_id"]

def test_get_booking_not_found(client: TestClient):
    response = client.get("/api/v1/bookings/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"

def test_update_booking(client: TestClient):
    student_id = create_test_user(client)
    instructor_id = create_test_instructor(client)
    aircraft_id = create_test_aircraft(client)
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking"
    }
    response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = response.json()["id"]
    
    # Update booking
    updated_data = booking_data.copy()
    updated_data["status"] = "Confirmed"
    updated_data["notes"] = "Updated booking"
    
    response = client.put(f"/api/v1/bookings/{booking_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == updated_data["status"]
    assert data["notes"] == updated_data["notes"]

def test_update_booking_not_found(client: TestClient):
    booking_data = {
        "student_id": 1,
        "instructor_id": 1,
        "aircraft_id": 1,
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "status": "Scheduled",
        "notes": "Test booking"
    }
    response = client.put("/api/v1/bookings/999", json=booking_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"

def test_delete_booking(client: TestClient):
    student_id = create_test_user(client)
    instructor_id = create_test_instructor(client)
    aircraft_id = create_test_aircraft(client)
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "student_id": student_id,
        "instructor_id": instructor_id,
        "aircraft_id": aircraft_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "Scheduled",
        "notes": "Test booking"
    }
    response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = response.json()["id"]
    
    # Delete booking
    response = client.delete(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 200
    
    # Verify booking is deleted
    response = client.get(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 404

def test_delete_booking_not_found(client: TestClient):
    response = client.delete("/api/v1/bookings/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found" 