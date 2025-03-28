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
                <span class="badge ${booking.status === 'cancelled' ? 'bg-danger' : 'bg-success'}">
                    ${booking.status === 'cancelled' ? 'Cancelled' : 'Confirmed'}
                </span>
            </td>
            <td>
                ${booking.status !== 'cancelled' ? `
                    <button type="button" class="btn btn-link text-primary p-0 me-2" onclick="editBooking(${booking.id})" 
                            title="Edit booking">
                        <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button type="button" class="btn btn-link text-danger p-0" onclick="deleteBooking(${booking.id})"
                            title="Cancel booking">
                        <i class="bi bi-trash-fill"></i>
                    </button>
                ` : ''}
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
    if (!selectedAircraft || !selectedInstructor) {
        showError('Please select both an aircraft and an instructor');
        return;
    }

    // Get the selected date and times
    const dateInput = document.getElementById('bookingDate');
    const startTimeInput = document.getElementById('startTimeInput');
    const endTimeInput = document.getElementById('endTimeInput');
    
    // Create full datetime strings
    const startDateTime = new Date(dateInput.value + 'T' + startTimeInput.value);
    const endDateTime = new Date(dateInput.value + 'T' + endTimeInput.value);
    
    // First, check if the selected resources are still available
    checkAvailability(startDateTime, endDateTime)
        .then(availabilityData => {
            const selectedAircraftAvailable = availabilityData.aircraft.find(a => a.id === selectedAircraft)?.available;
            const selectedInstructorAvailable = availabilityData.instructors.find(i => i.id === selectedInstructor)?.available;

            // Set the values in the booking modal
            const startTimeField = document.getElementById('startTime');
            const endTimeField = document.getElementById('endTime');
            const aircraftSelect = document.getElementById('aircraftSelect');
            const instructorSelect = document.getElementById('instructorSelect');
            const selectedAircraftText = document.getElementById('selectedAircraftText');
            const selectedInstructorText = document.getElementById('selectedInstructorText');

            // Set datetime values
            startTimeField.value = startDateTime.toISOString().slice(0, 16);
            endTimeField.value = endDateTime.toISOString().slice(0, 16);

            // Get the selected objects
            const selectedAircraftObj = aircraft.find(a => a.id === selectedAircraft);
            const selectedInstructorObj = instructors.find(i => i.id === selectedInstructor);

            // Set the form values
            aircraftSelect.value = selectedAircraft;
            instructorSelect.value = selectedInstructor;
            selectedAircraftText.textContent = `${selectedAircraftObj.make_model} (${selectedAircraftObj.tail_number})`;
            selectedInstructorText.textContent = selectedInstructorObj.name;

            // If either resource is no longer available, show warning and enable editing
            if (!selectedAircraftAvailable || !selectedInstructorAvailable) {
                showWarning('One or more selected resources are no longer available for the chosen time slot. Please adjust your selection.');
                
                // Enable editing of date/time fields
                startTimeField.removeAttribute('readonly');
                endTimeField.removeAttribute('readonly');
                
                // Show the aircraft and instructor dropdowns instead of text
                document.getElementById('aircraftSelectContainer').style.display = 'block';
                document.getElementById('instructorSelectContainer').style.display = 'block';
                document.getElementById('selectedAircraftText').style.display = 'none';
                document.getElementById('selectedInstructorText').style.display = 'none';

                // Populate the dropdowns with available options
                populateBookingFormSelects(availabilityData.aircraft, availabilityData.instructors);
            } else {
                // Resources are available, keep fields readonly
                startTimeField.setAttribute('readonly', true);
                endTimeField.setAttribute('readonly', true);
                
                // Show the text displays instead of dropdowns
                document.getElementById('aircraftSelectContainer').style.display = 'none';
                document.getElementById('instructorSelectContainer').style.display = 'none';
                document.getElementById('selectedAircraftText').style.display = 'block';
                document.getElementById('selectedInstructorText').style.display = 'block';
            }

            // Show the modal
            const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error checking availability:', error);
            showError('Failed to verify resource availability');
        });
}

async function checkAvailability(startDateTime, endDateTime) {
    try {
        const response = await fetch('/api/check-availability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_time: startDateTime.toISOString(),
                end_time: endDateTime.toISOString()
            })
        });

        if (!response.ok) {
            throw new Error('Failed to check availability');
        }

        return await response.json();
    } catch (error) {
        console.error('Error checking availability:', error);
        throw error;
    }
}

