from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import urllib.parse

import psycopg2

from core.settings import Settings
from db.database import init_db

router = APIRouter()


class CreateDatabaseRequest(BaseModel):
    db_name: str = "growth_tracker"


@router.post("/create_database", summary="Create a new Postgres database on the server")
def create_database(req: CreateDatabaseRequest):
    settings = Settings()
    admin_url = settings.admin_database_url
    # parse DSN to get connection params for psycopg2
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

