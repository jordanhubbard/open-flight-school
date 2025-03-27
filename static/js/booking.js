// Global variables
let aircraft = [];
let instructors = [];
let selectedAircraft = null;
let selectedInstructor = null;

// Booking page functionality
async function loadAvailableAircraft() {
    try {
        const response = await fetch('/api/available-aircraft');
        if (!response.ok) {
            throw new Error('Failed to load available aircraft');
        }
        aircraft = await response.json();
        console.log('Loaded aircraft:', aircraft); // Debug log
        displayAircraft();
    } catch (error) {
        console.error('Error loading aircraft:', error);
        showError('An error occurred while loading aircraft');
    }
}

async function loadAvailableInstructors() {
    try {
        const response = await fetch('/api/available-instructors');
        if (!response.ok) {
            throw new Error('Failed to load available instructors');
        }
        instructors = await response.json();
        console.log('Loaded instructors:', instructors); // Debug log
        displayInstructors();
    } catch (error) {
        console.error('Error loading instructors:', error);
        showError('An error occurred while loading instructors');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded, initializing...'); // Debug log
    
    // Load initial data
    await Promise.all([
        loadAvailableAircraft(),
        loadAvailableInstructors()
    ]);
    
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

    // Setup table navigation
    setupTableNavigation('aircraftTableScroll', 'aircraftScrollUp', 'aircraftScrollDown');
    setupTableNavigation('instructorsTableScroll', 'instructorsScrollUp', 'instructorsScrollDown');
    
    // Initial availability check
    await checkAvailabilityAndBook(false);
});

function updateEndTime() {
    const startTimeInput = document.getElementById('startTimeInput');
    const durationSelect = document.getElementById('durationSelect');
    const endTimeInput = document.getElementById('endTimeInput');
    
    if (startTimeInput.value) {
        const [hours, minutes] = startTimeInput.value.split(':');
        const startDate = new Date();
        startDate.setHours(parseInt(hours), parseInt(minutes), 0);
        
        const duration = parseFloat(durationSelect.value);
        const durationMs = duration * 60 * 60 * 1000;
        
        const endDate = new Date(startDate.getTime() + durationMs);
        endTimeInput.value = endDate.toTimeString().slice(0, 5);
    }
}

async function checkAvailabilityOnChange() {
    // Reset selections when time changes
    selectedAircraft = null;
    selectedInstructor = null;
    
    // Check availability with the new time
    await checkAvailabilityAndBook(false); // Pass false to prevent showing "no availability" error
}

async function checkAvailabilityAndBook(showErrors = true) {
    const dateInput = document.getElementById('bookingDate');
    const startTimeInput = document.getElementById('startTimeInput');
    const endTimeInput = document.getElementById('endTimeInput');
    
    if (!dateInput.value || !startTimeInput.value || !endTimeInput.value) {
        if (showErrors) {
            showError('Please select a date, start time, and duration');
        }
        return;
    }
    
    // Create local datetime objects
    const startDateTime = new Date(dateInput.value + 'T' + startTimeInput.value);
    const endDateTime = new Date(dateInput.value + 'T' + endTimeInput.value);
    
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
        
        const availabilityData = await response.json();
        
        // Update aircraft and instructors with availability information
        aircraft = availabilityData.aircraft;
        instructors = availabilityData.instructors;
        
        // Update displays
        displayAircraft();
        displayInstructors();
        
        if (showErrors && (!aircraft.some(a => a.available) || !instructors.some(i => i.available))) {
            showError('No available aircraft or instructors for the selected time slot');
            return;
        }
        
    } catch (error) {
        console.error('Error checking availability:', error);
        if (showErrors) {
            showError('Failed to check availability');
        }
    }
}

function displayAircraft() {
    const tableBody = document.querySelector('#aircraftTableBody');
    if (!tableBody) return;

    if (!aircraft || aircraft.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No aircraft available</td></tr>';
        return;
    }

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

    // Add click event listeners to the rows
    tableBody.querySelectorAll('tr').forEach(row => {
        if (!row.classList.contains('text-muted')) {
            row.addEventListener('click', function() {
                const id = parseInt(row.querySelector('input[type="radio"]').value);
                selectAircraft(id, row);
            });
        }
    });
}

