"""
Test fixtures and configuration for pytest
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set testing environment variable before importing app
os.environ["TESTING"] = "1"

from app import app
from db.database import Base, get_db


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_workout_data():
    """Sample workout data for testing"""
    return {
        "date": "2026-01-13",
        "workout_type": "Push",
        "workout_done": True,
        "duration_minutes": 60,
        "intensity": "Moderate",
        "notes": "Full body workout"
    }


@pytest.fixture
def sample_smoking_data():
    """Sample smoking data for testing"""
    return {
        "date": "2026-01-13",
        "cigarette_count": 5,
        "location": "Home",
        "remarks": "Stressful day"
    }


@pytest.fixture
def multiple_workout_entries():
    """Multiple workout entries for testing streaks and statistics"""
    return [
        {
            "date": "2026-01-10",
            "workout_type": "Push",
            "workout_done": True,
            "duration_minutes": 45,
            "intensity": "High",
            "notes": "Chest day"
        },
        {
            "date": "2026-01-11",
            "workout_type": "Cardio",
            "workout_done": True,
            "duration_minutes": 30,
            "intensity": "Moderate",
            "notes": "Morning run"
        },
        {
            "date": "2026-01-12",
            "workout_type": "Pull",
            "workout_done": False,
            "duration_minutes": 0,
            "intensity": None,
            "notes": "Rest day"
        },
        {
            "date": "2026-01-13",
            "workout_type": "Legs",
            "workout_done": True,
            "duration_minutes": 40,
            "intensity": "Low",
            "notes": "Flexibility focus"
        }
    ]


@pytest.fixture
def multiple_smoking_entries():
    """Multiple smoking entries for testing streaks and statistics"""
    return [
        {
            "date": "2026-01-10",
            "cigarette_count": 8,
            "location": "Work",
            "remarks": "Busy day"
        },
        {
            "date": "2026-01-11",
            "cigarette_count": 0,
            "location": "Home",
            "remarks": "Smoke-free day!"
        },
        {
            "date": "2026-01-12",
            "cigarette_count": 0,
            "location": "Home",
            "remarks": "Still going strong"
        },
        {
            "date": "2026-01-13",
            "cigarette_count": 3,
            "location": "Home",
            "remarks": "Weekend relapse"
        }
    ]
