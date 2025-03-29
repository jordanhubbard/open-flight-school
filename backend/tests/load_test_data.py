import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
from test_data_loader import load_test_data

# Test database URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/test_db")

def main():
    """Create database engine and load test data."""
    engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        connect_args={'options': '-c timezone=utc'}
    )
    
    # Create session
    session = Session(bind=engine)
    
    try:
        # Load test data
        load_test_data(session)
        print("Test data loaded successfully")
    except Exception as e:
        print(f"Error loading test data: {e}")
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main() 