function displayInstructors() {
    const tableBody = document.querySelector('#instructorsTableBody');
    if (!tableBody) return;

    if (!instructors || instructors.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No instructors available</td></tr>';
        return;
    }

    tableBody.innerHTML = instructors.map(i => {
        // Create badges from ratings array - each rating is a complete string
        const ratingBadges = Array.isArray(i.ratings) && i.ratings.length > 0 
            ? i.ratings.map(rating => `<span class="badge bg-secondary me-1">${rating.trim()}</span>`).join('') 
            : '<span class="text-muted">N/A</span>';

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

function selectAircraft(id, row) {
    // Remove selection from all aircraft rows
    document.querySelectorAll('#aircraftTableBody tr').forEach(tr => {
        tr.classList.remove('selected-row');
    });
    
    // Add selection to clicked row
    row.classList.add('selected-row');
    
    // Update the selected aircraft
    selectedAircraft = id;
    
    // Update radio button
    const radio = row.querySelector('input[type="radio"]');
    if (radio) {
        radio.checked = true;
    }
}

function selectInstructor(id, row) {
    // Remove selection from all instructor rows
    document.querySelectorAll('#instructorsTableBody tr').forEach(tr => {
        tr.classList.remove('selected-row');
    });
    
    // Add selection to clicked row
    row.classList.add('selected-row');
    
    // Update the selected instructor
    selectedInstructor = id;
    
    // Update radio button
    const radio = row.querySelector('input[type="radio"]');
    if (radio) {
        radio.checked = true;
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
    
    if (!dateInput.value || !startTimeInput.value || !endTimeInput.value) {
        showError('Please select a date, start time, and duration');
        return;
    }

    // Parse the date and time inputs
    const [startHours, startMinutes] = startTimeInput.value.split(':').map(Number);
    const [endHours, endMinutes] = endTimeInput.value.split(':').map(Number);
    
    // Create Date objects for start and end times
    const startDateTime = new Date(dateInput.value);
    startDateTime.setHours(startHours, startMinutes, 0, 0);
    
    const endDateTime = new Date(dateInput.value);
    endDateTime.setHours(endHours, endMinutes, 0, 0);
    
    // If end time is before start time, assume it's the next day
    if (endDateTime < startDateTime) {
        endDateTime.setDate(endDateTime.getDate() + 1);
    }

    // Format for display in the modal
    const modalStartTime = document.getElementById('startTime');
    const modalEndTime = document.getElementById('endTime');
    
    modalStartTime.value = startDateTime.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
    
    modalEndTime.value = endDateTime.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
    
    // Set selected aircraft and instructor
    const selectedAircraftObj = aircraft.find(a => a.id === selectedAircraft);
    const selectedInstructorObj = instructors.find(i => i.id === selectedInstructor);
    
    document.getElementById('selectedAircraftText').textContent = 
        `${selectedAircraftObj.make_model} (${selectedAircraftObj.tail_number})`;
    document.getElementById('selectedInstructorText').textContent = 
        selectedInstructorObj.name;
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
    modal.show();
}

function displayBookings() {
    const tableBody = document.querySelector('#bookingsTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = bookings.map(booking => {
        // Convert UTC dates to local time
        const startTime = new Date(booking.start_time);
        const endTime = new Date(booking.end_time);
        
        // Format date and time in local timezone
        const date = startTime.toLocaleDateString('en-US', { 
            weekday: 'short', 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
        
        const timeRange = `${startTime.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit'
        })} - ${endTime.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit'
        })}`;

        // Status badge styling - only confirmed or cancelled
        const statusClass = booking.status === 'cancelled' ? 'bg-danger' : 'bg-success';
        const statusText = booking.status === 'cancelled' ? 'Cancelled' : 'Confirmed';

        // Get aircraft and instructor names from the booking data
        const aircraftName = booking.aircraft || 'Not selected';
        const instructorName = booking.instructor || 'Not selected';

        return `
            <tr>
                <td>${date}</td>
                <td>${timeRange}</td>
                <td>${aircraftName}</td>
                <td>${instructorName}</td>
                <td><span class="badge ${statusClass}">${statusText}</span></td>
                <td>
                    ${booking.status !== 'cancelled' ? `
                        <button class="btn btn-link btn-sm p-0 me-2" onclick="editBooking(${booking.id})" title="Edit booking">
                            <i class="bi bi-pencil text-primary"></i>
                        </button>
                        <button class="btn btn-link btn-sm p-0" onclick="confirmDelete(${booking.id})" title="Cancel booking">
                            <i class="bi bi-trash text-danger"></i>
                        </button>
                    ` : ''}
                </td>
            </tr>
        `;
    }).join('');
}

function initializeCalendar() {
    const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'timeGridWeek,timeGridDay,dayGridMonth',
            center: 'title',
            right: 'prev,next today'
        },
        slotMinTime: '06:00:00',
        slotMaxTime: '22:00:00',
        allDaySlot: false,
        nowIndicator: true,
        scrollTime: '08:00:00',
        timeZone: 'local',
        events: function(info, successCallback, failureCallback) {
            fetch('/api/bookings')
                .then(response => response.json())
                .then(data => {
                    const events = data.map(booking => ({
                        title: `${booking.aircraft} - ${booking.instructor}`,
                        start: new Date(booking.start_time),
                        end: new Date(booking.end_time),
                        color: booking.status === 'confirmed' ? '#28a745' : '#dc3545'
                    }));
                    successCallback(events);
                })
                .catch(error => {
                    console.error('Error fetching bookings:', error);
                    failureCallback(error);
                });
        }
    });
    calendar.render();
}

function formatDateTimeForInput(date) {
    // Format date as YYYY-MM-DD
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function formatTimeForInput(date) {
    // Format time as HH:mm in 24-hour format
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

function populateSelects() {
    const aircraftSelect = document.getElementById('aircraftSelect');
    const instructorSelect = document.getElementById('instructorSelect');
    const editAircraftSelect = document.getElementById('editAircraftSelect');
    const editInstructorSelect = document.getElementById('editInstructorSelect');
    
    if (aircraftSelect) {
        aircraftSelect.innerHTML = aircraft.map(a => `
            <option value="${a.id}">${a.make_model} (${a.tail_number})</option>
        `).join('');
    }
    
    if (instructorSelect) {
        instructorSelect.innerHTML = instructors.map(i => `
            <option value="${i.id}">${i.name}</option>
        `).join('');
    }
    
    if (editAircraftSelect) {
        editAircraftSelect.innerHTML = aircraft.map(a => `
            <option value="${a.id}">${a.make_model} (${a.tail_number})</option>
        `).join('');
    }
    
    if (editInstructorSelect) {
        editInstructorSelect.innerHTML = instructors.map(i => `
            <option value="${i.id}">${i.name}</option>
        `).join('');
    }
}

function confirmDelete(id) {
    if (confirm('Are you sure you want to cancel this flight?')) {
        cancelBooking(id);
    }
}

async function cancelBooking(id) {
    try {
        const response = await fetch(`/api/bookings/${id}/cancel`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadData();
            showSuccess('Booking cancelled successfully');
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to cancel booking');
        }
    } catch (error) {
        console.error('Error cancelling booking:', error);
        showError('Failed to cancel booking');
    }
}

function editBooking(id) {
    const booking = bookings.find(b => b.id === id);
    if (!booking) return;
    
    // Convert UTC dates to local datetime-local input format
    const startDate = new Date(booking.start_time);
    const endDate = new Date(booking.end_time);
    
    document.getElementById('editBookingId').value = booking.id;
    document.getElementById('editStartTime').value = startDate.toISOString().slice(0, 16);
    document.getElementById('editEndTime').value = endDate.toISOString().slice(0, 16);
    document.getElementById('editAircraftSelect').value = booking.aircraft_id || '';
    document.getElementById('editInstructorSelect').value = booking.instructor_id || '';
    
    new bootstrap.Modal(document.getElementById('editBookingModal')).show();
}

function saveBooking() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    
    // Convert display format back to ISO format for API
    const startDate = new Date(startTime);
    const endDate = new Date(endTime);
    
    const booking = {
        start_time: startDate.toISOString(),
        end_time: endDate.toISOString(),
        aircraft_id: selectedAircraft,
        instructor_id: selectedInstructor
    };
    
    fetch('/api/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(booking)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Failed to create booking'); });
        }
        return response.json();
    })
    .then(data => {
        showSuccess('Booking created successfully!');
        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('bookingModal'));
        modal.hide();
        // Refresh the bookings list and availability
        getBookings();
        checkAvailability();
    })
    .catch(error => {
        showError(error.message);
    });
}

