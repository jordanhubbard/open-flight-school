// Utility functions
function showError(message, options = {}) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    
    let content = message;
    if (options.action) {
        content += `
            <div class="mt-2">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="this.closest('.alert').remove()">
                    ${options.action}
                </button>
            </div>
        `;
    }
    
    alertDiv.innerHTML = `
        ${content}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Try to find the container
    const container = document.querySelector('.container');
    if (container) {
        // Try to find the first row
        const firstRow = container.querySelector('.row');
        if (firstRow) {
            // Insert before the first row
            container.insertBefore(alertDiv, firstRow);
        } else {
            // If no row found, append to container
            container.appendChild(alertDiv);
        }
    } else {
        // If no container found, append to body
        document.body.appendChild(alertDiv);
    }
}

function showSuccess(message) {
    const toast = document.createElement('div');
    toast.className = 'alert alert-success alert-dismissible fade show';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('.container').insertBefore(toast, document.querySelector('.container').firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(toast);
        bsAlert.close();
    }, 5000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
    return overlay;
}

function hideLoading(overlay) {
    if (overlay) {
        overlay.remove();
    }
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    let requirements = [];
    
    if (password.length >= 8) {
        strength++;
    } else {
        requirements.push('at least 8 characters');
    }
    
    if (password.match(/[a-z]/)) {
        strength++;
    } else {
        requirements.push('lowercase letter');
    }
    
    if (password.match(/[A-Z]/)) {
        strength++;
    } else {
        requirements.push('uppercase letter');
    }
    
    if (password.match(/[0-9]/)) {
        strength++;
    } else {
        requirements.push('number');
    }
    
    if (password.match(/[^a-zA-Z0-9]/)) {
        strength++;
    } else {
        requirements.push('special character');
    }
    
    return {
        strength: strength,
        requirements: requirements
    };
}

// API calls
async function registerUser(userData) {
    console.log('Attempting to register user:', userData);
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        console.log('Registration response status:', response.status);
        const data = await response.json();
        console.log('Registration response data:', data);
        
        if (response.ok) {
            hideRegisterModal();
            showSuccess('Registration successful! Please login.');
            setTimeout(() => {
                showLoginModal();
            }, 1500); // Show login modal after a short delay
        } else {
            // Show error in the registration modal
            const errorMessage = data.error || 'Registration failed';
            showError(errorMessage);
            
            // Only show password reset modal if explicitly requested
            if (response.status === 400 && data.error === 'Email already registered') {
                // Add a button to the error message to reset password
                showError(errorMessage, {
                    action: 'Reset Password',
                    onclick: () => {
                        hideRegisterModal();
                        showResetPasswordModal();
                    }
                });
            }
        }
    } catch (error) {
        console.error('Registration error:', error);
        showError('An error occurred during registration');
    }
}

async function loginUser(credentials) {
    console.log('Attempting to login with:', credentials);
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials)
        });
        
        console.log('Login response status:', response.status);
        const data = await response.json();
        console.log('Login response data:', data);
        
        if (response.ok) {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                window.location.reload();
            }
        } else {
            showError(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('An error occurred during login');
    }
}

async function getBookings() {
    try {
        const response = await fetch('/api/bookings');
        if (response.ok) {
            const bookings = await response.json();
            displayBookings(bookings);
        } else {
            showError('Failed to load bookings');
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
        showError('An error occurred while loading bookings');
    }
}

function displayBookings(bookings) {
    const tbody = document.getElementById('bookingsList');
    if (!tbody) return;

    tbody.innerHTML = '';
    if (bookings.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="6" class="text-center">No bookings found</td>';
        tbody.appendChild(row);
        return;
    }

    bookings.forEach(booking => {
        const startDate = new Date(booking.start_time);
        const endDate = new Date(booking.end_time);
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${startDate.toLocaleDateString()}</td>
            <td>${startDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                ${endDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
            <td>${booking.aircraft}</td>
            <td>${booking.instructor}</td>
            <td>
                <span class="badge ${booking.status === 'confirmed' ? 'bg-success' : 'bg-warning'}">
                    ${booking.status}
                </span>
            </td>
            <td>
                <button type="button" class="btn btn-link text-primary p-0 me-2" onclick="editBooking(${booking.id})" 
                        title="Edit booking">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button type="button" class="btn btn-link text-danger p-0" onclick="deleteBooking(${booking.id})"
                        title="Cancel booking">
                    <i class="bi bi-trash-fill"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function editBooking(bookingId) {
    // Find the booking in the current bookings list
    fetch(`/api/bookings/${bookingId}`)
        .then(response => response.json())
        .then(booking => {
            document.getElementById('editBookingId').value = bookingId;
            document.getElementById('editStartTime').value = booking.start_time;
            document.getElementById('editEndTime').value = booking.end_time;
            
            const modal = new bootstrap.Modal(document.getElementById('editBookingModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Failed to load booking details');
        });
}

function deleteBooking(bookingId) {
    document.getElementById('editBookingId').value = bookingId;
    const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    modal.show();
}

// Add event listener for delete confirmation
document.addEventListener('DOMContentLoaded', function() {
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            const bookingId = document.getElementById('editBookingId').value;
            
            fetch(`/api/bookings/${bookingId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                } else {
                    showSuccess('Booking cancelled successfully');
                    bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal')).hide();
                    getBookings();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while cancelling the booking');
            });
        });
    }

    // Add event listener for saving edited booking
    const saveBookingBtn = document.getElementById('saveBookingBtn');
    if (saveBookingBtn) {
        saveBookingBtn.addEventListener('click', function() {
            const bookingId = document.getElementById('editBookingId').value;
            const startTime = document.getElementById('editStartTime').value;
            const endTime = document.getElementById('editEndTime').value;

            if (!startTime || !endTime) {
                showError('Please select both start and end times');
                return;
            }

            fetch(`/api/bookings/${bookingId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    start_time: startTime,
                    end_time: endTime
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                } else {
                    showSuccess('Booking updated successfully');
                    bootstrap.Modal.getInstance(document.getElementById('editBookingModal')).hide();
                    getBookings();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while updating the booking');
            });
        });
    }
});

// Modal handling
function showRegisterModal() {
    const modal = new bootstrap.Modal(document.getElementById('registerModal'));
    modal.show();
}

function hideRegisterModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
    if (modal) modal.hide();
}

function showLoginModal() {
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
}

function hideLoginModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
    if (modal) modal.hide();
}

function showResetPasswordModal() {
    const modal = new bootstrap.Modal(document.getElementById('resetPasswordModal'));
    modal.show();
}

function hideResetPasswordModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('resetPasswordModal'));
    if (modal) modal.hide();
}

function showNewPasswordModal() {
    const modal = new bootstrap.Modal(document.getElementById('newPasswordModal'));
    modal.show();
}

function hideNewPasswordModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('newPasswordModal'));
    if (modal) modal.hide();
}

// Password reset functionality
async function requestPasswordReset(email) {
    try {
        const response = await fetch('/api/request-password-reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        if (response.ok) {
            hideResetPasswordModal();
            showSuccess('If an account exists with this email, you will receive password reset instructions.');
        } else {
            showError(data.error || 'Failed to send reset email');
        }
    } catch (error) {
        console.error('Password reset request error:', error);
        showError('An error occurred while requesting password reset');
    }
}

async function resetPassword(token, password) {
    try {
        const response = await fetch(`/api/reset-password/${token}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password })
        });
        
        const data = await response.json();
        if (response.ok) {
            hideNewPasswordModal();
            showSuccess('Password has been reset successfully. Please login with your new password.');
            setTimeout(() => {
                showLoginModal();
            }, 1500);
        } else {
            showError(data.error || 'Failed to reset password');
        }
    } catch (error) {
        console.error('Password reset error:', error);
        showError('An error occurred while resetting password');
    }
}

