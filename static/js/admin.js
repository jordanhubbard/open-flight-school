let aircraftData = [];
let instructorData = [];
let userData = [];
let bookingData = [];

async function loadData() {
    try {
        // Load aircraft data
        const aircraftResponse = await fetch('/api/admin/aircraft');
        if (!aircraftResponse.ok) throw new Error('Failed to load aircraft data');
        aircraftData = await aircraftResponse.json();
        displayAircraft();

        // Load instructor data
        const instructorResponse = await fetch('/api/admin/instructors');
        if (!instructorResponse.ok) throw new Error('Failed to load instructor data');
        instructorData = await instructorResponse.json();
        displayInstructors();

        // Load user data
        const userResponse = await fetch('/api/admin/users');
        if (!userResponse.ok) throw new Error('Failed to load user data');
        userData = await userResponse.json();
        displayUsers();

        // Load booking data
        const bookingResponse = await fetch('/api/admin/bookings');
        if (!bookingResponse.ok) throw new Error('Failed to load booking data');
        bookingData = await bookingResponse.json();
        displayBookings();
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Failed to load data');
    }
}

function displayAircraft() {
    const tableBody = document.querySelector('#aircraftTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = aircraftData.map(aircraft => `
        <tr>
            <td>${aircraft.make_model}</td>
            <td>${aircraft.tail_number}</td>
            <td>${aircraft.type}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editAircraft(${aircraft.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteAircraft(${aircraft.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function displayInstructors() {
    const tableBody = document.querySelector('#instructorsTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = instructorData.map(instructor => `
        <tr>
            <td>${instructor.name}</td>
            <td>${instructor.email}</td>
            <td>${instructor.phone || ''}</td>
            <td>${instructor.ratings || ''}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editInstructor(${instructor.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteInstructor(${instructor.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function displayUsers() {
    const tableBody = document.querySelector('#usersTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = userData.map(user => `
        <tr>
            <td>${user.first_name} ${user.last_name}</td>
            <td>${user.email}</td>
            <td>${user.phone || ''}</td>
            <td>${user.is_admin ? 'Admin' : 'User'}</td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editUser(${user.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function displayBookings() {
    const tableBody = document.querySelector('#bookingsTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = bookingData.map(booking => `
        <tr>
            <td>${booking.user.name}</td>
            <td>${new Date(booking.start_time).toLocaleDateString()}</td>
            <td>${new Date(booking.start_time).toLocaleTimeString()} - ${new Date(booking.end_time).toLocaleTimeString()}</td>
            <td>${booking.aircraft || ''}</td>
            <td>${booking.instructor || ''}</td>
            <td>${booking.status}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editBooking(${booking.id})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteBooking(${booking.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
}

function showModal(title, content, onSave) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body"></div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="save-button">Save</button>
                </div>
            </div>
        </div>
    `;

    modal.querySelector('.modal-body').appendChild(content);
    document.body.appendChild(modal);

    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();

    modal.querySelector('#save-button').addEventListener('click', async () => {
        await onSave();
        modalInstance.hide();
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    });
}

// Load data when the page loads
document.addEventListener('DOMContentLoaded', loadData);

// Aircraft Management
async function saveAircraft() {
    const data = {
        make_model: document.getElementById('makeModel').value,
        tail_number: document.getElementById('tailNumber').value,
        type: document.getElementById('type').value
    };
    
    const aircraftId = document.getElementById('aircraftId').value;
    const method = aircraftId ? 'PUT' : 'POST';
    const url = aircraftId ? `/api/admin/aircraft/${aircraftId}` : '/api/admin/aircraft';
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('aircraftModal')).hide();
            loadData();
            showSuccess('Aircraft saved successfully');
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to save aircraft');
        }
    } catch (error) {
        console.error('Error saving aircraft:', error);
        showError('Failed to save aircraft');
    }
}

// Instructor Management
async function saveInstructor() {
    const data = {
        name: document.getElementById('instructorName').value,
        email: document.getElementById('instructorEmail').value,
        phone: document.getElementById('instructorPhone').value,
        ratings: document.getElementById('instructorRatings').value.split(',').map(r => r.trim()).filter(r => r)
    };
    
    const instructorId = document.getElementById('instructorId').value;
    const method = instructorId ? 'PUT' : 'POST';
    const url = instructorId ? `/api/admin/instructors/${instructorId}` : '/api/admin/instructors';
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('instructorModal')).hide();
            loadData();
            showSuccess('Instructor saved successfully');
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to save instructor');
        }
    } catch (error) {
        console.error('Error saving instructor:', error);
        showError('Failed to save instructor');
    }
}

function editAircraft(id) {
    fetch(`/api/admin/aircraft/${id}`)
        .then(response => response.json())
        .then(aircraft => {
            document.getElementById('aircraftModalTitle').textContent = 'Edit Aircraft';
            document.getElementById('aircraftId').value = aircraft.id;
            document.getElementById('makeModel').value = aircraft.make_model;
            document.getElementById('tailNumber').value = aircraft.tail_number;
            document.getElementById('type').value = aircraft.type;
            new bootstrap.Modal(document.getElementById('aircraftModal')).show();
        })
        .catch(error => {
            console.error('Error loading aircraft:', error);
            showError('Failed to load aircraft data');
        });
}

function editInstructor(id) {
    fetch(`/api/admin/instructors/${id}`)
        .then(response => response.json())
        .then(instructor => {
            document.getElementById('instructorModalTitle').textContent = 'Edit Instructor';
            document.getElementById('instructorId').value = instructor.id;
            document.getElementById('instructorName').value = instructor.name;
            document.getElementById('instructorEmail').value = instructor.email;
            document.getElementById('instructorPhone').value = instructor.phone;
            document.getElementById('instructorRatings').value = instructor.ratings.join(', ');
            new bootstrap.Modal(document.getElementById('instructorModal')).show();
        })
        .catch(error => {
            console.error('Error loading instructor:', error);
            showError('Failed to load instructor data');
        });
}

// Delete functions
async function deleteAircraft(id) {
    if (!confirm('Are you sure you want to delete this aircraft?')) return;

    try {
        const response = await fetch(`/api/admin/aircraft/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadData();
            showSuccess('Aircraft deleted successfully');
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to delete aircraft');
        }
    } catch (error) {
        console.error('Error deleting aircraft:', error);
        showError('Failed to delete aircraft');
    }
}

async function deleteInstructor(id) {
    if (!confirm('Are you sure you want to delete this instructor?')) return;

    try {
        const response = await fetch(`/api/admin/instructors/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadData();
            showSuccess('Instructor deleted successfully');
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to delete instructor');
        }
    } catch (error) {
        console.error('Error deleting instructor:', error);
        showError('Failed to delete instructor');
    }
}

async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
        const response = await fetch(`/api/admin/users/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete user');
        
        userData = userData.filter(u => u.id !== id);
        displayUsers();
    } catch (error) {
        console.error('Error deleting user:', error);
        showError('Failed to delete user');
    }
}

async function deleteBooking(id) {
    if (!confirm('Are you sure you want to delete this booking?')) return;

    try {
        const response = await fetch(`/api/admin/bookings/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete booking');
        
        bookingData = bookingData.filter(b => b.id !== id);
        displayBookings();
    } catch (error) {
        console.error('Error deleting booking:', error);
        showError('Failed to delete booking');
    }
}

function showAddAircraftModal() {
    document.getElementById('aircraftModalTitle').textContent = 'Add Aircraft';
    document.getElementById('aircraftId').value = '';
    document.getElementById('makeModel').value = '';
    document.getElementById('tailNumber').value = '';
    document.getElementById('type').value = '';
    new bootstrap.Modal(document.getElementById('aircraftModal')).show();
}

function showAddInstructorModal() {
    document.getElementById('instructorModalTitle').textContent = 'Add Instructor';
    document.getElementById('instructorId').value = '';
    document.getElementById('instructorName').value = '';
    document.getElementById('instructorEmail').value = '';
    document.getElementById('instructorPhone').value = '';
    document.getElementById('instructorRatings').value = '';
    new bootstrap.Modal(document.getElementById('instructorModal')).show();
}

// Helper functions
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.insertBefore(successDiv, document.body.firstChild);
}

function showError(message) {
    // Implement error message display
    alert(message);
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadData();
}); 