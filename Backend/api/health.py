from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import HealthCheck

router = APIRouter()


@router.get("/", tags=["health"])
def app_health():
    return {"status": "ok", "message": "Growth Tracker API running"}


@router.get("/db", tags=["health"])
def db_health(db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=503, detail=f"Database unreachable: {str(e)}")
