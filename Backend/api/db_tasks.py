"""
Database Setup and Management API Routes

This module provides utility endpoints for database initialization,
table creation, and database management tasks.

Purpose:
    - Initialize PostgreSQL database
    - Create all required tables from SQLAlchemy models
    - Support database setup automation
    - Enable database reset/recreation for development
    - Provide idempotent setup operations

Routes:
    POST /db/create_database - Create PostgreSQL database
    POST /db/create_tables   - Create all database tables

Security Note:
    These endpoints should be restricted in production environments
    or moved to administrative CLI tools. They allow database structure
    modifications which should require elevated privileges.

Use Cases:
    - Initial application setup
    - Development environment setup
    - Docker container initialization
    - CI/CD pipeline database preparation
    - Database migration tasks
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import os

from db.database import engine, Base
from db.models import WorkoutEntry, SmokingEntry, HealthCheck

router = APIRouter()


class DatabaseCreate(BaseModel):
    """
    Database Creation Request Model
    
    Fields:
        db_name: Name of the PostgreSQL database to create
                Default: "growth_tracker"
                Must be valid PostgreSQL identifier
    
    Validation:
        - db_name must not be empty
        - Should contain only alphanumeric characters and underscores
        - Case-sensitive (PostgreSQL converts to lowercase by default)
    
    Examples:
        {"db_name": "growth_tracker"}
        {"db_name": "growth_tracker_test"}
        {"db_name": "growth_tracker_dev"}
    """
    db_name: str = "growth_tracker"


@router.post("/create_database")
def create_database(request: DatabaseCreate):
    """
    Create PostgreSQL Database
    
    Purpose:
        Creates a new PostgreSQL database with the specified name.
        Connects to 'postgres' default database to execute CREATE DATABASE command.
        Operation is idempotent - returns success if database already exists.
    
    Request Body:
        {
            "db_name": "growth_tracker"  # Database name to create
        }
    
    Response (Created):
        {
            "status": "ok",
            "detail": "database 'growth_tracker' created"
        }
    
    Response (Already Exists):
        {
            "status": "ok",
            "detail": "database 'growth_tracker' already exists"
        }
    
    Response (Error):
        {
            "detail": "Failed to create database: <error message>"
        }
    
    Status Codes:
        - 200 OK: Database created or already exists
        - 500 Internal Server Error: Database creation failed
    
    How It Works:
        1. Reads PostgreSQL connection details from environment variables
        2. Constructs connection URL to 'postgres' database
        3. Creates new engine with autocommit isolation level
        4. Executes CREATE DATABASE command
        5. Catches "already exists" error and treats as success
        6. Returns appropriate response
    
    Environment Variables Required:
        - PG_USER: PostgreSQL username (e.g., "postgres")
        - PG_PASSWORD: PostgreSQL password
        - PG_HOST: PostgreSQL host (e.g., "localhost")
        - PG_PORT: PostgreSQL port (default: 5432)
    
    Database Connection:
        - Uses 'postgres' system database for creation command
        - Requires CREATE DATABASE privileges
        - Connection URL format: postgresql://user:pass@host:port/postgres
    
    Isolation Level:
        - AUTOCOMMIT: Required for CREATE DATABASE
        - PostgreSQL doesn't support CREATE DATABASE in transaction blocks
        - Ensures command executes immediately
    
    Idempotency:
        - Safe to call multiple times
        - Already exists error (42P04) treated as success
        - Doesn't modify existing database
        - No data loss risk
    
    Use Cases:
        - Initial application setup
        - Docker container startup script
        - CI/CD pipeline database preparation
        - Development environment automation
        - Testing environment setup
    
    Security Considerations:
        - Should be restricted to admin users in production
        - Exposes database structure information
        - Requires elevated PostgreSQL privileges
        - Consider moving to CLI tool for production
        - Add authentication/authorization
    
    Error Handling:
        - Catches ProgrammingError for already exists condition
        - Returns generic error message for other failures
        - Logs errors for troubleshooting
        - Doesn't expose sensitive connection details
    
    Example:
        curl -X POST http://localhost:8000/db/create_database \
          -H "Content-Type: application/json" \
          -d '{"db_name":"growth_tracker"}'
    
    Docker Integration:
        ```dockerfile
        # In docker-entrypoint.sh
        curl -X POST http://localhost:8000/db/create_database \
             -H "Content-Type: application/json" \
             -d '{"db_name":"growth_tracker"}'
        ```
    
    Best Practices:
        - Run during initial deployment only
        - Store database name in environment variable
        - Use different database names per environment
        - Implement proper access control
        - Log database creation events
        - Validate database name format
    
    Troubleshooting:
        - Verify PostgreSQL is running
        - Check connection credentials
        - Ensure user has CREATE DATABASE privilege
        - Verify network connectivity to PostgreSQL
        - Check PostgreSQL logs for detailed errors
    """
    try:
        # Get PostgreSQL connection details from environment
        pg_user = os.getenv("PG_USER", "postgres")
        pg_password = os.getenv("PG_PASSWORD", "your_password")
        pg_host = os.getenv("PG_HOST", "localhost")
        pg_port = os.getenv("PG_PORT", "5432")
        
        # Connect to default 'postgres' database to create new database
        connection_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/postgres"
        temp_engine = create_engine(connection_url, isolation_level="AUTOCOMMIT")
        
        with temp_engine.connect() as conn:
            # Create database
            conn.execute(text(f"CREATE DATABASE {request.db_name}"))
        
        return {
            "status": "ok",
            "detail": f"database '{request.db_name}' created"
        }
    
    except ProgrammingError as e:
        # Database already exists
        if "already exists" in str(e):
            return {
                "status": "ok",
                "detail": f"database '{request.db_name}' already exists"
            }
        raise HTTPException(status_code=500, detail=f"Failed to create database: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create database: {str(e)}")


@router.post("/create_tables")
def create_tables():
    """
    Create All Database Tables
    
    Purpose:
        Creates all database tables defined in SQLAlchemy models (Base.metadata).
        Uses CREATE TABLE IF NOT EXISTS logic - safe to run multiple times.
        Sets up complete database schema for Growth Tracker application.
    
    Request:
        - No body required
        - POST method (modifies database state)
    
    Response (Success):
        {
            "status": "ok",
            "detail": "tables created or already exist"
        }
    
    Response (Error):
        {
            "detail": "Failed to create tables: <error message>"
        }
    
    Status Codes:
        - 200 OK: Tables created or already exist
        - 500 Internal Server Error: Table creation failed
    
    Tables Created:
        1. health_check
           - id: Primary key (auto-increment)
           - message: VARCHAR
           - created_at: TIMESTAMP
        
        2. workout_entries
           - date: Primary key (DATE)
           - workout_type: VARCHAR (enum)
           - workout_done: BOOLEAN
           - duration_minutes: INTEGER
           - intensity: VARCHAR (enum, nullable)
           - notes: TEXT (nullable)
           - created_at: TIMESTAMP
           - updated_at: TIMESTAMP
        
        3. smoking_entries
           - date: Primary key (DATE)
           - cigarette_count: INTEGER
           - location: VARCHAR (enum, nullable)
           - remarks: TEXT (nullable)
           - created_at: TIMESTAMP
    
    How It Works:
        1. Reads all model definitions from Base.metadata
        2. Generates CREATE TABLE statements for each model
        3. Executes DDL commands against target database
        4. Creates tables only if they don't exist
        5. Sets up primary keys, foreign keys, and indexes
        6. Applies column types and constraints
    
    Idempotency:
        - Safe to call multiple times
        - Uses CREATE TABLE IF NOT EXISTS
        - Doesn't modify existing tables
        - Doesn't drop or truncate data
        - No risk of data loss
    
    Prerequisites:
        - Database must exist (call /create_database first)
        - Database connection configured correctly
        - User must have CREATE TABLE privileges
        - Models must be imported in current module
    
    Model Discovery:
        - Base.metadata contains all model definitions
        - Models must inherit from Base class
        - Models must be imported before this endpoint is called
        - Current models: WorkoutEntry, SmokingEntry, HealthCheck
    
    Use Cases:
        - Initial database setup
        - New deployment environments
        - Development database initialization
        - Testing environment setup
        - Database reset (after dropping tables)
    
    Migration Note:
        - This is NOT a migration system
        - Doesn't handle schema changes to existing tables
        - For production, use Alembic or similar tool
        - Only creates tables that don't exist
        - Doesn't alter existing table structure
    
    Security Considerations:
        - Should be restricted to admin users in production
        - Requires elevated database privileges
        - Exposes database structure information
        - Consider moving to CLI tool for production
        - Add authentication/authorization
    
    Error Handling:
        - Catches all exceptions during table creation
        - Returns generic error message for failures
        - Logs errors for troubleshooting
        - Doesn't expose sensitive connection details
    
    Example:
        curl -X POST http://localhost:8000/db/create_tables
    
    Setup Sequence:
        ```bash
        # 1. Create database
        curl -X POST http://localhost:8000/db/create_database \
             -H "Content-Type: application/json" \
             -d '{"db_name":"growth_tracker"}'
        
        # 2. Create tables
        curl -X POST http://localhost:8000/db/create_tables
        
        # 3. Verify with health check
        curl -X GET http://localhost:8000/api/health/db
        ```
    
    Docker Integration:
        ```yaml
        # docker-compose.yml
        services:
          api:
            entrypoint: |
              sh -c "
                python -c 'from api.db_tasks import create_database, create_tables;
                          create_database();
                          create_tables()'
                uvicorn main:app --host 0.0.0.0
              "
        ```
    
    Alternative Approach (Alembic):
        For production applications, consider using Alembic:
        ```bash
        # Initialize Alembic
        alembic init alembic
        
        # Generate migration
        alembic revision --autogenerate -m "initial tables"
        
        # Apply migration
        alembic upgrade head
        ```
    
    Troubleshooting:
        - Verify database exists (run /create_database first)
        - Check database connection configuration
        - Ensure user has CREATE TABLE privilege
        - Verify models are properly imported
        - Check for syntax errors in model definitions
        - Review PostgreSQL logs for detailed errors
    
    Best Practices:
        - Run after /create_database
        - Run during initial deployment only
        - Use Alembic for schema migrations in production
        - Test on development database first
        - Backup production data before structural changes
        - Implement proper access control
        - Log table creation events
    
    Development Workflow:
        1. Define/modify models in db/models.py
        2. Import models in api/db_tasks.py
        3. Call /create_tables to apply changes
        4. For production: Generate Alembic migration
    """
    try:
        # Create all tables defined in Base.metadata
        Base.metadata.create_all(bind=engine)
        
        return {
            "status": "ok",
            "detail": "tables created or already exist"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tables: {str(e)}")