// Form Validation
function validatePassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return {
        isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar,
        message: 'Password must be at least 8 characters long and contain uppercase, lowercase, numbers, and special characters.'
    };
}

// API Calls
async function apiCall(url, method = 'GET', data = null) {
    const overlay = showLoading();
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'An error occurred');
        }
        
        return result;
    } catch (error) {
        showError(error.message);
        throw error;
    } finally {
        hideLoading(overlay);
    }
}

function bookNow() {
    const selectedAircraft = document.querySelector('input[name="aircraft"]:checked');
    const selectedInstructor = document.querySelector('input[name="instructor"]:checked');
    
    if (!selectedAircraft || !selectedInstructor) {
        showError('Please select both an aircraft and an instructor');
        return;
    }
    
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    
    if (!startTime || !endTime) {
        showError('Please select both start and end times');
        return;
    }
    
    // Create booking
    createBooking({
        aircraft_id: selectedAircraft.value,
        instructor_id: selectedInstructor.value,
        start_time: startTime,
        end_time: endTime
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only fetch data if we're on the booking page
    const isBookingPage = document.getElementById('bookingsList') !== null;
    
    if (isBookingPage) {
        // Load initial data
        loadAvailableAircraft();
        loadAvailableInstructors();
        getBookings();
    }
});

// Aircraft Management
async function saveAircraft() {
    const form = document.getElementById('aircraftForm');
    const formData = {
        make_model: document.getElementById('makeModel').value,
        tail_number: document.getElementById('tailNumber').value,
        type: document.getElementById('type').value
    };

    try {
        const response = await fetch('/api/admin/aircraft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (response.ok) {
            showSuccess('Aircraft saved successfully');
            const modal = bootstrap.Modal.getInstance(document.getElementById('aircraftModal'));
            modal.hide();
            loadAircraft(); // Refresh the aircraft list
        } else {
            showError(data.error || 'Failed to save aircraft');
        }
    } catch (error) {
        console.error('Error saving aircraft:', error);
        showError('An error occurred while saving the aircraft');
    }
}

async function loadAircraft() {
    try {
        const response = await fetch('/api/admin/aircraft');
        if (response.ok) {
            const aircraft = await response.json();
            const tbody = document.getElementById('aircraftTableBody');
            tbody.innerHTML = '';
            
            aircraft.forEach(a => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${a.make_model}</td>
                    <td>${a.tail_number}</td>
                    <td>${a.type}</td>
                    <td>${a.available ? 'Available' : 'Unavailable'}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editAircraft(${a.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteAircraft(${a.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            showError('Failed to load aircraft');
        }
    } catch (error) {
        console.error('Error loading aircraft:', error);
        showError('An error occurred while loading aircraft');
    }
}

function showAddAircraftModal() {
    document.getElementById('aircraftModalTitle').textContent = 'Add Aircraft';
    document.getElementById('aircraftForm').reset();
    document.getElementById('aircraftId').value = '';
    const modal = new bootstrap.Modal(document.getElementById('aircraftModal'));
    modal.show();
}

// Instructor Management
async function saveInstructor() {
    const form = document.getElementById('instructorForm');
    const data = {
        name: document.getElementById('instructorName').value,
        email: document.getElementById('instructorEmail').value,
        phone: document.getElementById('instructorPhone').value,
        ratings: document.getElementById('ratings').value
    };
    
    try {
        const response = await fetch('/api/admin/instructors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        if (response.ok) {
            showSuccess('Instructor saved successfully');
            const modal = bootstrap.Modal.getInstance(document.getElementById('instructorModal'));
            modal.hide();
            loadInstructors(); // Refresh the instructor list
        } else {
            showError(responseData.error || 'Failed to save instructor');
        }
    } catch (error) {
        console.error('Error saving instructor:', error);
        showError('An error occurred while saving the instructor');
    }
}

async function loadInstructors() {
    try {
        const response = await fetch('/api/admin/instructors');
        if (response.ok) {
            const instructors = await response.json();
            const tbody = document.getElementById('instructorTableBody');
            tbody.innerHTML = '';
            
            instructors.forEach(i => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${i.name}</td>
                    <td>${i.email}</td>
                    <td>${i.phone}</td>
                    <td>${i.ratings || 'No ratings'}</td>
                    <td>${i.available ? 'Available' : 'Unavailable'}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editInstructor(${i.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteInstructor(${i.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            showError('Failed to load instructors');
        }
    } catch (error) {
        console.error('Error loading instructors:', error);
        showError('An error occurred while loading instructors');
    }
}

function showAddInstructorModal() {
    document.getElementById('instructorModalTitle').textContent = 'Add Instructor';
    document.getElementById('instructorForm').reset();
    document.getElementById('instructorId').value = '';
    const modal = new bootstrap.Modal(document.getElementById('instructorModal'));
    modal.show();
}

// Booking page functionality
async function loadAvailableAircraft() {
    try {
        const response = await fetch('/api/available-aircraft');
        if (response.ok) {
            const aircraft = await response.json();
            displayAircraft(aircraft);
        } else {
            showError('Failed to load available aircraft');
        }
    } catch (error) {
        console.error('Error loading aircraft:', error);
        showError('An error occurred while loading aircraft');
    }
}

async function loadAvailableInstructors() {
    try {
        const response = await fetch('/api/available-instructors');
        if (response.ok) {
            const instructors = await response.json();
            displayInstructors(instructors);
        } else {
            showError('Failed to load available instructors');
        }
    } catch (error) {
        console.error('Error loading instructors:', error);
        showError('An error occurred while loading instructors');
    }
}

function displayAircraft(aircraft) {
    const listContainer = document.getElementById('aircraftList');
    if (!listContainer) return;

    listContainer.innerHTML = '';
    aircraft.forEach(plane => {
        const status = plane.status || plane.availability || 'available';
        const item = document.createElement('div');
        item.className = `list-group-item list-group-item-action ${status === 'available' ? '' : 'disabled'}`;
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between align-items-center">
                <div>
                    <input type="radio" name="aircraft" value="${plane.id}" class="form-check-input me-2"
                           ${status === 'available' ? '' : 'disabled'}>
                    <strong>${plane.make_model}</strong> (${plane.tail_number})
                </div>
                <span class="badge ${status === 'available' ? 'bg-success' : 'bg-warning'}">
                    ${status === 'available' ? 'Available' : 'Unavailable'}
                </span>
            </div>
            <small class="text-muted">${plane.type || 'N/A'}</small>
        `;
        listContainer.appendChild(item);
    });
}

function displayInstructors(instructors) {
    const listContainer = document.getElementById('instructorList');
    if (!listContainer) return;

    listContainer.innerHTML = '';
    instructors.forEach(instructor => {
        const status = instructor.status || instructor.availability || 'available';
        const item = document.createElement('div');
        item.className = `list-group-item list-group-item-action ${status === 'available' ? '' : 'disabled'}`;
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between align-items-center">
                <div>
                    <input type="radio" name="instructor" value="${instructor.id}" class="form-check-input me-2"
                           ${status === 'available' ? '' : 'disabled'}>
                    <strong>${instructor.name}</strong>
                </div>
                <span class="badge ${status === 'available' ? 'bg-success' : 'bg-warning'}">
                    ${status === 'available' ? 'Available' : 'Unavailable'}
                </span>
            </div>
            <small class="text-muted">${instructor.email} | ${instructor.phone || 'N/A'}</small>
        `;
        listContainer.appendChild(item);
    });
} 