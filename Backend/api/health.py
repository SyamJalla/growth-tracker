from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_db

router = APIRouter()


@router.get("/", tags=["health"])
def app_health():
    return {"status": "ok", "message": "Growth Tracker API running"}


@router.get("/db", tags=["health"])
def db_health(db: Session = Depends(get_db)):
    try:
        # simple lightweight check
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unreachable")
