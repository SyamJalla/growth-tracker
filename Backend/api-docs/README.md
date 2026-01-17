# API Documentation

This folder contains comprehensive documentation for the Growth Tracker API.

## Available Documentation Formats

### 📄 Markdown Documentation
**File:** `API-Documentation.md`

Comprehensive API documentation in Markdown format, perfect for:
- Reading in any text editor
- Viewing on GitHub
- Converting to other formats
- Version control tracking

**Features:**
- Complete endpoint reference
- Request/response examples
- Error handling guide
- Data models and schemas
- Version history

### 🌐 HTML Documentation
**File:** `API-Documentation.html`

Beautifully formatted HTML documentation with:
- Professional styling
- Syntax-highlighted code blocks
- Interactive table of contents
- Print-friendly layout
- Easy navigation

**How to Use:**
Simply open `API-Documentation.html` in any web browser.

### 📮 Postman Collection
**File:** `growth-tracker.postman_collection.json`

Complete Postman collection with:
- All API endpoints configured
- Pre-filled request examples
- Response samples
- Environment variables
- Organized folders

**How to Import:**
1. Open Postman
2. Click "Import" button
3. Select `growth-tracker.postman_collection.json`
4. Start testing immediately!

---

## Current Version: 2.3

**Release Date:** January 17, 2026  
**Update:** Frontend Bug Fixes & Platform Compatibility

### What's New in v2.3

#### ✅ Fixed Issues

**Dashboard Field Names Corrected:**
- `total_workouts` → `total_workout_days`
- `avg_duration` → `average_duration`
- `current_streak` → `current_clean_streak` (smoking stats)
- `longest_streak` → `longest_clean_streak` (smoking stats)

**Workout Type Enum Synchronized:**
- Updated to: `Push`, `Pull`, `Legs`, `Upper`, `Lower`, `Cardio`, `Others`
- Removed legacy types

**Intensity Level Correction:**
- Changed: `Medium` → `Moderate`
- Now: `Low`, `Moderate`, `High`

**Date Handling Improvements:**
- Added timezone normalization (`T00:00:00`)
- Platform-specific date pickers (web vs mobile)
- Consistent date formatting across clients

**Web Browser Compatibility:**
- HTML5 date input for web clients
- Native pickers for iOS/Android
- Improved cross-platform consistency

#### 📝 Documentation Updates

- All field names updated across all docs
- Enum values documented and synchronized
- Platform-specific implementation notes added
- Date handling best practices included
- Frontend integration guide enhanced

---

## Quick Start Guide

### 1. Choose Your Format

- **Developers:** Use Markdown (`API-Documentation.md`) for integration reference
- **Testing:** Import Postman collection for immediate API testing
- **Presentation:** Open HTML (`API-Documentation.html`) for client/team reviews

### 2. Set Up Your Environment

```bash
# Base URL (default)
http://localhost:8000

# Update in Postman collection variables if needed
```

### 3. First API Calls

```bash
# Test connection
curl http://localhost:8000/

# Check health
curl http://localhost:8000/api/health/

# Get dashboard data
curl http://localhost:8000/api/dashboard/
```

---

## API Overview

### Base URL
```
http://localhost:8000
```

### Key Endpoints

#### Health & Status
- `GET /` - API status
- `GET /api/health/` - Application health
- `GET /api/health/db` - Database health

#### Database Setup
- `POST /db/create_database` - Create database
- `POST /db/create_tables` - Create tables

#### Dashboard
- `GET /api/dashboard/` - Get all KPIs and statistics

#### Workout Tracker
- `POST /api/workouts/upsert/` ⭐ - Create/update workout (recommended)
- `POST /api/workouts/` - Create workout
- `GET /api/workouts/{date}` - Get workout by date
- `PUT /api/workouts/{date}` - Update workout
- `DELETE /api/workouts/{date}` - Delete workout
- `GET /api/workouts/history/` - Get workout history

#### Smoking Tracker
- `POST /api/smoking/upsert/` ⭐ - Create/update smoking entry (recommended)
- `POST /api/smoking/` - Create smoking entry
- `GET /api/smoking/{date}` - Get smoking entry by date
- `DELETE /api/smoking/{date}` - Delete smoking entry
- `GET /api/smoking/history/` - Get smoking history

---

## Data Models (v2.3)

### Dashboard Response
```json
{
  "workout": {
    "current_streak": 15,
    "longest_streak": 15,
    "total_workout_days": 12,       // ✅ Corrected field name
    "total_days": 17,
    "workout_percentage": 70.6,
    "average_duration": 45.5,        // ✅ Corrected field name
    "most_common_type": "Push"
  },
  "smoking": {
    "current_clean_streak": 7,       // ✅ Corrected field name
    "longest_clean_streak": 12,      // ✅ Corrected field name
    "total_relapses": 3,
    "total_cigarettes": 15,
    "most_common_location": "Social"
  },
  "last_updated": "2026-01-17"
}
```

