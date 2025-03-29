from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from tests.test_data_loader import load_test_data

# Create database engine
engine = create_engine("postgresql://postgres:postgres@postgres:5432/flight_school")

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def main():
    try:
        # Load test data
        load_test_data(db)
        print("Test data loaded successfully!")
    except Exception as e:
        print(f"Error loading test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 