function populateBookingFormSelects(availableAircraft, availableInstructors) {
    const aircraftSelect = document.getElementById('aircraftSelect');
    const instructorSelect = document.getElementById('instructorSelect');

    // Populate aircraft dropdown
    aircraftSelect.innerHTML = availableAircraft
        .map(a => `<option value="${a.id}" ${!a.available ? 'disabled' : ''}>${a.make_model} (${a.tail_number})${!a.available ? ' - Unavailable' : ''}</option>`)
        .join('');

    // Populate instructor dropdown
    instructorSelect.innerHTML = availableInstructors
        .map(i => `<option value="${i.id}" ${!i.available ? 'disabled' : ''}>${i.name}${!i.available ? ' - Unavailable' : ''}</option>`)
        .join('');
}

function showWarning(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.modal-body').insertBefore(alertDiv, document.querySelector('.modal-body').firstChild);
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

    // Set default date and time for booking
    const bookingDate = document.getElementById('bookingDate');
    const startTimeInput = document.getElementById('startTimeInput');
    const durationSelect = document.getElementById('durationSelect');
    
    if (bookingDate && startTimeInput) {
        // Set today's date as default
        const today = new Date();
        bookingDate.value = formatDateForInput(today);
        
        // Set current time rounded to next 15 minutes as default
        const roundedTime = roundToNearest15Minutes(new Date());
        startTimeInput.value = formatTimeForInput(roundedTime);
        
        // Calculate initial end time
        updateEndTime();
        
        // Add event listeners for time updates
        startTimeInput.addEventListener('change', updateEndTime);
        durationSelect.addEventListener('change', updateEndTime);
        bookingDate.addEventListener('change', updateEndTime);
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
    
    // Get ratings input and convert to array, filtering out invalid ones
    const ratingsInput = document.getElementById('instructorRatings').value;
    const ratings = ratingsInput
        .split(',')
        .map(r => r.trim())
        .filter(r => r.length >= 2);  // Only keep ratings that are at least 2 chars
    
    const data = {
        name: document.getElementById('instructorName').value,
        email: document.getElementById('instructorEmail').value,
        phone: document.getElementById('instructorPhone').value,
        ratings: ratings  // Send as array
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
                // Create badges for each rating with consistent styling
                const ratingBadges = Array.isArray(i.ratings) && i.ratings.length > 0
                    ? i.ratings.map(rating => {
                        let badgeClass = 'bg-secondary';
                        if (rating === 'CFI') badgeClass = 'bg-primary';
                        else if (rating === 'CFII') badgeClass = 'bg-info';
                        else if (rating === 'MEI') badgeClass = 'bg-success';
                        else if (rating.endsWith('GI')) badgeClass = 'bg-warning text-dark';
                        return `<span class="badge ${badgeClass} me-1">${rating}</span>`;
                    }).join('')
                    : '<span class="text-muted">No ratings</span>';
                
                row.innerHTML = `
                    <td>${i.name}</td>
                    <td>${i.email}</td>
                    <td>${i.phone}</td>
                    <td>${ratingBadges}</td>
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
    const tableBody = document.querySelector('#aircraftTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = aircraft.map(a => `
        <tr class="${selectedAircraft === a.id ? 'selected-row' : ''} ${!a.available ? 'text-muted' : ''}" 
            onclick="${a.available ? `selectAircraft(${a.id}, this)` : ''}" 
            style="cursor: ${a.available ? 'pointer' : 'not-allowed'}">
            <td>
                <input type="radio" name="aircraft" value="${a.id}" 
                    ${selectedAircraft === a.id ? 'checked' : ''}
                    ${!a.available ? 'disabled' : ''}>
            </td>
            <td>${a.make_model}</td>
            <td>${a.tail_number}</td>
            <td>${a.type}</td>
        </tr>
    `).join('');

    // Add click event listeners to rows
    tableBody.querySelectorAll('tr').forEach(row => {
        if (!row.classList.contains('text-muted')) {
            row.addEventListener('click', function() {
                const radioBtn = this.querySelector('input[type="radio"]');
                if (radioBtn && !radioBtn.disabled) {
                    selectAircraft(parseInt(radioBtn.value), this);
                }
            });
        }
    });
}

function displayInstructors(instructors) {
    const tableBody = document.querySelector('#instructorsTableBody');
    if (!tableBody) return;

    if (!instructors || instructors.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No instructors available</td></tr>';
        return;
    }

    tableBody.innerHTML = instructors.map(i => {
        // Create badges for each rating - ensure ratings is treated as an array
        const ratingBadges = Array.isArray(i.ratings) && i.ratings.length > 0 
            ? i.ratings.map(rating => {
                // Color-code badges based on rating type
                let badgeClass = 'bg-secondary';
                if (rating === 'CFI') badgeClass = 'bg-primary';
                else if (rating === 'CFII') badgeClass = 'bg-info';
                else if (rating === 'MEI') badgeClass = 'bg-success';
                else if (rating.endsWith('GI')) badgeClass = 'bg-warning text-dark'; // Ground instructor ratings
                return `<span class="badge ${badgeClass} me-1">${rating}</span>`;
            }).join('') 
            : '<span class="text-muted">No ratings</span>';

        return `
            <tr class="${selectedInstructor === i.id ? 'selected-row' : ''} ${!i.available ? 'text-muted' : ''}" 
                onclick="${i.available ? `selectInstructor(${i.id}, this)` : ''}" 
                style="cursor: ${i.available ? 'pointer' : 'not-allowed'}">
                <td>
                    <input type="radio" name="instructor" value="${i.id}" 
                        ${selectedInstructor === i.id ? 'checked' : ''}
                        ${!i.available ? 'disabled' : ''}>
                </td>
                <td>${i.name}</td>
                <td>${i.email}</td>
                <td>${i.phone}</td>
                <td>${ratingBadges}</td>
            </tr>
        `;
    }).join('');

    // Add click event listeners to the rows
    tableBody.querySelectorAll('tr').forEach(row => {
        if (!row.classList.contains('text-muted')) {
            row.addEventListener('click', function() {
                const id = parseInt(row.querySelector('input[type="radio"]').value);
                selectInstructor(id, row);
            });
        }
    });
}

async function saveBooking() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const aircraftId = document.getElementById('aircraftSelect').value;
    const instructorId = document.getElementById('instructorSelect').value;
    
    const data = {
        start_time: startTime,
        end_time: endTime,
        aircraft_id: parseInt(aircraftId),
        instructor_id: parseInt(instructorId),
        status: 'confirmed'  // Explicitly set status to confirmed
    };
    
    try {
        const response = await fetch('/api/bookings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const responseData = await response.json();
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
            await loadData();  // Reload all data
            showSuccess('Booking created successfully');
            selectedAircraft = null;
            selectedInstructor = null;
            await checkAvailabilityAndBook(false);  // Refresh availability
        } else {
            showError(responseData.error || 'Failed to create booking');
        }
    } catch (error) {
        console.error('Error creating booking:', error);
        showError('Failed to create booking');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Login link
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            showLoginModal();
        });
    }

    // Register link
    const registerLink = document.getElementById('register-link');
    if (registerLink) {
        registerLink.addEventListener('click', function(e) {
            e.preventDefault();
            showRegisterModal();
        });
    }

    // Logout link
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/logout';
        });
    }

    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const credentials = {
                email: document.getElementById('loginEmail').value,
                password: document.getElementById('loginPassword').value
            };
            loginUser(credentials);
        });
    }

    // Register form with password validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const registerPassword = document.getElementById('registerPassword');
        const registerPasswordConfirm = document.getElementById('registerPasswordConfirm');

        // Add password strength check on input
        if (registerPassword) {
            registerPassword.addEventListener('input', function() {
                const result = checkPasswordStrength(this.value);
                let feedback = this.nextElementSibling;
                if (!feedback || !feedback.classList.contains('form-text')) {
                    feedback = document.createElement('div');
                    feedback.className = 'form-text';
                    this.parentNode.insertBefore(feedback, this.nextSibling);
                }
                
                if (result.strength < 5) {
                    feedback.className = 'form-text text-danger';
                    feedback.textContent = `Password must include: ${result.requirements.join(', ')}`;
                } else {
                    feedback.className = 'form-text text-success';
                    feedback.textContent = 'Password strength: Excellent';
                }
            });
        }

        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const password = registerPassword.value;
            const confirmPassword = registerPasswordConfirm.value;
            
            // Check password strength
            const strengthResult = checkPasswordStrength(password);
            if (strengthResult.strength < 5) {
                showError(`Password is not strong enough. ${strengthResult.requirements.join(', ')}`);
                return;
            }
            
            // Check password match
            if (password !== confirmPassword) {
                showError('Passwords do not match');
                return;
            }

            const userData = {
                first_name: document.getElementById('registerFirstName').value,
                last_name: document.getElementById('registerLastName').value,
                email: document.getElementById('registerEmail').value,
                password: password
            };
            registerUser(userData);
        });
    }

    // Password Reset form
    const resetPasswordForm = document.getElementById('resetPasswordForm');
    if (resetPasswordForm) {
        resetPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('resetEmail').value;
            requestPasswordReset(email);
        });
    }

    // New Password form with validation
    const newPasswordForm = document.getElementById('newPasswordForm');
    if (newPasswordForm) {
        const newPassword = document.getElementById('newPassword');
        const newPasswordConfirm = document.getElementById('newPasswordConfirm');

        // Add password strength check on input
        if (newPassword) {
            newPassword.addEventListener('input', function() {
                const result = checkPasswordStrength(this.value);
                let feedback = this.nextElementSibling;
                if (!feedback || !feedback.classList.contains('form-text')) {
                    feedback = document.createElement('div');
                    feedback.className = 'form-text';
                    this.parentNode.insertBefore(feedback, this.nextSibling);
                }
                
                if (result.strength < 5) {
                    feedback.className = 'form-text text-danger';
                    feedback.textContent = `Password must include: ${result.requirements.join(', ')}`;
                } else {
                    feedback.className = 'form-text text-success';
                    feedback.textContent = 'Password strength: Excellent';
                }
            });
        }

        newPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const password = newPassword.value;
            const confirmPassword = newPasswordConfirm.value;
            
            // Check password strength
            const strengthResult = checkPasswordStrength(password);
            if (strengthResult.strength < 5) {
                showError(`Password is not strong enough. ${strengthResult.requirements.join(', ')}`);
                return;
            }
            
            // Check password match
            if (password !== confirmPassword) {
                showError('Passwords do not match');
                return;
            }

            // Get token from URL
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get('token');
            if (!token) {
                showError('Password reset token is missing');
                return;
            }

            resetPassword(token, password);
        });
    }

    // Initialize any Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize any Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Time handling functions
function roundToNearest15Minutes(date) {
    const minutes = date.getMinutes();
    const roundedMinutes = Math.ceil(minutes / 15) * 15;
    date.setMinutes(roundedMinutes);
    date.setSeconds(0);
    date.setMilliseconds(0);
    return date;
}

function formatTimeForInput(date) {
    return date.toTimeString().substring(0, 5);
}

function formatDateForInput(date) {
    return date.toISOString().split('T')[0];
}

function calculateEndTime(startTime, durationHours) {
    const endTime = new Date(startTime);
    endTime.setMinutes(endTime.getMinutes() + (durationHours * 60));
    return endTime;
}

function updateEndTime() {
    const startTimeInput = document.getElementById('startTimeInput');
    const endTimeInput = document.getElementById('endTimeInput');
    const durationSelect = document.getElementById('durationSelect');
    const bookingDate = document.getElementById('bookingDate');

    if (startTimeInput.value && durationSelect.value && bookingDate.value) {
        const [hours, minutes] = startTimeInput.value.split(':');
        const startTime = new Date(bookingDate.value);
        startTime.setHours(parseInt(hours), parseInt(minutes));
        
        const endTime = calculateEndTime(startTime, parseFloat(durationSelect.value));
        endTimeInput.value = formatTimeForInput(endTime);
    }
}

// Update the edit instructor function to handle ratings properly
function editInstructor(id) {
    const instructor = instructors.find(i => i.id === id);
    if (!instructor) return;

    document.getElementById('instructorModalTitle').textContent = 'Edit Instructor';
    document.getElementById('instructorId').value = instructor.id;
    document.getElementById('instructorName').value = instructor.name;
    document.getElementById('instructorEmail').value = instructor.email;
    document.getElementById('instructorPhone').value = instructor.phone;
    // Join ratings array with commas for the input field
    document.getElementById('instructorRatings').value = Array.isArray(instructor.ratings) 
        ? instructor.ratings.join(', ')
        : '';

    const modal = new bootstrap.Modal(document.getElementById('instructorModal'));
    modal.show();
} 