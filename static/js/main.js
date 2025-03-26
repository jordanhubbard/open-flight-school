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
            showError('Failed to fetch bookings');
        }
    } catch (error) {
        showError('An error occurred while fetching bookings');
    }
}

async function createBooking(bookingData) {
    try {
        const response = await fetch('/api/bookings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        if (response.ok) {
            showSuccess('Booking created successfully!');
            getBookings();
        } else {
            showError(data.error || 'Failed to create booking');
        }
    } catch (error) {
        showError('An error occurred while creating the booking');
    }
}

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

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Login button handler
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault();
            showLoginModal();
        });
    }
    
    // Register button handler
    const registerLink = document.getElementById('register-link');
    if (registerLink) {
        registerLink.addEventListener('click', function(e) {
            e.preventDefault();
            showRegisterModal();
        });
    }
    
    // Logout button handler
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/logout';
        });
    }
    
    // Bookings link handler
    const bookingsLink = document.getElementById('bookings-link');
    if (bookingsLink) {
        bookingsLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/bookings';
        });
    }

    // Register Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        console.log('Register form found, adding submit handler');
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Registration form submitted');
            
            const firstName = document.getElementById('registerFirstName');
            const lastName = document.getElementById('registerLastName');
            const email = document.getElementById('registerEmail');
            const password = document.getElementById('registerPassword');
            const confirmPassword = document.getElementById('registerPasswordConfirm');
            
            console.log('Form elements found:', {
                firstName: firstName ? 'yes' : 'no',
                lastName: lastName ? 'yes' : 'no',
                email: email ? 'yes' : 'no',
                password: password ? 'yes' : 'no',
                confirmPassword: confirmPassword ? 'yes' : 'no'
            });
            
            if (!firstName || !lastName || !email || !password || !confirmPassword) {
                console.error('One or more form elements not found');
                showError('Form error: Please fill in all fields');
                return;
            }
            
            const firstNameValue = firstName.value;
            const lastNameValue = lastName.value;
            const emailValue = email.value;
            const passwordValue = password.value;
            const confirmPasswordValue = confirmPassword.value;
            
            console.log('Form values:', {
                firstName: firstNameValue,
                lastName: lastNameValue,
                email: emailValue,
                password: passwordValue ? '***' : '',
                confirmPassword: confirmPasswordValue ? '***' : ''
            });
            
            if (passwordValue !== confirmPasswordValue) {
                console.log('Passwords do not match');
                showError('Passwords do not match');
                return;
            }
            
            const strengthCheck = checkPasswordStrength(passwordValue);
            console.log('Password strength:', strengthCheck.strength);
            if (strengthCheck.strength < 3) {
                console.log('Password too weak');
                const missingRequirements = strengthCheck.requirements.join(', ');
                showError(`Password is too weak. Please include: ${missingRequirements}`);
                return;
            }
            
            const userData = {
                first_name: firstNameValue,
                last_name: lastNameValue,
                email: emailValue,
                password: passwordValue
            };
            
            console.log('Submitting registration data:', {
                ...userData,
                password: '***'
            });
            await registerUser(userData);
        });
    } else {
        console.error('Register form not found in the DOM');
    }
    
    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Login form submitted');
            
            const credentials = {
                email: document.getElementById('loginEmail').value,
                password: document.getElementById('loginPassword').value
            };
            
            console.log('Submitting login credentials:', credentials);
            await loginUser(credentials);
        });
    }

    // Check for password reset token in URL
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
        showNewPasswordModal();
    }

    // Reset Password Form
    const resetPasswordForm = document.getElementById('resetPasswordForm');
    if (resetPasswordForm) {
        resetPasswordForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Reset password form submitted');
            
            const email = document.getElementById('resetEmail').value;
            await requestPasswordReset(email);
        });
    }
    
    // New Password Form
    const newPasswordForm = document.getElementById('newPasswordForm');
    if (newPasswordForm) {
        newPasswordForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('New password form submitted');
            
            const password = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('newPasswordConfirm').value;
            
            if (password !== confirmPassword) {
                showError('Passwords do not match');
                return;
            }
            
            const strength = checkPasswordStrength(password);
            if (strength < 3) {
                showError('Password is too weak. Please include uppercase, lowercase, numbers, and special characters.');
                return;
            }
            
            const token = new URLSearchParams(window.location.search).get('token');
            if (!token) {
                showError('Invalid password reset link');
                return;
            }
            
            await resetPassword(token, password);
        });
    }

    // If we're on the booking page
    if (document.getElementById('bookingForm')) {
        loadAvailableAircraft();
        loadAvailableInstructors();
        getBookings(); // Load existing bookings
        
        // Handle booking form submission
        const bookingForm = document.getElementById('bookingForm');
        bookingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const startTime = document.getElementById('startTime').value;
            const endTime = document.getElementById('endTime').value;
            const aircraftId = document.getElementById('aircraftSelect').value;
            const instructorId = document.getElementById('instructorSelect').value;
            
            const bookingData = {
                start_time: startTime,
                end_time: endTime,
                aircraft_id: aircraftId,
                instructor_id: instructorId
            };
            
            await createBooking(bookingData);
        });
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
                    <td>Available</td>
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
            const select = document.getElementById('aircraftSelect');
            if (select) {
                select.innerHTML = '';
                aircraft.forEach(a => {
                    const option = document.createElement('option');
                    option.value = a.id;
                    option.textContent = `${a.make_model} (${a.tail_number})`;
                    select.appendChild(option);
                });
            }
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
            const select = document.getElementById('instructorSelect');
            if (select) {
                select.innerHTML = '';
                instructors.forEach(i => {
                    const option = document.createElement('option');
                    option.value = i.id;
                    option.textContent = `${i.name} - ${i.ratings || 'No ratings'}`;
                    select.appendChild(option);
                });
            }
        } else {
            showError('Failed to load available instructors');
        }
    } catch (error) {
        console.error('Error loading instructors:', error);
        showError('An error occurred while loading instructors');
    }
}

function displayBookings(bookings) {
    const container = document.getElementById('bookingsList');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (bookings.length === 0) {
        container.innerHTML = '<p class="text-muted">No bookings found.</p>';
        return;
    }
    
    const table = document.createElement('table');
    table.className = 'table table-striped';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Aircraft</th>
                <th>Instructor</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;
    
    const tbody = table.querySelector('tbody');
    bookings.forEach(booking => {
        const startDate = new Date(booking.start_time);
        const endDate = new Date(booking.end_time);
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${startDate.toLocaleDateString()}</td>
            <td>${startDate.toLocaleTimeString()} - ${endDate.toLocaleTimeString()}</td>
            <td>${booking.aircraft || 'N/A'}</td>
            <td>${booking.instructor || 'N/A'}</td>
            <td>${booking.status || 'Pending'}</td>
        `;
        tbody.appendChild(row);
    });
    
    container.appendChild(table);
} 