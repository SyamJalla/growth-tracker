"""
Health Check API Routes

This module provides endpoints for monitoring the health and availability
of the Growth Tracker API application and its database connection.

Purpose:
    - Verify application is running and responsive
    - Check database connectivity and query execution
    - Provide status information for monitoring systems
    - Support health checks in containerized environments (Docker, Kubernetes)

Routes:
    GET /api/health/     - Application health check
    GET /api/health/db   - Database connectivity check
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import HealthCheck

router = APIRouter()


@router.get("/", tags=["health"])
def app_health():
    """
    Application Health Check
    
    Purpose:
        Verifies that the FastAPI application is running and responsive.
        Used for basic uptime monitoring and load balancer health checks.
    
    Request:
        - No parameters required
        - No authentication required
    
    Response:
        {
            "status": "ok",
            "message": "Growth Tracker API running"
        }
    
    Status Codes:
        - 200 OK: Application is healthy and responsive
    
    Use Cases:
        - Container orchestration health probes
        - Load balancer health checks
        - Uptime monitoring services
        - API availability verification
    
    Example:
        curl -X GET http://localhost:8000/api/health/
    """
    return {"status": "ok", "message": "Growth Tracker API running"}


@router.get("/db", tags=["health"])
def db_health(db: Session = Depends(get_db)):
    """
    Database Health Check
    
    Purpose:
        Verifies database connectivity by querying the health_check table.
        Ensures the database is accessible and can execute queries.
    
    Request:
        - No parameters required
        - No authentication required
        - Database session injected via dependency
    
    Response (Success):
        {
            "status": "ok",
            "db": "ok",
            "message": "Health check message from database",
            "created_at": "2026-01-17T10:00:00"
        }
    
    Response (No Health Record):
        {
            "status": "ok",
            "db": "ok",
            "message": "No health check message found in database"
        }
    
    Response (Database Error):
        {
            "detail": "Database unreachable: <error details>"
        }
    
    Status Codes:
        - 200 OK: Database is connected and responsive
        - 503 Service Unavailable: Database connection failed
    
    Use Cases:
        - Verify database connectivity before deployment
        - Monitor database availability
        - Troubleshoot connection issues
        - Database migration verification
    
    Error Handling:
        - Catches all database exceptions
        - Returns 503 status on any database error
        - Includes error details in response
    
    Example:
        curl -X GET http://localhost:8000/api/health/db
    """
    try:
        # Query the health_check table
        health_record = db.query(HealthCheck).first()
        
        if health_record:
            return {
                "status": "ok", 
                "db": "ok",
                "message": health_record.message,
                "created_at": health_record.created_at.isoformat()
            }
        else:
            return {
                "status": "ok", 
                "db": "ok",
                "message": "No health check message found in database"
            }
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Database unreachable: {str(e)}"
        )
