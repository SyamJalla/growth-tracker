# Growth Tracker API Documentation

**Version:** 2.3  
**Base URL:** `http://localhost:8000`  
**Last Updated:** January 17, 2026 (VERSION 2.3 - Frontend Bug Fixes & Platform Compatibility)

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
   - [Root Endpoint](#root-endpoint)
   - [Health Check](#health-check)
   - [Dashboard](#dashboard)
   - [Workout Tracker](#workout-tracker)
   - [Smoking Tracker](#smoking-tracker)
   - [Database Setup](#database-setup)
5. [Error Handling](#error-handling)
6. [Data Models](#data-models)
7. [Version History](#version-history)

---

## Overview

The Growth Tracker API is a FastAPI-based backend service designed to track personal growth metrics. It provides endpoints for health monitoring, database management, and features for tracking smoking and workout activities.

### Features

- ✅ Health check endpoints for application and database monitoring
- ✅ Database initialization and management utilities
- ✅ Dashboard with comprehensive KPIs (streaks, totals, percentages)
- ✅ Workout tracker with CRUD operations
- ✅ Smoking tracker with CRUD operations
- ✅ Upsert endpoints for seamless historical data entry
- ✅ RESTful API design
- ✅ CORS support for cross-origin requests
- ✅ Web browser compatibility for frontend clients

### Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Server:** Uvicorn
- **Frontend:** React Native (Web + Mobile)

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

### Dashboard

Get all KPIs and statistics in a single call.

#### Get Dashboard Data

Returns comprehensive statistics for both workout and smoking tracking.

**Endpoint:** `GET /api/dashboard/`

**Response (Success):**

```json
{
  "workout": {
    "current_streak": 15,
    "longest_streak": 15,
    "total_workout_days": 12,
    "total_days": 17,
    "workout_percentage": 70.6,
    "average_duration": 45.5,
    "most_common_type": "Push"
  },
  "smoking": {
    "current_clean_streak": 7,
    "longest_clean_streak": 12,
    "total_relapses": 3,
    "total_cigarettes": 15,
    "most_common_location": "Social"
  },
  "last_updated": "2026-01-17"
}
```

**Field Descriptions:**

**Workout Stats:**
- `current_streak` - Current consecutive workout days
- `longest_streak` - Best workout streak achieved
- `total_workout_days` - Total days with workouts logged
- `total_days` - Total days in tracking period (2026)
- `workout_percentage` - Percentage of days with workouts
- `average_duration` - Average workout duration in minutes
- `most_common_type` - Most frequently performed workout type

**Smoking Stats:**
- `current_clean_streak` - Current consecutive smoke-free days
- `longest_clean_streak` - Best clean streak achieved
- `total_relapses` - Total number of relapse days
- `total_cigarettes` - Total cigarettes smoked across all entries
- `most_common_location` - Most common relapse location

**Status Codes:**
- `200 OK` - Dashboard data retrieved successfully

**Example Request:**

```bash
curl -X GET http://localhost:8000/api/dashboard/
```

**Use Case:** Primary endpoint for mobile dashboard screen. Returns all calculated KPIs for calendar year 2026.

**Version 2.3 Notes:**
- ✅ Field names corrected (January 17, 2026)
- ✅ `total_workout_days` replaces `total_workouts`
- ✅ `average_duration` replaces `avg_duration`
- ✅ `current_clean_streak` replaces `current_streak` in smoking stats
- ✅ `longest_clean_streak` replaces `longest_streak` in smoking stats
- Frontend synchronized to match these field names

---

### Workout Tracker

Endpoints for managing workout entries. Supports full CRUD operations plus smart upsert functionality.

#### Workout Types (Enum)

Valid workout types (updated in v2.3):

- `Push` - Push exercises (chest, shoulders, triceps)
- `Pull` - Pull exercises (back, biceps)
- `Legs` - Leg exercises (squats, lunges, etc.)
- `Upper` - Upper body mixed
- `Lower` - Lower body mixed
- `Cardio` - Cardiovascular exercises
- `Others` - Other workout types

#### Intensity Levels (Enum)

Valid intensity levels (updated in v2.3):

- `Low` - Light effort
- `Moderate` - Medium effort (previously "Medium")
- `High` - Maximum effort

---

#### 1. Create Workout Entry

Creates a new workout entry for a specific date. Returns error if entry already exists.

**Endpoint:** `POST /api/workouts/`

**Request Body:**

```json
{
  "date": "2026-01-17",
  "workout_type": "Push",
  "workout_done": true,
  "duration_minutes": 45,
  "intensity": "High",
  "notes": "Great chest session"
}
```

**Response (Success):**

```json
{
  "date": "2026-01-17",
  "workout_type": "Push",
  "workout_done": true,
  "duration_minutes": 45,
  "intensity": "High",
  "notes": "Great chest session",
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:30:00"
}
```

**Status Codes:**
- `201 Created` - Entry created successfully
- `400 Bad Request` - Entry already exists for this date

---

#### 2. Upsert Workout Entry (Recommended) ⭐

Creates or updates workout entry for a specific date. Smart endpoint that automatically handles both create and update operations.

**Endpoint:** `POST /api/workouts/upsert/`

**Request Body:**

```json
{
  "date": "2026-01-05",
  "workout_type": "Pull",
  "workout_done": true,
  "duration_minutes": 60,
  "intensity": "Moderate",
  "notes": "Back and biceps"
}
```

**Response (Success):**

```json
{
  "date": "2026-01-05",
  "workout_type": "Pull",
  "workout_done": true,
  "duration_minutes": 60,
  "intensity": "Moderate",
  "notes": "Back and biceps",
  "created_at": "2026-01-05T09:00:00",
  "updated_at": "2026-01-17T11:00:00"
}
```

**Status Codes:**
- `200 OK` - Entry created or updated successfully

**Benefits:**
- ✅ No duplicate entry errors
- ✅ Single API call for all operations
- ✅ Ideal for historical date entry
- ✅ Idempotent (safe to retry)
- ✅ Used by web and mobile clients

---

#### 3. Get Workout Entry

Retrieves workout entry for a specific date.

**Endpoint:** `GET /api/workouts/{date}`

**Path Parameters:**
- `date` (string, required): Date in YYYY-MM-DD format

**Response (Success):**

```json
{
  "date": "2026-01-17",
  "workout_type": "Push",
  "workout_done": true,
  "duration_minutes": 45,
  "intensity": "High",
  "notes": "Great session",
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:30:00"
}
```

**Status Codes:**
- `200 OK` - Entry found
- `404 Not Found` - No entry for this date

---

#### 4. Update Workout Entry

Updates existing workout entry for a specific date.

**Endpoint:** `PUT /api/workouts/{date}`

**Path Parameters:**
- `date` (string, required): Date in YYYY-MM-DD format

**Request Body:**

```json
{
  "workout_type": "Legs",
  "duration_minutes": 50,
  "intensity": "High"
}
```

**Response (Success):**

```json
{
  "date": "2026-01-17",
  "workout_type": "Legs",
  "workout_done": true,
  "duration_minutes": 50,
  "intensity": "High",
  "notes": "Great session",
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T15:00:00"
}
```

**Status Codes:**
- `200 OK` - Entry updated successfully
- `404 Not Found` - No entry exists for this date

---

#### 5. Delete Workout Entry

Deletes workout entry for a specific date.

**Endpoint:** `DELETE /api/workouts/{date}`

**Path Parameters:**
- `date` (string, required): Date in YYYY-MM-DD format

**Response (Success):** No content

**Status Codes:**
- `204 No Content` - Entry deleted successfully
- `404 Not Found` - No entry exists for this date

---

#### 6. Get Workout History

Retrieves list of all workout entries with optional date filtering.

**Endpoint:** `GET /api/workouts/history/`

**Query Parameters:**
- `start_date` (string, optional): Filter from this date (YYYY-MM-DD)
- `end_date` (string, optional): Filter until this date (YYYY-MM-DD)

**Response (Success):**

```json
[
  {
    "date": "2026-01-17",
    "workout_type": "Push",
    "workout_done": true,
    "duration_minutes": 45,
    "intensity": "High",
    "notes": "Great session",
    "created_at": "2026-01-17T10:30:00",
    "updated_at": "2026-01-17T10:30:00"
  },
  {
    "date": "2026-01-16",
    "workout_type": "Pull",
    "workout_done": true,
    "duration_minutes": 50,
    "intensity": "Moderate",
    "notes": null,
    "created_at": "2026-01-16T09:00:00",
    "updated_at": "2026-01-16T09:00:00"
  }
]
```

**Status Codes:**
- `200 OK` - List retrieved successfully (may be empty)

**Example Requests:**

```bash
# Get all workouts
curl -X GET http://localhost:8000/api/workouts/history/

# Get workouts for January 2026
curl -X GET "http://localhost:8000/api/workouts/history/?start_date=2026-01-01&end_date=2026-01-31"
```

---

### Smoking Tracker

Endpoints for managing smoking entries. Each entry represents a relapse day.

#### Location Types (Enum)

Valid locations:

- `Home` - At home
- `Work` - At workplace
- `Social` - Social gatherings
- `Other` - Other locations

---

#### 1. Create Smoking Entry

Creates a new smoking entry for a specific date. Returns error if entry already exists.

**Endpoint:** `POST /api/smoking/`

**Request Body:**

```json
{
  "date": "2026-01-10",
  "cigarette_count": 3,
  "location": "Social",
  "remarks": "Party with friends"
}
```

**Response (Success):**

```json
{
  "date": "2026-01-10",
  "cigarette_count": 3,
  "location": "Social",
  "remarks": "Party with friends",
  "created_at": "2026-01-10T20:00:00"
}
```

**Status Codes:**
- `201 Created` - Entry created successfully
- `400 Bad Request` - Entry already exists for this date

---

#### 2. Upsert Smoking Entry (Recommended) ⭐

Creates or updates smoking entry for a specific date. Recommended for all data entry operations.

**Endpoint:** `POST /api/smoking/upsert/`

**Request Body:**

```json
{
  "date": "2026-01-10",
  "cigarette_count": 5,
  "location": "Work",
  "remarks": "Stressful day"
}
```

**Response (Success):**

```json
{
  "date": "2026-01-10",
  "cigarette_count": 5,
  "location": "Work",
  "remarks": "Stressful day",
  "created_at": "2026-01-10T20:00:00"
}
```

**Status Codes:**
- `200 OK` - Entry created or updated successfully

**Benefits:**
- ✅ No duplicate entry errors
- ✅ Single API call for all operations
- ✅ Ideal for historical date entry
- ✅ Clean streak recalculates automatically

---

#### 3. Get Smoking Entry

Retrieves smoking entry for a specific date.

**Endpoint:** `GET /api/smoking/{date}`

**Path Parameters:**
- `date` (string, required): Date in YYYY-MM-DD format

**Response (Success):**

```json
{
  "date": "2026-01-10",
  "cigarette_count": 3,
  "location": "Social",
  "remarks": "Party with friends",
  "created_at": "2026-01-10T20:00:00"
}
```

**Status Codes:**
- `200 OK` - Entry found
- `404 Not Found` - No entry for this date

---

#### 4. Delete Smoking Entry

Deletes smoking entry for a specific date.

**Endpoint:** `DELETE /api/smoking/{date}`

**Path Parameters:**
- `date` (string, required): Date in YYYY-MM-DD format

**Response (Success):** No content

**Status Codes:**
- `204 No Content` - Entry deleted successfully
- `404 Not Found` - No entry exists for this date

---

#### 5. Get Smoking History

Retrieves list of all smoking entries with optional date filtering.

**Endpoint:** `GET /api/smoking/history/`

**Query Parameters:**
- `start_date` (string, optional): Filter from this date (YYYY-MM-DD)
- `end_date` (string, optional): Filter until this date (YYYY-MM-DD)

**Response (Success):**

```json
[
  {
    "date": "2026-01-10",
    "cigarette_count": 3,
    "location": "Social",
    "remarks": "Party with friends",
    "created_at": "2026-01-10T20:00:00"
  },
  {
    "date": "2026-01-05",
    "cigarette_count": 2,
    "location": "Work",
    "remarks": null,
    "created_at": "2026-01-05T12:00:00"
  }
]
```

**Status Codes:**
- `200 OK` - List retrieved successfully (may be empty)

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
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request parameters or duplicate entry |
| 404 | Not Found | Resource or endpoint doesn't exist |
| 422 | Unprocessable Entity | Request validation failed |
| 500 | Internal Server Error | Server-side error occurred |
| 503 | Service Unavailable | Database or service unreachable |

### Example Error Responses

**Validation Error (422):**

```json
{
  "detail": [
    {
      "loc": ["body", "workout_type"],
      "msg": "value is not a valid enumeration member; permitted: 'Push', 'Pull', 'Legs', 'Upper', 'Lower', 'Cardio', 'Others'",
      "type": "type_error.enum"
    }
  ]
}
```

**Duplicate Entry (400):**

```json
{
  "detail": "Entry already exists for 2026-01-17"
}
```

**Database Unreachable (503):**

```json
{
  "detail": "Database unreachable"
}
```

---

## Data Models

### Dashboard Response

```typescript
{
  workout: {
    current_streak: number,        // Current workout streak (days)
    longest_streak: number,        // Best workout streak
    total_workout_days: number,    // Total days with workouts
    total_days: number,            // Total tracking days
    workout_percentage: number,    // Workout adherence %
    average_duration: number,      // Avg workout duration (min)
    most_common_type: string       // Most frequent workout type
  },
  smoking: {
    current_clean_streak: number,  // Current smoke-free days
    longest_clean_streak: number,  // Best clean streak
    total_relapses: number,        // Total relapse days
    total_cigarettes: number,      // Total cigarettes smoked
    most_common_location: string   // Most common relapse location
  },
  last_updated: string             // ISO date string
}
```

### Workout Entry

```typescript
{
  date: string,                    // YYYY-MM-DD format (primary key)
  workout_type: WorkoutType,       // Push | Pull | Legs | Upper | Lower | Cardio | Others
  workout_done: boolean,           // Whether workout was completed
  duration_minutes: number,        // Workout duration
  intensity?: IntensityLevel,      // Low | Moderate | High (optional)
  notes?: string,                  // Optional notes (optional)
  created_at: string,              // ISO timestamp
  updated_at: string               // ISO timestamp
}
```

### Smoking Entry

```typescript
{
  date: string,                    // YYYY-MM-DD format (primary key)
  cigarette_count: number,         // Number of cigarettes (min: 1)
  location?: Location,             // Home | Work | Social | Other (optional)
  remarks?: string,                // Optional notes (optional)
  created_at: string               // ISO timestamp
}
```

### Date Format Notes

**Backend:**
- All dates stored as DATE type (no time component)
- Format: `YYYY-MM-DD` (ISO 8601)
- Example: `"2026-01-17"`
- Date is the primary key for entries

**Frontend Handling (v2.3):**
- Web: Uses HTML5 `<input type="date">`
- Mobile: Uses native DateTimePicker component
- Parsing: Always append `T00:00:00` to prevent timezone issues
- Example: `new Date("2026-01-17T00:00:00")`
- This ensures correct date display regardless of user timezone

---

## Version History

### Version 2.3 (January 17, 2026) - Frontend Bug Fixes

**Fixed:**
- ✅ Dashboard field name corrections
  - `total_workouts` → `total_workout_days`
  - `avg_duration` → `average_duration`
  - `current_streak` → `current_clean_streak` (smoking)
  - `longest_streak` → `longest_clean_streak` (smoking)
- ✅ Workout type enum synchronized
  - Updated to: Push, Pull, Legs, Upper, Lower, Cardio, Others
- ✅ Intensity level correction
  - Changed: Medium → Moderate
- ✅ Date handling improvements
  - Added timezone normalization (T00:00:00)
  - Platform-specific date pickers (web vs mobile)
- ✅ Web browser compatibility
  - HTML5 date input for web clients
  - Native pickers for iOS/Android

**Frontend Changes:**
- 8 files modified
- ~380 lines changed
- Platform detection added (web vs mobile)
- Date formatting standardized
- Color scheme improved

**Documentation:**
- API docs updated with correct field names
- Enum values documented
- Platform-specific notes added
- Date handling best practices included

---

### Version 2.2 (January 13, 2026) - Historical Date Support

**Added:**
- ✅ Upsert endpoints for both workout and smoking
- ✅ Dashboard endpoint with comprehensive KPIs
- ✅ Streak calculation logic
- ✅ Historical date entry support
- ✅ Most common workout type tracking
- ✅ Location-based smoking statistics

**Improved:**
- Better error messages
- Idempotent operations
- Clean streak recalculation

---

### Version 2.0 (January 13, 2026) - Full CRUD Implementation

**Added:**
- ✅ Complete workout tracker endpoints
- ✅ Complete smoking tracker endpoints
- ✅ Date-based primary keys
- ✅ Enum validation for types and intensity
- ✅ Comprehensive test coverage (84%)

---

### Version 1.0 (January 13, 2026) - Initial Release

**Added:**
- ✅ Root endpoint
- ✅ Health check endpoints
- ✅ Database setup utilities
- ✅ Basic API structure

---

## Frontend Integration Notes

### React Native Client

**Web Browser:**
- Uses HTML5 `<input type="date">` for date selection
- Detects platform via `Platform.OS === 'web'`
- Date stored as string (YYYY-MM-DD)

**Mobile (iOS/Android):**
- Uses `@react-native-community/datetimepicker`
- Native date picker UI
- Date stored as Date object, converted to string for API

**Date Handling Best Practice:**
```javascript
// Parsing date from API
const date = new Date(apiDate + 'T00:00:00'); // Timezone safe

// Formatting for API
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};
```

**Field Mapping Reference:**
```javascript
// Dashboard
dashboardResponse.data.workout.current_streak ✅
dashboardResponse.data.workout.total_workout_days ✅
dashboardResponse.data.workout.average_duration ✅
dashboardResponse.data.smoking.current_clean_streak ✅
dashboardResponse.data.smoking.longest_clean_streak ✅

// Workout Entry
entry.date ✅
entry.workout_type ✅
entry.duration_minutes ✅
entry.intensity ✅

// Smoking Entry
entry.date ✅
entry.cigarette_count ✅
entry.location ✅
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
│   ├── dashboard.py  # Dashboard KPIs
│   ├── workout.py    # Workout CRUD
│   ├── smoking.py    # Smoking CRUD
│   └── health.py     # Health checks
├── core/             # Settings and configuration
├── db/               # Database models and connection
├── api-docs/         # API documentation (this file)
├── tests/            # Test files (84% coverage)
├── app.py            # Main application entry point
└── requirements.txt  # Python dependencies
```

---

## Support and Contact

For issues, questions, or contributions:

- **Interactive Docs:** http://localhost:8000/docs
- **GitHub Issues:** [Create an issue]
- **Email:** support@example.com

---

## License

[Add your license information here]

---

*Last Updated: January 17, 2026*  
*Version: 2.3*  
*API Status: Production Ready*

---

*End of Documentation*
