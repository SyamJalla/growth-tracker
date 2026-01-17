from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import urllib.parse

import psycopg2
from sqlalchemy.orm import Session

from core.settings import Settings
from db.database import init_db, get_db
from db.models import HealthCheck

router = APIRouter()


class CreateDatabaseRequest(BaseModel):
    db_name: str = "growth_tracker"


@router.post("/create_database", summary="Create a new Postgres database on the server")
def create_database(req: CreateDatabaseRequest):
    settings = Settings()
    admin_url = settings.admin_database_url
    
    # Convert SQLAlchemy URL to psycopg2 format
    # Remove the +psycopg2 dialect if present
    if "+psycopg2" in admin_url:
        admin_url = admin_url.replace("+psycopg2", "")
    
    try:
        # Use psycopg2 to connect to the admin DB and create the database
        conn = psycopg2.connect(admin_url)
        conn.autocommit = True
        cur = conn.cursor()
        # safe identifier via quoting
        dbname = req.db_name
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cur.fetchone()
        if exists:
            cur.close()
            conn.close()
            return {"status": "ok", "detail": f"database '{dbname}' already exists"}
        cur.execute(f"CREATE DATABASE {psycopg2.extensions.quote_ident(dbname, cur)};")
        cur.close()
        conn.close()
        return {"status": "ok", "detail": f"database '{dbname}' created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_tables", summary="Create all database tables")
def create_tables():
    try:
        init_db()
        return {"status": "ok", "detail": "tables created or already exist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/init_health_check", summary="Initialize health check table with test message")
# def init_health_check(db: Session = Depends(get_db)):
#     try:
#         # Check if message already exists
#         existing = db.query(HealthCheck).first()
#         if existing:
#             return {"status": "ok", "detail": "Health check message already exists", "message": existing.message}
        
#         # Insert test message
#         health_msg = HealthCheck(message="Database connection is healthy and working!")
#         db.add(health_msg)
#         db.commit()
#         db.refresh(health_msg)
#         return {"status": "ok", "detail": "Health check message created", "message": health_msg.message}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

