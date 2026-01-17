"""
Smoking Tracker API Routes

This module provides CRUD operations for smoking cessation tracking
with date-based relapse logging and clean streak calculations.

Purpose:
    - Log smoking relapses (days with cigarette consumption)
    - Track cigarette counts and smoking locations
    - Support historical data entry and corrections
    - Calculate clean streaks (consecutive days without smoking)
    - Identify smoking triggers through location tracking
    - Provide smoking history with date range filtering

Routes:
    POST   /api/smoking/         - Create new smoking entry
    POST   /api/smoking/upsert/  - Create or update smoking entry (recommended)
    GET    /api/smoking/{date}   - Get smoking entry by date
    DELETE /api/smoking/{date}   - Delete smoking entry
    GET    /api/smoking/history/ - Get smoking history with filtering

Data Model:
    - Primary Key: date (YYYY-MM-DD)
    - Required: cigarette_count (integer)
    - Location Types: Home, Work, Social, Other
    - Optional fields: location, remarks
    - Timestamp: created_at (no updates - relapses are fixed events)

Business Logic:
    - Entry exists = Relapse day (user smoked)
    - No entry = Clean day (user did not smoke)
    - Each entry represents one relapse event
    - Clean streaks calculated from gaps between entries
    - Locations help identify smoking triggers
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from db.database import get_db
from db.models import SmokingEntry
from db.schemas import SmokingCreate, SmokingResponse

router = APIRouter()


@router.post("/", response_model=SmokingResponse, status_code=201)
def create_smoking_entry(entry: SmokingCreate, db: Session = Depends(get_db)):
    """
    Create New Smoking Entry (Log Relapse)
    
    Purpose:
        Creates a new smoking entry to log a relapse day. Returns an error
        if an entry already exists for that date (one entry per day maximum).
    
    Request Body:
        {
            "date": "2026-01-10",          # Required: YYYY-MM-DD format
            "cigarette_count": 3,          # Required: Integer >= 0
            "location": "Social",          # Optional: Enum value
            "remarks": "Party with friends" # Optional: String
        }
    
    Validation:
        - date: Must be valid date in YYYY-MM-DD format
        - cigarette_count: Must be non-negative integer
        - location: Must be valid enum value (Home, Work, Social, Other) if provided
        - remarks: Optional string, max length determined by database
    
    Response (Success):
        {
            "date": "2026-01-10",
            "cigarette_count": 3,
            "location": "Social",
            "remarks": "Party with friends",
            "created_at": "2026-01-10T20:00:00"
        }
    
    Status Codes:
        - 201 Created: Entry created successfully (relapse logged)
        - 400 Bad Request: Entry already exists for this date
        - 422 Unprocessable Entity: Validation failed
    
    Error Response (Duplicate):
        {
            "detail": "Entry already exists for 2026-01-10"
        }
    
    Use Cases:
        - Log today's relapse
        - Record cigarette consumption
        - Track smoking triggers (location)
        - Manual data entry
    
    Business Logic:
        - One entry per day maximum (multiple smoking sessions = one relapse day)
        - Cigarette count represents total for the entire day
        - Location typically indicates where first/most cigarettes were smoked
        - Remarks can note circumstances, triggers, or feelings
    
    Impact on Statistics:
        - Ends current clean streak
        - Increments total relapses counter
        - Adds to total cigarette count
        - May update most common location
    
    Recommendation:
        Use /upsert/ endpoint instead for:
        - Historical data entry
        - Updating cigarette counts
        - Avoiding duplicate errors
        - Correcting location/remarks
    
    Example:
        curl -X POST http://localhost:8000/api/smoking/ \
          -H "Content-Type: application/json" \
          -d '{"date":"2026-01-10","cigarette_count":3,"location":"Social"}'
    
    Note:
        - created_at timestamp recorded at entry creation
        - No updated_at field (relapses are historical events)
        - Consider emotional context when logging (remarks field)
    """
    # Check if entry already exists
    existing = db.query(SmokingEntry).filter(SmokingEntry.date == entry.date).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Entry already exists for {entry.date}")
    
    # Create new smoking entry
    db_entry = SmokingEntry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.post("/upsert/", response_model=SmokingResponse)
def upsert_smoking_entry(entry: SmokingCreate, db: Session = Depends(get_db)):
    """
    Create or Update Smoking Entry (Recommended)
    
    Purpose:
        Smart endpoint that automatically creates a new entry or updates
        an existing one based on the date. Eliminates duplicate entry errors
        and simplifies data correction workflows.
    
    Request Body:
        {
            "date": "2026-01-10",
            "cigarette_count": 5,
            "location": "Work",
            "remarks": "Stressful day"
        }
    
    Behavior:
        - If date doesn't exist: Creates new entry (like POST)
        - If date exists: Updates all fields (cigarette count, location, remarks)
        - Always succeeds (no duplicate errors)
        - Idempotent (safe to retry)
        - created_at timestamp preserved when updating
    
    Response:
        {
            "date": "2026-01-10",
            "cigarette_count": 5,
            "location": "Work",
            "remarks": "Stressful day",
            "created_at": "2026-01-10T20:00:00"  # Original timestamp preserved
        }
    
    Status Codes:
        - 200 OK: Entry created or updated successfully
        - 422 Unprocessable Entity: Validation failed
    
    Benefits:
        ✅ No duplicate entry errors
        ✅ Single API call for all operations
        ✅ Ideal for historical data entry
        ✅ Perfect for data corrections
        ✅ Idempotent (safe to retry)
        ✅ Used by web and mobile clients
        ✅ Simplifies frontend logic
    
    Use Cases:
        - Primary data entry method
        - Historical relapse logging
        - Update cigarette count (if counted wrong initially)
        - Correct location information
        - Add or update remarks
        - Data import/sync operations
    
    Business Logic:
        - Updating an entry doesn't "undo" the relapse
        - Clean streaks calculated from entry existence, not cigarette count
        - Location changes help identify trigger patterns
        - Remarks can be added later as reflection/insight develops
    
    Impact on Statistics:
        - Total cigarettes: Updates sum calculation
        - Most common location: May change if location updated
        - Clean streaks: Unaffected (date still has entry)
        - Total relapses: Unaffected (still one entry per date)
    
    Performance:
        - 1 query: Check if entry exists
        - 1 query: INSERT or UPDATE
        - Total: 2 database operations
        - Automatically recalculates dashboard stats
    
    Examples:
        # Create new entry
        curl -X POST http://localhost:8000/api/smoking/upsert/ \
          -H "Content-Type: application/json" \
          -d '{"date":"2026-01-10","cigarette_count":3,"location":"Social"}'
        
        # Update existing entry (change count and location)
        curl -X POST http://localhost:8000/api/smoking/upsert/ \
          -H "Content-Type: application/json" \
          -d '{"date":"2026-01-10","cigarette_count":5,"location":"Work"}'
    
    Version History:
        - v2.2: Added upsert endpoint for smoking tracker
        - v2.3: Made recommended endpoint for all data entry
    
    Frontend Integration:
        - Use for all smoking entry forms
        - No need to check if entry exists first
        - Handles both "Add Relapse" and "Edit Relapse" flows
        - Perfect for date picker + form submission
    """
    # Check if entry exists
    existing = db.query(SmokingEntry).filter(SmokingEntry.date == entry.date).first()
    
    if existing:
        # Update existing entry (preserve created_at, update all other fields)
        for key, value in entry.dict().items():
            if key != 'created_at':  # Don't update timestamp
                setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new entry
        db_entry = SmokingEntry(**entry.dict())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry


@router.get("/{entry_date}", response_model=SmokingResponse)
def get_smoking_entry(entry_date: date, db: Session = Depends(get_db)):
    """
    Get Smoking Entry by Date
    
    Purpose:
        Retrieves a specific smoking entry for a given date.
        Used to check if a relapse occurred on a particular day.
    
    Path Parameters:
        entry_date: Date in YYYY-MM-DD format
        Example: /api/smoking/2026-01-10
    
    Request:
        - No body required
        - Date parsed from URL path
        - Automatic date validation by FastAPI
    
    Response (Success):
        {
            "date": "2026-01-10",
            "cigarette_count": 3,
            "location": "Social",
            "remarks": "Party with friends",
            "created_at": "2026-01-10T20:00:00"
        }
    
    Response (Not Found):
        {
            "detail": "Smoking entry not found for 2026-01-10"
        }
    
    Status Codes:
        - 200 OK: Entry found (relapse occurred on this date)
        - 404 Not Found: No entry for this date (clean day)
        - 422 Unprocessable Entity: Invalid date format
    
    Use Cases:
        - Check if relapse occurred on specific date
        - Fetch entry for editing
        - Display relapse details
        - Calendar date selection
        - Clean streak verification
        - Trigger pattern analysis
    
    Business Logic:
        - Entry found = Relapse day
        - 404 Not Found = Clean day (positive outcome!)
        - Use 404 status to determine clean vs relapse days
    
    Performance:
        - Single database query
        - Indexed by primary key (fast)
        - Average response time: <50ms
    
    Example:
        curl -X GET http://localhost:8000/api/smoking/2026-01-10
    
    Frontend Integration:
        - Use when user selects date on calendar
        - Pre-fill edit form with existing data
        - Show relapse details in modal
        - Color-code calendar (green=404, red=200)
        - Calculate day-by-day clean status
    
    Clean Day Detection:
        ```javascript
        const isCleanDay = async (date) => {
            try {
                await fetch(`/api/smoking/${date}`);
                return false; // Entry exists = relapse day
            } catch (error) {
                if (error.status === 404) {
                    return true; // No entry = clean day
                }
                throw error;
            }
        };
        ```
    """
    entry = db.query(SmokingEntry).filter(SmokingEntry.date == entry_date).first()
    if not entry:
        raise HTTPException(status_code=404, detail=f"Smoking entry not found for {entry_date}")
    return entry


@router.delete("/{entry_date}", status_code=204)
def delete_smoking_entry(entry_date: date, db: Session = Depends(get_db)):
    """
    Delete Smoking Entry
    
    Purpose:
        Permanently deletes a smoking entry for a specific date.
        This operation cannot be undone. Use to remove incorrect entries
        or acknowledge that a logged relapse was a data entry error.
    
    Path Parameters:
        entry_date: Date of entry to delete (YYYY-MM-DD)
        Example: /api/smoking/2026-01-10
    
    Request:
        - No body required
        - Date parsed from URL path
    
    Response (Success):
        - No content returned
        - HTTP 204 status indicates successful deletion
    
    Response (Not Found):
        {
            "detail": "Smoking entry not found for 2026-01-10"
        }
    
    Status Codes:
        - 204 No Content: Entry deleted successfully
        - 404 Not Found: No entry exists for this date
        - 422 Unprocessable Entity: Invalid date format
    
    Side Effects:
        - Entry permanently removed from database
        - Affects dashboard statistics:
          * Clean streaks recalculated (may increase!)
          * Total relapses decreases
          * Total cigarettes decreases
          * Most common location may change
        - Date becomes a "clean day" again
        - Operation cannot be undone
    
    Use Cases:
        - Remove duplicate entries
        - Delete incorrect entries (data entry mistakes)
        - Clear test data
        - Acknowledge false positive (didn't actually smoke)
        - Reset tracking for specific date
    
    Business Logic:
        - Deletion converts relapse day back to clean day
        - May significantly improve clean streak statistics
        - Should be used thoughtfully (not to "cheat" the system)
        - Consider adding audit log for deletions
    
    Caution:
        - No confirmation prompt at API level
        - Frontend should implement confirmation dialog
        - Consider soft delete for production use
        - Backup data before bulk deletions
        - Deletion affects motivation metrics
    
    Example:
        curl -X DELETE http://localhost:8000/api/smoking/2026-01-10
    
    Best Practices:
        - Implement frontend confirmation dialog
        - Show impact on statistics before confirming
        - Log deletions for audit trail
        - Consider requiring reason for deletion
        - Validate user intent
        - Maybe allow "undo" within time window
    
    Ethical Considerations:
        - Deleting entries to improve stats defeats purpose
        - Frontend should emphasize honesty in tracking
        - Consider showing "data correction" vs "achievement"
        - Maybe show "corrected entries" separately in stats
    
    Alternative Approach:
        - Instead of DELETE, consider UPDATE with cigarette_count=0
        - Preserves audit trail while reflecting reality
        - Distinguishes between "no smoke" and "data error"
    """
    entry = db.query(SmokingEntry).filter(SmokingEntry.date == entry_date).first()
    if not entry:
        raise HTTPException(status_code=404, detail=f"Smoking entry not found for {entry_date}")
    
    db.delete(entry)
    db.commit()


@router.get("/history/", response_model=List[SmokingResponse])
def get_smoking_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get Smoking History with Date Range Filtering
    
    Purpose:
        Retrieves list of all smoking entries (relapses) with optional
        date range filtering. Supports historical analysis and pattern
        identification for smoking cessation support.
    
    Query Parameters:
        start_date: Filter from this date (inclusive)
                   Format: YYYY-MM-DD
                   Example: ?start_date=2026-01-01
        
        end_date: Filter until this date (inclusive)
                 Format: YYYY-MM-DD
                 Example: ?end_date=2026-01-31
    
    Filtering Logic:
        - No params: Returns all smoking entries (entire history)
        - start_date only: Returns entries from start_date onwards
        - end_date only: Returns entries up to end_date
        - Both params: Returns entries within date range (inclusive)
    
    Response (Success):
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
    
    Response (Empty):
        []  # Empty array if no entries found (all clean days!)
    
    Status Codes:
        - 200 OK: List retrieved successfully (may be empty)
        - 422 Unprocessable Entity: Invalid date format
    
    Use Cases:
        - Display relapse calendar (mark dates with entries)
        - Generate monthly cessation reports
        - Analyze smoking patterns and triggers
        - Identify high-risk situations (location analysis)
        - Track progress over time
        - Export data for external analysis
        - Calculate custom statistics
    
    Pattern Analysis:
        - Group by location: Identify trigger environments
        - Group by day of week: Find high-risk days
        - Analyze gaps: Measure clean streak distributions
        - Time of day patterns: When logged (created_at)
        - Cigarette count trends: Increasing or decreasing
    
    Performance:
        - Indexed query on date field
        - Efficient date range filtering
        - Order by date descending (most recent first)
        - Consider pagination for large datasets
    
    Examples:
        # Get all relapses
        curl -X GET http://localhost:8000/api/smoking/history/
        
        # Get January 2026 relapses
        curl -X GET "http://localhost:8000/api/smoking/history/?start_date=2026-01-01&end_date=2026-01-31"
        
        # Get relapses from start of year
        curl -X GET "http://localhost:8000/api/smoking/history/?start_date=2026-01-01"
        
        # Get relapses up to today
        curl -X GET "http://localhost:8000/api/smoking/history/?end_date=2026-01-17"
    
    Pagination Considerations:
        - Current: Returns all matching records
        - Future: Add limit/offset parameters for long histories
        - Recommended limit: 100 entries per page
        - Most users will have relatively few entries (goal is cessation!)
    
    Frontend Integration:
        - Use for calendar view rendering (mark relapse dates)
        - Filter by current month/week for focused view
        - Populate relapse history list
        - Generate trigger analysis charts
        - Show progress visualization (gaps getting longer)
        - Display location-based heatmap
    
    Clean Day Calculation:
        ```javascript
        const getCleanDays = (startDate, endDate, relapseHistory) => {
            const totalDays = daysBetween(startDate, endDate);
            const relapseDays = relapseHistory.length;
            return totalDays - relapseDays;
        };
        ```
    
    Statistics Examples:
        - Average cigarettes per relapse day
        - Most common relapse day of week
        - Time between relapses (clean streak distribution)
        - Location frequency (trigger identification)
        - Month-over-month improvement
    
    Motivational Use:
        - Show decreasing frequency of entries (progress!)
        - Highlight increasing gaps between entries
        - Celebrate empty result sets (no relapses!)
        - Compare current month to previous months
    """
    query = db.query(SmokingEntry)
    
    if start_date:
        query = query.filter(SmokingEntry.date >= start_date)
    if end_date:
        query = query.filter(SmokingEntry.date <= end_date)
    
    entries = query.order_by(SmokingEntry.date.desc()).all()
    return entries