### Workout Entry
```json
{
  "date": "2026-01-17",
  "workout_type": "Push",              // ✅ Push, Pull, Legs, Upper, Lower, Cardio, Others
  "workout_done": true,
  "duration_minutes": 45,
  "intensity": "High",                 // ✅ Low, Moderate, High
  "notes": "Great session",
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:30:00"
}
```

### Smoking Entry
```json
{
  "date": "2026-01-10",
  "cigarette_count": 3,
  "location": "Social",                // Home, Work, Social, Other
  "remarks": "Party with friends",
  "created_at": "2026-01-10T20:00:00"
}
```

---

## Enums Reference (v2.3)

### Workout Types
- `Push` - Push exercises (chest, shoulders, triceps)
- `Pull` - Pull exercises (back, biceps)
- `Legs` - Leg exercises (squats, lunges, etc.)
- `Upper` - Upper body mixed
- `Lower` - Lower body mixed
- `Cardio` - Cardiovascular exercises
- `Others` - Other workout types

### Intensity Levels
- `Low` - Light effort
- `Moderate` - Medium effort ✅ (changed from "Medium")
- `High` - Maximum effort

### Location Types
- `Home` - At home
- `Work` - At workplace
- `Social` - Social gatherings
- `Other` - Other locations

---

## Date Format Guidelines

### Backend Format
- **Format:** `YYYY-MM-DD` (ISO 8601)
- **Example:** `2026-01-17`
- **Type:** DATE (no time component)
- **Usage:** Primary key for entries

### Frontend Handling (v2.3)

**Web Browser:**
```javascript
// HTML5 date input
<input type="date" value="2026-01-17" />
```

**Mobile (React Native):**
```javascript
// Native DateTimePicker
import DateTimePicker from '@react-native-community/datetimepicker';
```

**Best Practice - Parsing:**
```javascript
// Always append T00:00:00 to prevent timezone issues
const date = new Date("2026-01-17T00:00:00");
```

**Best Practice - Formatting:**
```javascript
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};
```

---

## Common HTTP Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid parameters or duplicate entry |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation failed |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Database unreachable |

---

## Authentication

**Current Status:** None required

All endpoints are currently open and do not require authentication. Future versions will implement authentication and authorization.

---

## Version History

### Version 2.3 (January 17, 2026)
**Frontend Bug Fixes & Platform Compatibility**

**Fixed:**
- ✅ Dashboard field name corrections
- ✅ Workout type enum synchronized
- ✅ Intensity level correction (Medium → Moderate)
- ✅ Date handling improvements
- ✅ Web browser compatibility

**Details:** See full documentation for complete change list.

### Version 2.2 (January 13, 2026)
**Historical Date Support**

**Added:**
- ✅ Upsert endpoints for both trackers
- ✅ Dashboard with comprehensive KPIs
- ✅ Streak calculation logic
- ✅ Historical date entry support

### Version 2.0 (January 13, 2026)
**Full CRUD Implementation**

**Added:**
- ✅ Complete workout tracker endpoints
- ✅ Complete smoking tracker endpoints
- ✅ Date-based primary keys
- ✅ Enum validation

### Version 1.0 (January 13, 2026)
**Initial Release**

**Added:**
- ✅ Root endpoint
- ✅ Health check endpoints
- ✅ Database setup utilities

---

## Support & Resources

### Interactive Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Testing Tools
- **Postman:** Import `growth-tracker.postman_collection.json`
- **cURL:** Examples provided in all documentation

### Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Server:** Uvicorn
- **Frontend:** React Native (Web + Mobile)

---

## Contributing

When updating documentation:

1. **Maintain all formats** - Update Markdown, HTML, and Postman collection
2. **Increment version** - Follow semantic versioning
3. **Document changes** - Add to version history
4. **Test examples** - Verify all code examples work
5. **Update README** - Keep this file current

---

## File Structure

```
api-docs/
├── README.md                              # This file
├── API-Documentation.md                   # Markdown documentation
├── API-Documentation.html                 # HTML documentation
└── growth-tracker.postman_collection.json # Postman collection
```

---

## Quick Reference Card

### Most Used Endpoints

```bash
# Dashboard (all KPIs)
GET /api/dashboard/

# Create/update workout (recommended)
POST /api/workouts/upsert/

# Create/update smoking entry (recommended)
POST /api/smoking/upsert/

# Get workout history
GET /api/workouts/history/?start_date=2026-01-01&end_date=2026-01-31

# Get smoking history
GET /api/smoking/history/?start_date=2026-01-01&end_date=2026-01-31
```

### Field Mapping (v2.3)
```javascript
// ✅ CORRECT field names
dashboard.workout.total_workout_days
dashboard.workout.average_duration
dashboard.smoking.current_clean_streak
dashboard.smoking.longest_clean_streak

// ❌ OLD field names (deprecated)
// dashboard.workout.total_workouts
// dashboard.workout.avg_duration
// dashboard.smoking.current_streak
// dashboard.smoking.longest_streak
```

---

## License

[Add your license information here]

---

**Last Updated:** January 17, 2026  
**Current Version:** 2.3  
**Status:** Production Ready ✅

---

*For detailed API reference, see `API-Documentation.md` or open `API-Documentation.html` in your browser.*
