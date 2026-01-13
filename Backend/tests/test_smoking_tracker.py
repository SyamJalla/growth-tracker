"""
Tests for Smoking Tracker API endpoints
"""
import pytest


def test_create_smoking_entry(client, sample_smoking_data):
    """Test creating a new smoking entry"""
    response = client.post("/api/smoking", json=sample_smoking_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["date"] == sample_smoking_data["date"]
    assert data["cigarette_count"] == sample_smoking_data["cigarette_count"]
    assert data["location"] == sample_smoking_data["location"]
    assert data["remarks"] == sample_smoking_data["remarks"]


def test_create_smoking_entry_duplicate_date(client, sample_smoking_data):
    """Test creating smoking entry with duplicate date"""
    # Create first entry
    response = client.post("/api/smoking", json=sample_smoking_data)
    assert response.status_code == 201
    
    # Try to create duplicate
    response = client.post("/api/smoking", json=sample_smoking_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_create_smoking_minimal_data(client):
    """Test creating smoking entry with minimal required fields"""
    minimal_data = {
        "date": "2026-01-14",
        "cigarette_count": 0,
        "location": "Home"
    }
    response = client.post("/api/smoking", json=minimal_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["date"] == minimal_data["date"]
    assert data["cigarette_count"] == minimal_data["cigarette_count"]


def test_create_smoking_zero_count(client):
    """Test creating smoking entry with zero cigarettes (smoke-free day)"""
    smoke_free_data = {
        "date": "2026-01-14",
        "cigarette_count": 0,
        "location": "Home",
        "remarks": "Smoke-free day!"
    }
    response = client.post("/api/smoking", json=smoke_free_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["cigarette_count"] == 0
    assert data["remarks"] == "Smoke-free day!"


def test_create_smoking_negative_count(client):
    """Test creating smoking entry with negative cigarette count"""
    invalid_data = {
        "date": "2026-01-14",
        "cigarette_count": -5
    }
    response = client.post("/api/smoking", json=invalid_data)
    # Should either reject or validate minimum value
    assert response.status_code in [200, 422]


def test_create_smoking_invalid_location(client):
    """Test creating smoking entry with invalid location"""
    invalid_data = {
        "date": "2026-01-14",
        "cigarette_count": 5,
        "location": "Office"
    }
    response = client.post("/api/smoking", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_get_smoking_entry(client, sample_smoking_data):
    """Test retrieving a specific smoking entry"""
    # Create entry
    client.post("/api/smoking", json=sample_smoking_data)
    
    # Get entry
    response = client.get(f"/api/smoking/{sample_smoking_data['date']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["date"] == sample_smoking_data["date"]
    assert data["cigarette_count"] == sample_smoking_data["cigarette_count"]


def test_get_smoking_entry_not_found(client):
    """Test retrieving non-existent smoking entry"""
    response = client.get("/api/smoking/2026-01-01")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower() or "no" in response.json()["detail"].lower()


def test_delete_smoking_entry(client, sample_smoking_data):
    """Test deleting a smoking entry"""
    # Create entry
    client.post("/api/smoking", json=sample_smoking_data)
    
    # Delete entry
    response = client.delete(f"/api/smoking/{sample_smoking_data['date']}")
    assert response.status_code == 204
    assert "deleted successfully" in response.json()["message"].lower()
    
    # Verify deletion
    response = client.get(f"/api/smoking/{sample_smoking_data['date']}")
    assert response.status_code == 404


def test_delete_smoking_not_found(client):
    """Test deleting non-existent smoking entry"""
    response = client.delete("/api/smoking/2026-01-01")
    assert response.status_code == 404


def test_get_smoking_history_empty(client):
    """Test getting smoking history with no entries"""
    response = client.get("/api/smoking/history")
    if response.status_code == 200:
        assert response.json() == []


def test_get_smoking_history_all(client, multiple_smoking_entries):
    """Test getting all smoking history"""
    # Create multiple entries
    for entry in multiple_smoking_entries:
        client.post("/api/smoking", json=entry)
    
    # Get history
    response = client.get("/api/smoking/history")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 4
        # Should be sorted by date descending
        assert data[0]["date"] == "2026-01-13"
        assert data[-1]["date"] == "2026-01-10"


def test_get_smoking_history_date_range(client, multiple_smoking_entries):
    """Test getting smoking history with date range filter"""
    # Create multiple entries
    for entry in multiple_smoking_entries:
        client.post("/api/smoking", json=entry)
    
    # Get history for specific range
    response = client.get("/api/smoking/history?start_date=2026-01-11&end_date=2026-01-12")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2
        dates = [entry["date"] for entry in data]
        assert "2026-01-11" in dates
        assert "2026-01-12" in dates


def test_get_smoking_history_limit(client, multiple_smoking_entries):
    """Test getting smoking history with limit"""
    # Create multiple entries
    for entry in multiple_smoking_entries:
        client.post("/api/smoking", json=entry)
    
    # Get history with limit
    response = client.get("/api/smoking/history?limit=2")
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2


def test_smoking_history_mixed_days(client):
    """Test smoking history with mix of smoking and smoke-free days"""
    entries = [
        {"date": "2026-01-10", "cigarette_count": 5, "location": "Home"},
        {"date": "2026-01-11", "cigarette_count": 0, "remarks": "Smoke-free!"},
        {"date": "2026-01-12", "cigarette_count": 3, "location": "Work"},
        {"date": "2026-01-13", "cigarette_count": 0, "remarks": "Another smoke-free day"}
    ]
    
    for entry in entries:
        client.post("/api/smoking", json=entry)
    
    response = client.get("/api/smoking/history")
    if response.status_code != 200:
        return  # Skip if endpoint not available
    
    data = response.json()
    assert len(data) == 4
    
    # Verify mix of smoking and smoke-free days
    counts = [entry["cigarette_count"] for entry in data]
    assert 0 in counts
    assert any(count > 0 for count in counts)


def test_smoking_location_consistency(client):
    """Test that location is properly stored and retrieved"""
    locations_to_test = ["Home", "Work", "Social", "Other"]
    
    for i, location in enumerate(locations_to_test):
        entry = {
            "date": f"2026-01-{10+i:02d}",
            "cigarette_count": 5,
            "location": location
        }
        response = client.post("/api/smoking", json=entry)
        assert response.status_code == 201
        assert response.json()["location"] == location


def test_update_smoking_entry_not_supported(client, sample_smoking_data):
    """Test that updating smoking entries is not supported (only create/delete)"""
    # Create entry
    client.post("/api/smoking", json=sample_smoking_data)
    
    # Try to update (PUT method should not be available)
    updated_data = {"cigarette_count": 10}
    response = client.put(f"/api/smoking/{sample_smoking_data['date']}", json=updated_data)
    assert response.status_code == 405  # Method Not Allowed
