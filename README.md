# Eyes Outside Flight School

A web application for managing flight school bookings, aircraft, and instructors.

## Features

- User registration and authentication
- Aircraft and instructor management
- Real-time booking system with conflict detection
- Email notifications for booking confirmations
- Admin dashboard for managing resources
- Responsive design for all devices

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- make (for using the Makefile)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eyes-outside.git
cd eyes-outside
```

2. Create a virtual environment and install dependencies:
```bash
make setup
```

3. Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///flight_school.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
```

## Running the Application

1. Start the development server:
```bash
make run
```

2. Open your web browser and navigate to `http://localhost:5000`

## Testing

Run the test suite:
```bash
make test
```

## Development

The project structure is organized as follows:

```
eyes-outside/
├── app.py              # Main application file
├── models.py           # Database models
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── Makefile           # Build automation
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── tests/            # Test files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
