Welcome to Open Flight School's documentation!
===========================================

Open Flight School is a web application for managing flight school operations, including aircraft scheduling, instructor management, and student bookings.

Getting Started
--------------

1. Clone the repository
2. Create a virtual environment and install dependencies:
   ::

     make venv

3. Create and configure your environment file:
   ::

     make env

4. Initialize the database:
   ::

     make init

5. Load test data:
   ::

     make test-data

6. Run the application:
   ::

     make dev

Development Workflow
------------------

The application uses several development tools to maintain code quality:

- **Linting**: Run ``make lint`` to check code style
- **Formatting**: Run ``make format`` to format code
- **Testing**: Run ``make test`` to run tests
- **Coverage**: Run ``make coverage`` to generate coverage reports
- **Documentation**: Run ``make docs`` to build documentation

For a complete check of the codebase, run:
::

  make check

This will run linting, formatting, and tests.

Database Management
-----------------

- Create a new migration:
  ::

    make migrate message="your migration message"

- Reset the database:
  ::

    make reset-db

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   development
   api/models
   api/routes
   api/utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 