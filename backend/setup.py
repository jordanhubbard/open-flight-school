from setuptools import setup, find_packages

setup(
    name="open-flight-school",
    version="0.1.0",
    packages=find_packages(where=".", include=["app", "app.*", "tests", "tests.*"]),
    package_dir={"": "."},
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "pydantic",
        "python-jose",
        "passlib",
        "python-multipart",
        "pytest",
        "requests",
        "alembic",
    ],
    python_requires=">=3.11",
) 