async function loadData() {
    try {
        // Load bookings
        const bookingsResponse = await fetch('/api/bookings');
        if (!bookingsResponse.ok) throw new Error('Failed to load bookings');
        bookings = await bookingsResponse.json();
        
        // Display bookings and initialize calendar
        displayBookings();
        initializeCalendar();
        
        // Also refresh availability
        await checkAvailabilityAndBook(false);
        
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Failed to load data');
    }
}

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
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.insertBefore(errorDiv, document.body.firstChild);
}

function setupTableNavigation(scrollContainerId, upButtonId, downButtonId) {
    const container = document.getElementById(scrollContainerId);
    const upButton = document.getElementById(upButtonId);
    const downButton = document.getElementById(downButtonId);
    const scrollAmount = 80; // Adjust scroll amount for smoother navigation

    function updateButtonStates() {
        if (!container || !upButton || !downButton) return;
        
        const scrollTop = container.scrollTop;
        const scrollHeight = container.scrollHeight;
        const clientHeight = container.clientHeight;
        
        // Show/hide up button
        upButton.disabled = scrollTop <= 0;
        
        // Show/hide down button
        downButton.disabled = Math.abs(scrollHeight - clientHeight - scrollTop) < 1;
    }

    if (upButton) {
        upButton.addEventListener('click', () => {
            container.scrollBy({
                top: -scrollAmount,
                behavior: 'smooth'
            });
            // Update button states after animation
            setTimeout(updateButtonStates, 400);
        });
    }

    if (downButton) {
        downButton.addEventListener('click', () => {
            container.scrollBy({
                top: scrollAmount,
                behavior: 'smooth'
            });
            // Update button states after animation
            setTimeout(updateButtonStates, 400);
        });
    }

    if (container) {
        // Update button states on scroll
        container.addEventListener('scroll', updateButtonStates);
        
        // Initial button state
        updateButtonStates();
        
        // Update button states when content changes
        const observer = new MutationObserver(updateButtonStates);
        observer.observe(container, { childList: true, subtree: true });
    }
}

// Load data when the page loads
document.addEventListener('DOMContentLoaded', loadData); 