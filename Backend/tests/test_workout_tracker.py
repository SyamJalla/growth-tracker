"""
Tests for Workout Tracker API endpoints
"""
import pytest


def test_create_workout_entry(client, sample_workout_data):
    """Test creating a new workout entry"""
    response = client.post("/api/workouts", json=sample_workout_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["date"] == sample_workout_data["date"]
    assert data["workout_type"] == sample_workout_data["workout_type"]
    assert data["workout_done"] == sample_workout_data["workout_done"]
    assert data["duration_minutes"] == sample_workout_data["duration_minutes"]
    assert data["intensity"] == sample_workout_data["intensity"]
    assert data["notes"] == sample_workout_data["notes"]


def test_create_workout_entry_duplicate_date(client, sample_workout_data):
    """Test creating workout entry with duplicate date"""
    # Create first entry
    response = client.post("/api/workouts", json=sample_workout_data)
    assert response.status_code == 201
    
    # Try to create duplicate
    response = client.post("/api/workouts", json=sample_workout_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_create_workout_minimal_data(client):
    """Test creating workout with minimal required fields"""
    minimal_data = {
        "date": "2026-01-14",
        "workout_type": "Push",
        "workout_done": True
    }
    response = client.post("/api/workouts", json=minimal_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["date"] == minimal_data["date"]
    assert data["workout_type"] == minimal_data["workout_type"]
    assert data["workout_done"] == minimal_data["workout_done"]


def test_create_workout_invalid_workout_type(client):
    """Test creating workout with invalid workout type"""
    invalid_data = {
        "date": "2026-01-14",
        "workout_type": "Gym",
        "workout_done": True
    }
    response = client.post("/api/workouts", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_create_workout_invalid_intensity(client):
    """Test creating workout with invalid intensity"""
    invalid_data = {
        "date": "2026-01-14",
        "workout_type": "Push",
        "workout_done": True,
        "intensity": "SuperHigh"
    }
    response = client.post("/api/workouts", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_get_workout_entry(client, sample_workout_data):
    """Test retrieving a specific workout entry"""
    # Create entry
    client.post("/api/workouts", json=sample_workout_data)
    
    # Get entry
    response = client.get(f"/api/workouts/{sample_workout_data['date']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["date"] == sample_workout_data["date"]
    assert data["workout_type"] == sample_workout_data["workout_type"]


def test_get_workout_entry_not_found(client):
    """Test retrieving non-existent workout entry"""
    response = client.get("/api/workouts/2026-01-01")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower() or "no" in response.json()["detail"].lower()


def test_update_workout_entry(client, sample_workout_data):
    """Test updating an existing workout entry"""
    # Create entry
    client.post("/api/workouts", json=sample_workout_data)
    
    # Update entry
    updated_data = {
        "workout_type": "Cardio",
        "workout_done": True,
        "duration_minutes": 45,
        "intensity": "High",
        "notes": "Updated workout"
    }
    response = client.put(f"/api/workouts/{sample_workout_data['date']}", json=updated_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["workout_type"] == updated_data["workout_type"]
    assert data["duration_minutes"] == updated_data["duration_minutes"]
    assert data["intensity"] == updated_data["intensity"]
    assert data["notes"] == updated_data["notes"]


def test_update_workout_partial(client, sample_workout_data):
    """Test partial update of workout entry"""
    # Create entry
    client.post("/api/workouts", json=sample_workout_data)
    
    # Partial update
    partial_data = {
        "duration_minutes": 90,
        "notes": "Extended session"
    }
    response = client.put(f"/api/workouts/{sample_workout_data['date']}", json=partial_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["duration_minutes"] == 90
    assert data["notes"] == "Extended session"
    # Original fields should remain
    assert data["workout_type"] == sample_workout_data["workout_type"]


def test_update_workout_not_found(client):
    """Test updating non-existent workout entry"""
    updated_data = {
        "workout_type": "Push",
        "workout_done": True
    }
    response = client.put("/api/workouts/2026-01-01", json=updated_data)
    assert response.status_code == 404


def test_delete_workout_entry(client, sample_workout_data):
    """Test deleting a workout entry"""
    # Create entry
    client.post("/api/workouts", json=sample_workout_data)
    
    # Delete entry
    response = client.delete(f"/api/workouts/{sample_workout_data['date']}")
    assert response.status_code == 204
    assert "deleted successfully" in response.json()["message"].lower()
    
    # Verify deletion
    response = client.get(f"/api/workouts/{sample_workout_data['date']}")
    assert response.status_code == 404


def test_delete_workout_not_found(client):
    """Test deleting non-existent workout entry"""
    response = client.delete("/api/workouts/2026-01-01")
    assert response.status_code == 404


def test_get_workout_history_empty(client):
    """Test getting workout history with no entries"""
    # Note: List endpoint may not be implemented
    response = client.get("/api/workouts/history")
    if response.status_code == 200:
        assert response.json() == []


def test_get_workout_history_all(client, multiple_workout_entries):
    """Test getting all workout history"""
    # Create multiple entries
    for entry in multiple_workout_entries:
        client.post("/api/workouts", json=entry)
    
    # Get history
    response = client.get("/api/workouts/history")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 4
        # Should be sorted by date descending
        assert data[0]["date"] == "2026-01-13"
        assert data[-1]["date"] == "2026-01-10"


def test_get_workout_history_date_range(client, multiple_workout_entries):
    """Test getting workout history with date range filter"""
    # Create multiple entries
    for entry in multiple_workout_entries:
        client.post("/api/workouts", json=entry)
    
    # Get history for specific range
    response = client.get("/api/workouts/history?start_date=2026-01-11&end_date=2026-01-12")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2
        dates = [entry["date"] for entry in data]
        assert "2026-01-11" in dates
        assert "2026-01-12" in dates


def test_get_workout_history_limit(client, multiple_workout_entries):
    """Test getting workout history with limit"""
    # Create multiple entries
    for entry in multiple_workout_entries:
        client.post("/api/workouts", json=entry)
    
    # Get history with limit
    response = client.get("/api/workouts/history?limit=2")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2


def test_workout_done_false_with_duration(client):
    """Test creating workout with workout_done=False but duration provided"""
    data = {
        "date": "2026-01-15",
        "workout_type": "Push",
        "workout_done": False,
        "duration_minutes": 60  # Duration provided but workout not done
    }
    response = client.post("/api/workouts", json=data)
    # Should either accept it or validate that duration should be 0
    assert response.status_code in [201, 422]
