Development Guide
================

This guide provides detailed information about the development workflow, tools, and best practices for the Open Flight School project.

Development Environment
---------------------

The project uses a virtual environment to isolate dependencies. The development environment is managed through Make targets:

1. **Initial Setup**
   ::

     make env        # Create .env file from template
     make setup      # Set up the complete development environment

2. **Running the Application**
   ::

     make dev       # Run the Flask development server
     make test      # Run the test suite
     make check     # Run all code quality checks

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

The application uses SQLite for development and testing. Database operations are managed through Flask-Migrate:

1. **Creating Migrations**
   ::

     make migrate message="description of changes"

2. **Applying Migrations**
   ::

     make init

3. **Resetting Database**
   ::

     make reset-db

4. **Loading Test Data**
   ::

     make test-data

Development Workflow
-----------------

1. **Starting a New Feature**
   ::

     make env              # Ensure .env is set up
     make setup           # Set up development environment
     make dev            # Start the development server

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

     make check          # Run all checks
     make coverage       # Check test coverage
     make docs          # Build documentation

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
   - Reset the database: ``make reset-db``
   - Check migrations: ``flask db current``
   - Verify database URL in .env

2. **Test Failures**
   - Run tests with verbose output: ``pytest -v``
   - Check test coverage: ``make coverage``
   - Verify test data setup

3. **Documentation Build Issues**
   - Clean docs: ``rm -rf docs/_build``
   - Rebuild: ``make docs``
   - Check Sphinx warnings

4. **Environment Issues**
   - Clean environment: ``make clean``
   - Recreate venv: ``make venv``
   - Verify .env configuration

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