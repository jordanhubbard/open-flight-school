Development Guide
================

This guide provides detailed information about the development workflow, tools, and best practices for the Open Flight School project.

Development Environment
---------------------

The project uses Docker Compose for consistent development, testing, and production environments. The development environment is managed through Make targets:

1. **Initial Setup**
   ::

     make build        # Build Docker containers
     make init         # Initialize the database
     make test-data    # Load test data

2. **Running the Application**
   ::

     make run         # Start the application
     make test        # Run the test suite
     make clean       # Clean up containers and temporary files

Code Quality Tools
----------------

The project uses several tools to maintain code quality:

1. **Code Formatting (Black)**
   - Enforces consistent code style
   - Run formatting: ``make format``
   - Check formatting: ``make lint``

2. **Linting (Flake8)**
   - Catches potential errors and style issues
   - Run linting: ``make lint``

3. **Testing (Pytest)**
   - Unit and integration tests
   - Run tests: ``make test``
   - Generate coverage report: ``make coverage``

4. **Documentation (Sphinx)**
   - API documentation
   - Build docs: ``make docs``
   - View docs: ``make serve-docs``

Database Management
-----------------

The application uses PostgreSQL for all environments. Database operations are managed through Flask-Migrate:

1. **Initializing the Database**
   ::

     make init

   This will:
   - Create the database
   - Run migrations
   - Set up required extensions

2. **Loading Test Data**
   ::

     make test-data

3. **Cleaning Up**
   ::

     make clean

   This will remove containers, volumes, and temporary files.

Development Workflow
-----------------

1. **Starting Development**
   ::

     make build        # Build containers
     make init         # Initialize database
     make test-data    # Load test data
     make run         # Start the application

2. **Making Changes**
   - Write code following the project's style guide
   - Run ``make format`` to format your code
   - Run ``make lint`` to check for issues
   - Write tests for new features
   - Run ``make test`` to verify changes

3. **Database Changes**
   - Modify models as needed
   - Create and apply migrations
   - Update test data if necessary

4. **Documentation**
   - Update docstrings following Google style
   - Build and check documentation
   - Update API documentation

5. **Pre-commit Checklist**
   ::

     make test        # Run tests
     make lint        # Check code style
     make docs        # Build documentation

Best Practices
------------

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use Black for formatting
   - Write descriptive variable names
   - Add type hints where appropriate

2. **Testing**
   - Write tests for new features
   - Maintain test coverage above 80%
   - Use fixtures for common test data
   - Test edge cases and error conditions

3. **Documentation**
   - Update docstrings for new functions
   - Document complex algorithms
   - Keep API documentation current
   - Include examples in docstrings

4. **Git Workflow**
   - Create feature branches
   - Write descriptive commit messages
   - Keep commits focused and atomic
   - Review code before merging

5. **Security**
   - Never commit sensitive data
   - Use environment variables for secrets
   - Follow security best practices
   - Keep dependencies updated

Troubleshooting
-------------

Common issues and solutions:

1. **Database Issues**
   - Reset containers: ``make clean``
   - Reinitialize: ``make init``
   - Check logs: ``make logs``
   - Verify database URL in .env

2. **Test Failures**
   - Run tests with verbose output: ``pytest -v``
   - Check test coverage: ``make coverage``
   - Verify test data setup

3. **Documentation Build Issues**
   - Clean docs: ``rm -rf docs/_build``
   - Rebuild: ``make docs``
   - Check Sphinx warnings

4. **Container Issues**
   - Check container status: ``make status``
   - View logs: ``make logs``
   - Restart containers: ``make clean && make run``

Getting Help
----------

- Check the project documentation
- Review the test suite for examples
- Consult the Flask documentation
- Ask for help in the project's issue tracker

Additional Resources
-----------------

- `Flask Documentation <https://flask.palletsprojects.com/>`_
- `SQLAlchemy Documentation <https://docs.sqlalchemy.org/>`_
- `Pytest Documentation <https://docs.pytest.org/>`_
- `Black Documentation <https://black.readthedocs.io/>`_
- `Sphinx Documentation <https://www.sphinx-doc.org/>`_
- `Docker Compose Documentation <https://docs.docker.com/compose/>`_ 