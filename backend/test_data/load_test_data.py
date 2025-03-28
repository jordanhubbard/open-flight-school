import json
import requests
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# API endpoint
API_URL = "http://localhost:5000/api/v1"

# Load test data from JSON files
def load_test_data():
    # Load user data
    with open(os.path.join(SCRIPT_DIR, 'users', 'test_user.json'), 'r') as f:
        user_data = json.load(f)
    response = requests.post(f"{API_URL}/users/", json=user_data)
    print("User added:", response.status_code)

    # Load aircraft data
    with open(os.path.join(SCRIPT_DIR, 'aircraft', 'test_aircraft.json'), 'r') as f:
        aircraft_data = json.load(f)
    response = requests.post(f"{API_URL}/aircraft/", json=aircraft_data)
    print("Aircraft added:", response.status_code)

    # Load instructor data
    with open(os.path.join(SCRIPT_DIR, 'instructors', 'test_instructor.json'), 'r') as f:
        instructor_data = json.load(f)
    response = requests.post(f"{API_URL}/instructors/", json=instructor_data)
    print("Instructor added:", response.status_code)

    # Load booking data
    with open(os.path.join(SCRIPT_DIR, 'bookings', 'test_booking.json'), 'r') as f:
        booking_data = json.load(f)
    response = requests.post(f"{API_URL}/bookings/", json=booking_data)
    print("Booking added:", response.status_code)

if __name__ == "__main__":
    load_test_data() 