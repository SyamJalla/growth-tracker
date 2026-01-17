"""
Workout Tracker API Routes

This module provides CRUD operations for workout entries with
date-based tracking and comprehensive workout statistics.

Purpose:
    - Log daily workout activities
    - Track workout types, duration, and intensity
    - Support historical data entry and corrections
    - Provide workout history with date range filtering
    - Enable streak calculations and progress tracking

Routes:
    POST   /api/workouts/         - Create new workout entry
    POST   /api/workouts/upsert/  - Create or update workout entry (recommended)
    GET    /api/workouts/{date}   - Get workout entry by date
    PUT    /api/workouts/{date}   - Update existing workout entry
    DELETE /api/workouts/{date}   - Delete workout entry
    GET    /api/workouts/history/ - Get workout history with filtering

Data Model:
    - Primary Key: date (YYYY-MM-DD)
    - Workout Types: Push, Pull, Legs, Upper, Lower, Cardio, Others
    - Intensity Levels: Low, Moderate, High
    - Optional fields: notes, intensity
    - Timestamps: created_at, updated_at
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from db.database import get_db
from db.models import WorkoutEntry
from db.schemas import WorkoutCreate, WorkoutUpdate, WorkoutResponse

router = APIRouter()


@router.post("/", response_model=WorkoutResponse, status_code=201)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """
    Create New Workout Entry
    
    Purpose:
        Creates a new workout entry for a specific date. Returns an error
        if an entry already exists for that date.
    
    Request Body:
        {
            "date": "2026-01-17",            # Required: YYYY-MM-DD format
            "workout_type": "Push",          # Required: Enum value
            "workout_done": true,            # Required: Boolean
            "duration_minutes": 45,          # Required: Integer > 0
            "intensity": "High",             # Optional: Enum value
            "notes": "Great session"         # Optional: String
        }
    
    Validation:
        - date: Must be valid date in YYYY-MM-DD format
        - workout_type: Must be one of valid enum values
        - workout_done: Must be boolean
        - duration_minutes: Must be positive integer
        - intensity: Must be valid enum value if provided
        - notes: Optional string, max length determined by database
    
    Response (Success):
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
    
    Status Codes:
        - 201 Created: Entry created successfully
        - 400 Bad Request: Entry already exists for this date
        - 422 Unprocessable Entity: Validation failed
    
    Error Response (Duplicate):
        {
            "detail": "Entry already exists for 2026-01-17"
        }
    
    Use Cases:
        - Log today's workout
        - Manual data entry
        - Batch data import
    
    Recommendation:
        Use /upsert/ endpoint instead for:
        - Historical data entry
        - Updating existing entries
        - Avoiding duplicate errors
    
    Example:
        curl -X POST http://localhost:8000/api/workouts/ \
          -H "Content-Type: application/json" \
          -d '{"date":"2026-01-17","workout_type":"Push",
               "workout_done":true,"duration_minutes":45}'
    """
    # Check if entry already exists
    existing = db.query(WorkoutEntry).filter(WorkoutEntry.date == workout.date).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Entry already exists for {workout.date}")
    
    # Create new entry
    db_workout = WorkoutEntry(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.post("/upsert/", response_model=WorkoutResponse)
def upsert_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """
    Create or Update Workout Entry (Recommended)
    
    Purpose:
        Smart endpoint that automatically creates a new entry or updates
        an existing one based on the date. Eliminates duplicate entry errors
        and simplifies data entry logic.
    
    Request Body:
        {
            "date": "2026-01-17",
            "workout_type": "Push",
            "workout_done": true,
            "duration_minutes": 45,
            "intensity": "High",
            "notes": "Updated session"
        }
    
    Behavior:
        - If date doesn't exist: Creates new entry (like POST)
        - If date exists: Updates all fields (like PUT)
        - Always succeeds (no duplicate errors)
        - Idempotent (safe to retry)
        - Updates updated_at timestamp automatically
    
    Response:
        {
            "date": "2026-01-17",
            "workout_type": "Push",
            "workout_done": true,
            "duration_minutes": 45,
            "intensity": "High",
            "notes": "Updated session",
            "created_at": "2026-01-17T10:30:00",  # Preserved if updating
            "updated_at": "2026-01-17T15:00:00"   # Always updated
        }
    
    Status Codes:
        - 200 OK: Entry created or updated successfully
        - 422 Unprocessable Entity: Validation failed
    
    Benefits:
        ✅ No duplicate entry errors
        ✅ Single API call for all operations
        ✅ Ideal for historical date entry
        ✅ Idempotent (safe to retry)
        ✅ Used by web and mobile clients
        ✅ Simplifies frontend logic
    
    Use Cases:
        - Primary data entry method
        - Historical data entry
        - Data corrections
        - Sync operations
        - Import/export workflows
    
    Performance:
        - 1 query: Check if entry exists
        - 1 query: INSERT or UPDATE
        - Total: 2 database operations
    
    Example:
        curl -X POST http://localhost:8000/api/workouts/upsert/ \
          -H "Content-Type: application/json" \
          -d '{"date":"2026-01-17","workout_type":"Push",
               "workout_done":true,"duration_minutes":45}'
    
    Version History:
        - v2.2: Added upsert endpoint
        - v2.3: Made recommended endpoint for all data entry
    """
    # Check if entry exists
    existing = db.query(WorkoutEntry).filter(WorkoutEntry.date == workout.date).first()
    
    if existing:
        # Update existing entry
        for key, value in workout.dict().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new entry
        db_workout = WorkoutEntry(**workout.dict())
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        return db_workout


@router.get("/{entry_date}", response_model=WorkoutResponse)
def get_workout(entry_date: date, db: Session = Depends(get_db)):
    """
    Get Workout Entry by Date
    
    Purpose:
        Retrieves a specific workout entry for a given date.
        Used to check if workout was logged for a particular day.
    
    Path Parameters:
        entry_date: Date in YYYY-MM-DD format
        Example: /api/workouts/2026-01-17
    
    Request:
        - No body required
        - Date parsed from URL path
        - Automatic date validation by FastAPI
    
    Response (Success):
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
    
    Response (Not Found):
        {
            "detail": "Workout entry not found for 2026-01-17"
        }
    
    Status Codes:
        - 200 OK: Entry found
        - 404 Not Found: No entry for this date
        - 422 Unprocessable Entity: Invalid date format
    
    Use Cases:
        - Check if workout logged for specific date
        - Fetch entry for editing
        - Display workout details
        - Calendar date selection
        - Streak verification
    
    Performance:
        - Single database query
        - Indexed by primary key (fast)
        - Average response time: <50ms
    
    Example:
        curl -X GET http://localhost:8000/api/workouts/2026-01-17
    
    Frontend Integration:
        - Use when user selects date on calendar
        - Pre-fill edit form with existing data
        - Show workout details in modal
    """
    workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not workout:
        raise HTTPException(status_code=404, detail=f"Workout entry not found for {entry_date}")
    return workout


@router.put("/{entry_date}", response_model=WorkoutResponse)
def update_workout(entry_date: date, workout_update: WorkoutUpdate, db: Session = Depends(get_db)):
    """
    Update Existing Workout Entry
    
    Purpose:
        Updates an existing workout entry. All fields are optional,
        only provided fields will be updated.
    
    Path Parameters:
        entry_date: Date of entry to update (YYYY-MM-DD)
        Example: /api/workouts/2026-01-17
    
    Request Body (All Optional):
        {
            "workout_type": "Legs",        # Optional
            "workout_done": true,          # Optional
            "duration_minutes": 60,        # Optional
            "intensity": "Moderate",       # Optional
            "notes": "Updated notes"       # Optional
        }
    
    Behavior:
        - Only updates fields provided in request
        - Omitted fields remain unchanged
        - Date cannot be changed (it's the primary key)
        - updated_at timestamp automatically updated
        - created_at timestamp preserved
    
    Response (Success):
        {
            "date": "2026-01-17",
            "workout_type": "Legs",
            "workout_done": true,
            "duration_minutes": 60,
            "intensity": "Moderate",
            "notes": "Updated notes",
            "created_at": "2026-01-17T10:30:00",  # Preserved
            "updated_at": "2026-01-17T15:45:00"   # Updated
        }
    
    Response (Not Found):
        {
            "detail": "Workout entry not found for 2026-01-17"
        }
    
    Status Codes:
        - 200 OK: Entry updated successfully
        - 404 Not Found: No entry exists for this date
        - 422 Unprocessable Entity: Validation failed
    
    Use Cases:
        - Correct workout type
        - Update duration
        - Change intensity level
        - Add/edit notes
        - Fix data entry mistakes
    
    Recommendation:
        Use /upsert/ endpoint instead for:
        - Simpler logic (no 404 handling needed)
        - Create if doesn't exist
        - Idempotent operations
    
    Example:
        curl -X PUT http://localhost:8000/api/workouts/2026-01-17 \
          -H "Content-Type: application/json" \
          -d '{"duration_minutes":60,"intensity":"Moderate"}'
    """
    workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not workout:
        raise HTTPException(status_code=404, detail=f"Workout entry not found for {entry_date}")
    
    # Update only provided fields
    update_data = workout_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(workout, key, value)
    
    db.commit()
    db.refresh(workout)
    return workout


@router.delete("/{entry_date}", status_code=204)
def delete_workout(entry_date: date, db: Session = Depends(get_db)):
    """
    Delete Workout Entry
    
    Purpose:
        Permanently deletes a workout entry for a specific date.
        This operation cannot be undone.
    
    Path Parameters:
        entry_date: Date of entry to delete (YYYY-MM-DD)
        Example: /api/workouts/2026-01-17
    
    Request:
        - No body required
        - Date parsed from URL path
    
    Response (Success):
        - No content returned
        - HTTP 204 status indicates successful deletion
    
    Response (Not Found):
        {
            "detail": "Workout entry not found for 2026-01-17"
        }
    
    Status Codes:
        - 204 No Content: Entry deleted successfully
        - 404 Not Found: No entry exists for this date
        - 422 Unprocessable Entity: Invalid date format
    
    Side Effects:
        - Entry permanently removed from database
        - Affects dashboard statistics:
          * Current streak may decrease
          * Total workout days decreases
          * Workout percentage recalculated
          * Average duration may change
        - Operation cannot be undone
    
    Use Cases:
        - Remove duplicate entries
        - Delete incorrect entries
        - Clear test data
        - Reset tracking for specific date
    
    Caution:
        - No confirmation prompt at API level
        - Frontend should implement confirmation dialog
        - Consider soft delete for production use
        - Backup data before bulk deletions
    
    Example:
        curl -X DELETE http://localhost:8000/api/workouts/2026-01-17
    
    Best Practices:
        - Implement frontend confirmation
        - Log deletions for audit trail
        - Consider undo functionality
        - Validate user intent
    """
    workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not workout:
        raise HTTPException(status_code=404, detail=f"Workout entry not found for {entry_date}")
    
    db.delete(workout)
    db.commit()


@router.get("/history/", response_model=List[WorkoutResponse])
def get_workout_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get Workout History with Date Range Filtering
    
    Purpose:
        Retrieves list of all workout entries with optional date range
        filtering. Supports pagination and historical data analysis.
    
    Query Parameters:
        start_date: Filter from this date (inclusive)
                   Format: YYYY-MM-DD
                   Example: ?start_date=2026-01-01
        
        end_date: Filter until this date (inclusive)
                 Format: YYYY-MM-DD
                 Example: ?end_date=2026-01-31
    
    Filtering Logic:
        - No params: Returns all workout entries (entire history)
        - start_date only: Returns entries from start_date onwards
        - end_date only: Returns entries up to end_date
        - Both params: Returns entries within date range (inclusive)
    
    Response (Success):
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
    
    Response (Empty):
        []  # Empty array if no entries found
    
    Status Codes:
        - 200 OK: List retrieved successfully (may be empty)
        - 422 Unprocessable Entity: Invalid date format
    
    Use Cases:
        - Display workout calendar
        - Generate monthly reports
        - Analyze workout patterns
        - Export workout data
        - Track progress over time
    
    Performance:
        - Indexed query on date field
        - Efficient date range filtering
        - Order by date descending (most recent first)
        - Consider pagination for large datasets
    
    Examples:
        # Get all workouts
        curl -X GET http://localhost:8000/api/workouts/history/
        
        # Get January 2026 workouts
        curl -X GET "http://localhost:8000/api/workouts/history/?start_date=2026-01-01&end_date=2026-01-31"
        
        # Get workouts from start of year
        curl -X GET "http://localhost:8000/api/workouts/history/?start_date=2026-01-01"
        
        # Get workouts up to today
        curl -X GET "http://localhost:8000/api/workouts/history/?end_date=2026-01-17"
    
    Pagination Considerations:
        - Current: Returns all matching records
        - Future: Add limit/offset parameters for large datasets
        - Recommended limit: 100 entries per page
    
    Frontend Integration:
        - Use for calendar view rendering
        - Filter by current month/week
        - Populate workout history list
        - Generate statistics charts
    """
    query = db.query(WorkoutEntry)
    
    if start_date:
        query = query.filter(WorkoutEntry.date >= start_date)
    if end_date:
        query = query.filter(WorkoutEntry.date <= end_date)
    
    workouts = query.order_by(WorkoutEntry.date.desc()).all()
    return workouts
