# Open Flight School

A web application for managing flight school operations, including aircraft scheduling, instructor management, and student bookings.

## Features

- User authentication and authorization
- Aircraft management
- Instructor management
- Student booking system
- Email notifications
- Admin dashboard

## Prerequisites

- Docker and Docker Compose
- Make

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/open-flight-school.git
   cd open-flight-school
   ```

2. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your configuration:
   ```bash
   # Database configuration
   DATABASE_URL=postgresql://postgres:postgres@db:5432/flight_school
   
   # Email configuration
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-specific-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

4. Build and start the containers:
   ```bash
   make build
   make init
   make test-data
   make run
   ```

5. Access the application at http://localhost:5000

## Development

### Running Tests

```bash
make test
```

### Code Quality

```bash
make lint
make format
```

### Documentation

```bash
make docs
make serve-docs
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
