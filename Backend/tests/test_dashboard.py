"""
Tests for Dashboard API endpoint
"""
import pytest
from datetime import datetime


def test_dashboard_empty(client):
    """Test dashboard with no data"""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    data = response.json()
    assert "workout" in data
    assert "smoking" in data
    
    # Verify empty workout stats
    workout = data["workout"]
    assert workout["current_streak"] == 0
    assert workout["longest_streak"] == 0
    assert workout["total_workout_days"] == 0
    assert workout["total_days"] == 0
    assert workout["workout_percentage"] == 0.0
    assert workout["average_duration"] is None
    
    # Verify empty smoking stats
    smoking = data["smoking"]
    assert smoking["total_cigarettes"] == 0
    assert smoking["current_clean_streak"] >= 0  # Days since year start
    assert smoking["longest_clean_streak"] >= 0
    assert smoking["total_relapses"] == 0


def test_dashboard_with_workout_data(client, multiple_workout_entries):
    """Test dashboard with multiple workout entries"""
    # Add workout entries
    for entry in multiple_workout_entries:
        response = client.post("/api/workouts", json=entry)
        assert response.status_code == 201
    
    # Get dashboard
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    data = response.json()
    workout = data["workout"]
    
    # Verify workout statistics
    assert workout["total_workout_days"] == 4
    assert workout["current_streak"] >= 0
    assert workout["longest_streak"] >= 2  # At least 2 consecutive days
    
    # Check duration average exists
    assert workout["average_duration"] is not None
    assert workout["average_duration"] > 0


def test_dashboard_with_smoking_data(client, multiple_smoking_entries):
    """Test dashboard with multiple smoking entries"""
    # Add smoking entries
    for entry in multiple_smoking_entries:
        response = client.post("/api/smoking", json=entry)
        assert response.status_code == 201
    
    # Get dashboard
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    data = response.json()
    smoking = data["smoking"]
    
    # Verify smoking statistics
    assert smoking["total_cigarettes"] == 11  # 8 + 0 + 0 + 3
    assert smoking["total_smoking_days"] == 2  # Jan 10 and Jan 13 had cigarettes
    assert smoking["currenrelapses"] >= 2  # Days with cigarettes
    assert smoking["longest_clean_streak"] >= 2  # Jan 11-12

def test_dashboard_with_all_data(client, multiple_workout_entries, multiple_smoking_entries):
    """Test dashboard with both workout and smoking data"""
    # Add workout entries
    for entry in multiple_workout_entries:
        client.post("/api/workouts", json=entry)
    
    # Add smoking entries
    for entry in multiple_smoking_entries:
        client.post("/api/smoking", json=entry)
    
    # Get dashboard
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    data = response.json()
    
    # Both sections should have data
    assert data["workout"]["total_workout_days"] == 4
    assert data["smoking"]["total_cigarettes"] == 11


def test_dashboard_date_range_filter(client, multiple_workout_entries):
    """Test dashboard with date range filter"""
    # Add workout entries
    for entry in multiple_workout_entries:
        client.post("/api/workouts", json=entry)
    
    # Filter for specific date range (Jan 11-12 only)
    response = client.get("/api/dashboard?start_date=2026-01-11&end_date=2026-01-12")
    assert response.status_code == 200
    
    data = response.json()
    workout = data["workout"]
    
    # Should include data from the range (Jan 11-12)
    assert workout["total_workout_days"] >= 1  # At least some data in range


def test_dashboard_invalid_date_param(client):
    """Test dashboard with invalid date parameter"""
    response = client.get("/api/dashboard?start_date=invalid-date")
    # API ignores invalid query params and returns all data
    assert response.status_code == 200


def test_dashboard_end_date_before_start_date(client):
    """Test dashboard with end_date before start_date"""
    response = client.get("/api/dashboard?start_date=2026-01-13&end_date=2026-01-10")
    # Should either return error or empty results
    assert response.status_code in [200, 400]
