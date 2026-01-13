"""
Tests for root endpoints
"""
import pytest


def test_read_root(client):
    """Test root endpoint"""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data and data["status"] == "ok"


def test_health_check(client):
    """Test health check endpoint"""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
