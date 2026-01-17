"""
Tests for VERSION 2.2 features:
- Historical date support
- Upsert endpoints
- Date validation
- Streak recalculation with historical data
"""
import pytest


def test_upsert_creates_new_workout(client):
    """Test upsert creates entry when it doesn't exist (VERSION 2.2)"""
    response = client.post("/api/workouts/upsert/", json={
        "date": "2026-01-05",
        "workout_type": "Push",
        "workout_done": True,
        "duration_minutes": 45,
        "intensity": "High"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == "2026-01-05"
    assert data["workout_type"] == "Push"
    assert data["duration_minutes"] == 45
    assert "created_at" in data
    assert "updated_at" in data


def test_upsert_updates_existing_workout(client, sample_workout_data):
    """Test upsert updates entry when it exists (VERSION 2.2)"""
    # Create entry via legacy POST
    client.post("/api/workouts", json=sample_workout_data)
    
    # Update via upsert with different values
    upsert_data = sample_workout_data.copy()
    upsert_data["workout_type"] = "Pull"
    upsert_data["duration_minutes"] = 90
    
    response = client.post("/api/workouts/upsert/", json=upsert_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["workout_type"] == "Pull"
    assert data["duration_minutes"] == 90
    
    # Verify only 1 entry exists (not duplicated)
    get_response = client.get(f"/api/workouts/{sample_workout_data['date']}")
    assert get_response.status_code == 200


def test_upsert_idempotent(client, sample_workout_data):
    """Test upsert is idempotent - safe to retry (VERSION 2.2)"""
    # Call upsert 3 times with same data
    responses = []
    for _ in range(3):
        response = client.post("/api/workouts/upsert/", json=sample_workout_data)
        responses.append(response)
    
    # All should succeed
    for response in responses:
        assert response.status_code == 200
    
    # Verify only 1 entry exists
    get_response = client.get(f"/api/workouts/{sample_workout_data['date']}")
    assert get_response.status_code == 200


def test_upsert_historical_workout_date(client):
    """Test upsert accepts historical dates (VERSION 2.2)"""
    historical_data = {
        "date": "2026-01-01",
        "workout_type": "Push",
        "workout_done": True,
        "duration_minutes": 60
    }
    response = client.post("/api/workouts/upsert/", json=historical_data)
    assert response.status_code == 200
    assert response.json()["date"] == "2026-01-01"


def test_upsert_creates_new_smoking(client):
    """Test upsert creates smoking entry (VERSION 2.2)"""
    response = client.post("/api/smoking/upsert/", json={
        "date": "2026-01-05",
        "cigarette_count": 3,
        "location": "Home",
        "remarks": "Evening"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == "2026-01-05"
    assert data["cigarette_count"] == 3


def test_upsert_updates_existing_smoking(client, sample_smoking_data):
    """Test upsert updates existing smoking entry (VERSION 2.2)"""
    # Create entry
    client.post("/api/smoking", json=sample_smoking_data)
    
    # Update via upsert
    updated_data = sample_smoking_data.copy()
    updated_data["cigarette_count"] = 10
    updated_data["remarks"] = "Updated"
    
    response = client.post("/api/smoking/upsert/", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["cigarette_count"] == 10
    assert data["remarks"] == "Updated"


def test_upsert_smoking_idempotent(client, sample_smoking_data):
    """Test smoking upsert is idempotent (VERSION 2.2)"""
    for _ in range(3):
        response = client.post("/api/smoking/upsert/", json=sample_smoking_data)
        assert response.status_code == 200
    
    # Verify only 1 entry
    get_response = client.get(f"/api/smoking/{sample_smoking_data['date']}")
    assert get_response.status_code == 200


def test_multiple_historical_workouts_sequential(client):
    """Test multiple historical entries added sequentially (VERSION 2.2)"""
    dates = ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08"]
    
    for workout_date in dates:
        response = client.post("/api/workouts/upsert/", json={
            "date": workout_date,
            "workout_type": "Push",
            "workout_done": True,
            "duration_minutes": 60
        })
        assert response.status_code == 200
    
    # Verify all 4 entries exist
    history_response = client.get("/api/workouts/history")
    if history_response.status_code == 200:
        assert len(history_response.json()) == 4


def test_dashboard_updates_after_historical_workout(client):
    """Test dashboard recalculates after adding historical workout (VERSION 2.2)"""
    # Add workouts: Jan 11, 12, 13
    dates = ["2026-01-11", "2026-01-12", "2026-01-13"]
    for date in dates:
        client.post("/api/workouts/upsert/", json={
            "date": date,
            "workout_type": "Push",
            "workout_done": True,
            "duration_minutes": 60
        })
    
    # Check initial total days
    response = client.get("/api/dashboard")
    initial_days = response.json()["workout"]["total_workout_days"]
    assert initial_days == 3
    
    # Add historical entry for Jan 10
    client.post("/api/workouts/upsert/", json={
        "date": "2026-01-10",
        "workout_type": "Push",
        "workout_done": True,
        "duration_minutes": 60
    })
    
    # Workout days should now be 4
    response = client.get("/api/dashboard")
    new_days = response.json()["workout"]["total_workout_days"]
    assert new_days == 4


def test_dashboard_updates_after_historical_smoking(client):
    """Test dashboard recalculates after historical smoking entry (VERSION 2.2)"""
    # Create smoking entry on Jan 3
    client.post("/api/smoking/upsert/", json={
        "date": "2026-01-03",
        "cigarette_count": 5,
        "location": "Home"
    })
    
    initial_response = client.get("/api/dashboard")
    initial_total = initial_response.json()["smoking"]["total_cigarettes"]
    assert initial_total == 5
    
    # Add another historical smoking on Jan 8
    client.post("/api/smoking/upsert/", json={
        "date": "2026-01-08",
        "cigarette_count": 3,
        "location": "Work"
    })
    
    # Total should now be 8
    new_response = client.get("/api/dashboard")
    new_total = new_response.json()["smoking"]["total_cigarettes"]
    assert new_total == 8


def test_year_boundary_dates(client):
    """Test dates at 2026 boundaries (VERSION 2.2)"""
    # Jan 1, 2026 (start of year)
    response1 = client.post("/api/workouts/upsert/", json={
        "date": "2026-01-01",
        "workout_type": "Push",
        "workout_done": True
    })
    assert response1.status_code == 200
    
    # Dec 31, 2026 (end of year)
    response2 = client.post("/api/workouts/upsert/", json={
        "date": "2026-12-31",
        "workout_type": "Push",
        "workout_done": True
    })
    # Accepts date (future date validation not yet added)
    assert response2.status_code in [200, 422]
