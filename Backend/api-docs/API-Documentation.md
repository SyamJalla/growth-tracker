# Growth Tracker API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:8000`  
**Last Updated:** January 13, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
   - [Root Endpoint](#root-endpoint)
   - [Health Check](#health-check)
   - [Database Setup](#database-setup)
5. [Error Handling](#error-handling)
6. [Data Models](#data-models)

---

## Overview

The Growth Tracker API is a FastAPI-based backend service designed to track personal growth metrics. It provides endpoints for health monitoring, database management, and future features for tracking smoking and workout activities.

### Features

- ✅ Health check endpoints for application and database monitoring
- ✅ Database initialization and management utilities
- ✅ RESTful API design
- ✅ CORS support for cross-origin requests
- 🔄 Smoking tracker (planned)
- 🔄 Workout tracker (planned)

### Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Server:** Uvicorn

---

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd growth-tracker/Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   
   Create a `.env` file or use default settings:
   ```
   DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker
   ADMIN_DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/postgres
   ```

4. **Start the server**
   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Initial Setup

After starting the server, initialize the database:

1. Create database: `POST /db/create_database`
2. Create tables: `POST /db/create_tables`
3. Verify: `GET /api/health/db`

---

## Authentication

**Current Version:** No authentication required

All endpoints are currently open and do not require authentication. Authentication and authorization will be added in future versions.

---

## API Endpoints

### Root Endpoint

#### Get API Status

Returns basic information about the API.

**Endpoint:** `GET /`

**Response:**

```json
{
  "status": "ok",
  "message": "Growth Tracker API"
}
```

**Status Codes:**
- `200 OK` - Service is running

**Example Request:**

```bash
curl -X GET http://localhost:8000/
```

---

### Health Check

Health monitoring endpoints to verify application and database status.

#### 1. Check Application Health

Verifies that the API application is running and responsive.

**Endpoint:** `GET /api/health/`

**Response:**

```json
{
  "status": "ok",
  "message": "Growth Tracker API running"
}
```

**Status Codes:**
- `200 OK` - Application is healthy

**Example Request:**

```bash
curl -X GET http://localhost:8000/api/health/
```

**Use Case:** Use this endpoint for basic application monitoring and uptime checks.

---

#### 2. Check Database Health

Verifies database connectivity by executing a lightweight query.

**Endpoint:** `GET /api/health/db`

**Response (Success):**

```json
{
  "status": "ok",
  "db": "ok"
}
```

**Response (Failure):**

```json
{
  "detail": "Database unreachable"
}
```

**Status Codes:**
- `200 OK` - Database is connected and responsive
- `503 Service Unavailable` - Database connection failed

**Example Request:**

```bash
curl -X GET http://localhost:8000/api/health/db
```

**Use Case:** Use this endpoint to monitor database connectivity. Ideal for health checks in container orchestration systems (Kubernetes, Docker Compose).

---

### Database Setup

Utility endpoints for database initialization. These should be run during first-time setup or when resetting the database.

#### 1. Create Database

Creates a new PostgreSQL database on the server.

**Endpoint:** `POST /db/create_database`

**Request Body:**

```json
{
  "db_name": "growth_tracker"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| db_name | string | Yes | Name of the database to create (default: "growth_tracker") |

**Response (Success - New Database):**

```json
{
  "status": "ok",
  "detail": "database 'growth_tracker' created"
}
```

**Response (Success - Already Exists):**

```json
{
  "status": "ok",
  "detail": "database 'growth_tracker' already exists"
}
```

**Response (Error):**

```json
{
  "detail": "<error message>"
}
```

**Status Codes:**
- `200 OK` - Database created successfully or already exists
- `500 Internal Server Error` - Failed to create database

**Example Request:**

```bash
curl -X POST http://localhost:8000/db/create_database \
  -H "Content-Type: application/json" \
  -d '{"db_name": "growth_tracker"}'
```

**Important Notes:**
- This endpoint connects to the admin database (typically 'postgres') using `admin_database_url`
- Requires appropriate PostgreSQL permissions to create databases
- Idempotent - safe to call multiple times
- Must be run before creating tables

---

#### 2. Create Tables

Creates all database tables defined in SQLAlchemy models.

**Endpoint:** `POST /db/create_tables`

**Request Body:** None required

**Response (Success):**

```json
{
  "status": "ok",
  "detail": "tables created or already exist"
}
```

**Response (Error):**

```json
{
  "detail": "<error message>"
}
```

**Status Codes:**
- `200 OK` - Tables created successfully or already exist
- `500 Internal Server Error` - Failed to create tables

**Example Request:**

```bash
curl -X POST http://localhost:8000/db/create_tables
```

**Important Notes:**
- Uses SQLAlchemy's `create_all()` method
- Idempotent - will not recreate existing tables
- Automatically creates all tables defined in `db/models.py`
- Database must exist before running this endpoint

---

## Error Handling

The API follows standard HTTP status codes and returns errors in a consistent format.

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Description | When It Occurs |
|------|-------------|----------------|
| 200 | OK | Request succeeded |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Endpoint doesn't exist |
| 422 | Unprocessable Entity | Request validation failed |
| 500 | Internal Server Error | Server-side error occurred |
| 503 | Service Unavailable | Database or service unreachable |

### Example Error Responses

**Validation Error (422):**

```json
{
  "detail": [
    {
      "loc": ["body", "db_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Database Unreachable (503):**

```json
{
  "detail": "Database unreachable"
}
```

**Internal Server Error (500):**

```json
{
  "detail": "FATAL: database \"growth_tracker\" does not exist"
}
```

---

## Data Models

### CreateDatabaseRequest

Used for creating a new database.

```python
{
  "db_name": "string"  # Required, default: "growth_tracker"
}
```

**Example:**

```json
{
  "db_name": "growth_tracker"
}
```

---

### Future Models

The following models are defined but not yet used in active endpoints:

#### SmokingEntry

```python
{
  "date": "string",           # Required, format: YYYY-MM-DD
  "cigarettes": "integer",    # Required
  "notes": "string"           # Optional
}
```

#### WorkoutEntry

```python
{
  "date": "string",           # Required, format: YYYY-MM-DD
  "activity": "string",       # Required (e.g., "Running", "Gym")
  "duration_minutes": "integer",  # Required
  "notes": "string"           # Optional
}
```

---

## Configuration

The API can be configured using environment variables or a `.env` file.

### Available Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| APP_NAME | string | "Growth Tracker API" | Application name |
| ENV | string | "dev" | Environment (dev, staging, prod) |
| DATABASE_URL | string | `postgresql+psycopg2://postgres:root@localhost:5432/growth_tracker` | Main database connection string |
| ADMIN_DATABASE_URL | string | `postgresql+psycopg2://postgres:root@localhost:5432/postgres` | Admin database for creating databases |
| CORS_ORIGINS | list | ["*"] | Allowed CORS origins |

### Example .env File

```env
APP_NAME=Growth Tracker API
ENV=production
DATABASE_URL=postgresql+psycopg2://user:password@db-host:5432/growth_tracker
ADMIN_DATABASE_URL=postgresql+psycopg2://user:password@db-host:5432/postgres
CORS_ORIGINS=["https://app.example.com"]
```

---

## Development

### Running Tests

```bash
pytest tests/
```

### API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Project Structure

```
Backend/
├── api/              # API route handlers
├── core/             # Settings and configuration
├── db/               # Database models and connection
├── api-docs/         # API documentation and Postman collection
├── tests/            # Test files
├── app.py            # Main application entry point
└── requirements.txt  # Python dependencies
```

---

## Support and Contact

For issues, questions, or contributions:

- **GitHub Issues:** [Create an issue]
- **Email:** support@example.com
- **Documentation:** This file

---

## Changelog

### Version 1.0.0 (January 13, 2026)

**Added:**
- Root endpoint for basic status
- Health check endpoints (app and database)
- Database creation endpoint
- Table creation endpoint
- API documentation

**Removed:**
- S3 service integration
- Alembic migration support

**Planned:**
- Smoking tracker endpoints
- Workout tracker endpoints
- Authentication and authorization
- User management

---

## License

[Add your license information here]

---

*End of Documentation*
