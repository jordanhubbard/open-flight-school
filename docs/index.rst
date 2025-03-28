Welcome to Open Flight School's documentation!
===========================================

Open Flight School is a web application for managing flight school operations, including aircraft scheduling, instructor management, and student bookings.

Getting Started
--------------

1. Clone the repository
2. Build the containers:
   ::

     make build

3. Initialize the database:
   ::

     make init

4. Load test data:
   ::

     make test-data

5. Run the application:
   ::

     make run

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

  make test && make lint && make docs

This will run tests, linting, and build documentation.

Database Management
-----------------

The application uses PostgreSQL for all environments. Database operations are managed through Docker Compose:

- Initialize database: ``make init``
- Load test data: ``make test-data``
- Clean up: ``make clean``

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