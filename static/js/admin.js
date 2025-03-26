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
            <td>${instructor.ratings.join(', ')}</td>
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

function editAircraft(id) {
    const aircraft = aircraftData.find(a => a.id === id);
    if (!aircraft) return;

    const form = document.createElement('form');
    form.innerHTML = `
        <div class="form-group">
            <label for="tail_number">Tail Number</label>
            <input type="text" class="form-control" id="tail_number" value="${aircraft.tail_number}" required>
        </div>
        <div class="form-group">
            <label for="make_model">Make/Model</label>
            <input type="text" class="form-control" id="make_model" value="${aircraft.make_model}" required>
        </div>
        <div class="form-group">
            <label for="type">Type</label>
            <input type="text" class="form-control" id="type" value="${aircraft.type}" required>
        </div>
    `;

    showModal('Edit Aircraft', form, async () => {
        const data = {
            tail_number: form.querySelector('#tail_number').value,
            make_model: form.querySelector('#make_model').value,
            type: form.querySelector('#type').value
        };

        try {
            const response = await fetch(`/api/admin/aircraft/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Failed to update aircraft');
            
            const updatedAircraft = await response.json();
            const index = aircraftData.findIndex(a => a.id === id);
            if (index !== -1) {
                aircraftData[index] = updatedAircraft;
                displayAircraft();
            }
        } catch (error) {
            console.error('Error updating aircraft:', error);
            showError('Failed to update aircraft');
        }
    });
}

function editInstructor(id) {
    const instructor = instructorData.find(i => i.id === id);
    if (!instructor) return;

    const form = document.createElement('form');
    form.innerHTML = `
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" value="${instructor.name}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" value="${instructor.email}" required>
        </div>
        <div class="form-group">
            <label for="phone">Phone</label>
            <input type="tel" class="form-control" id="phone" value="${instructor.phone || ''}" required>
        </div>
        <div class="form-group">
            <label for="ratings">Ratings (comma-separated)</label>
            <input type="text" class="form-control" id="ratings" value="${instructor.ratings.join(',')}" required>
        </div>
    `;

    showModal('Edit Instructor', form, async () => {
        const data = {
            name: form.querySelector('#name').value,
            email: form.querySelector('#email').value,
            phone: form.querySelector('#phone').value,
            ratings: form.querySelector('#ratings').value.split(',').map(r => r.trim()).filter(r => r)
        };

        try {
            const response = await fetch(`/api/admin/instructors/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Failed to update instructor');
            
            const updatedInstructor = await response.json();
            const index = instructorData.findIndex(i => i.id === id);
            if (index !== -1) {
                instructorData[index] = updatedInstructor;
                displayInstructors();
            }
        } catch (error) {
            console.error('Error updating instructor:', error);
            showError('Failed to update instructor');
        }
    });
}

async function deleteAircraft(id) {
    if (!confirm('Are you sure you want to delete this aircraft?')) return;

    try {
        const response = await fetch(`/api/admin/aircraft/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete aircraft');
        
        aircraftData = aircraftData.filter(a => a.id !== id);
        displayAircraft();
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

        if (!response.ok) throw new Error('Failed to delete instructor');
        
        instructorData = instructorData.filter(i => i.id !== id);
        displayInstructors();
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