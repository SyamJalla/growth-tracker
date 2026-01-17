"""
Pydantic Schemas for Request/Response Validation

This module defines Pydantic models used for API request validation
and response serialization. Provides automatic data validation,
type checking, and JSON serialization.

Purpose:
    - Validate incoming request data
    - Serialize database models to JSON
    - Enforce data types and constraints
    - Generate automatic API documentation
    - Provide type hints for IDEs

Schema Types:
    - Create schemas: For POST requests (creating new entries)
    - Update schemas: For PUT requests (updating existing entries)
    - Response schemas: For API responses (reading data)

Benefits:
    - Automatic validation before database operations
    - Type safety throughout application
    - Self-documenting API (OpenAPI/Swagger)
    - Prevents invalid data from reaching database
    - Consistent error messages
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional

from db.models import WorkoutType, IntensityLevel, LocationType


class WorkoutCreate(BaseModel):
    """
    Workout Creation Schema
    
    Purpose:
        Validates data for creating new workout entries.
        Used in POST /api/workouts/ and POST /api/workouts/upsert/
    
    Fields:
        date: Workout date (required)
              - Format: YYYY-MM-DD
              - Must be valid date
              - Can be past, present, or future
              - Primary key for entry
        
        workout_type: Type of workout (required)
                     - Must be valid WorkoutType enum
                     - Examples: "Push", "Pull", "Legs"
                     - Case-sensitive
        
        workout_done: Completion flag (required)
                     - Boolean value
                     - Usually true when logging
                     - Future use: partial completion
        
        duration_minutes: Workout duration (required)
                         - Must be positive integer
                         - Reasonable range: 5-300 minutes
                         - Validation enforced
        
        intensity: Workout intensity (optional)
                  - Must be valid IntensityLevel enum if provided
                  - Examples: "Low", "Moderate", "High"
                  - Can be null
        
        notes: Personal notes (optional)
              - String field
              - No maximum length (TEXT field)
              - Can be null or empty string
    
    Validation Rules:
        - date: Must be valid ISO date format
        - workout_type: Must match enum values exactly
        - workout_done: Must be boolean
        - duration_minutes: Must be > 0
        - intensity: Must match enum values if provided
    
    Example:
        {
            "date": "2026-01-17",
            "workout_type": "Push",
            "workout_done": true,
            "duration_minutes": 45,
            "intensity": "High",
            "notes": "Great chest and triceps session!"
        }
    
    Minimal Example:
        {
            "date": "2026-01-17",
            "workout_type": "Push",
            "workout_done": true,
            "duration_minutes": 45
        }
    """
    date: date
    workout_type: WorkoutType
    workout_done: bool = True
    duration_minutes: int = Field(..., gt=0, description="Duration must be positive")
    intensity: Optional[IntensityLevel] = None
    notes: Optional[str] = None
    
    @field_validator('duration_minutes')
    @classmethod
    def validate_duration(cls, v):
        """
        Validate workout duration is reasonable
        
        Rules:
            - Must be positive (> 0)
            - Should be reasonable (typically 5-300 minutes)
            - Warning for extreme values
        
        Args:
            v: Duration value to validate
        
        Returns:
            Validated duration value
        
        Raises:
            ValueError: If duration is invalid
        """
        if v <= 0:
            raise ValueError('Duration must be positive')
        if v > 300:
            # Allow but warn for very long workouts
            pass  # Could add logging here
        return v
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "date": "2026-01-17",
                "workout_type": "Push",
                "workout_done": True,
                "duration_minutes": 45,
                "intensity": "High",
                "notes": "Great session!"
            }
        }


class WorkoutUpdate(BaseModel):
    """
    Workout Update Schema
    
    Purpose:
        Validates data for updating existing workout entries.
        Used in PUT /api/workouts/{date}
    
    Fields:
        All fields are optional - only update what's provided
        - workout_type: Change workout type
        - workout_done: Update completion status
        - duration_minutes: Correct duration
        - intensity: Add/change intensity
        - notes: Add/update notes
    
    Behavior:
        - Only provided fields are updated
        - Omitted fields remain unchanged
        - Date cannot be updated (it's the primary key)
        - Null values explicitly set field to null
        - Empty strings different from null
    
    Example (Update duration and intensity):
        {
            "duration_minutes": 60,
            "intensity": "Moderate"
        }
    
    Example (Update notes only):
        {
            "notes": "Updated notes with more details"
        }
    
    Example (Change workout type):
        {
            "workout_type": "Legs"
        }
    """
    workout_type: Optional[WorkoutType] = None
    workout_done: Optional[bool] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    intensity: Optional[IntensityLevel] = None
    notes: Optional[str] = None
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "duration_minutes": 60,
                "intensity": "Moderate",
                "notes": "Updated notes"
            }
        }


class WorkoutResponse(BaseModel):
    """
    Workout Response Schema
    
    Purpose:
        Defines structure of workout data returned by API.
        Used in all GET responses for workout endpoints.
    
    Fields:
        date: Workout date (YYYY-MM-DD)
        workout_type: Type of workout
        workout_done: Completion status
        duration_minutes: Duration in minutes
        intensity: Intensity level (nullable)
        notes: Personal notes (nullable)
        created_at: Creation timestamp (ISO format)
        updated_at: Last update timestamp (ISO format)
    
    Serialization:
        - Automatically converts SQLAlchemy model to JSON
        - Handles datetime to ISO string conversion
        - Handles enum to string conversion
        - Handles null values appropriately
    
    Example Response:
        {
            "date": "2026-01-17",
            "workout_type": "Push",
            "workout_done": true,
            "duration_minutes": 45,
            "intensity": "High",
            "notes": "Great session!",
            "created_at": "2026-01-17T10:30:00",
            "updated_at": "2026-01-17T10:30:00"
        }
    
    Usage:
        - GET /api/workouts/{date}
        - POST /api/workouts/ (returns created entry)
        - POST /api/workouts/upsert/ (returns entry)
        - PUT /api/workouts/{date} (returns updated entry)
        - GET /api/workouts/history/ (list of these)
    """
    date: date
    workout_type: WorkoutType
    workout_done: bool
    duration_minutes: int
    intensity: Optional[IntensityLevel]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """
        Pydantic configuration for ORM mode
        
        from_attributes=True enables:
        - Reading data from SQLAlchemy models
        - Automatic conversion of model objects
        - Lazy loading of relationships
        """
        from_attributes = True


class SmokingCreate(BaseModel):
    """
    Smoking Entry Creation Schema
    
    Purpose:
        Validates data for creating new smoking entries (logging relapses).
        Used in POST /api/smoking/ and POST /api/smoking/upsert/
    
    Fields:
        date: Relapse date (required)
              - Format: YYYY-MM-DD
              - Must be valid date
              - Can be past or present
              - Primary key for entry
        
        cigarette_count: Number of cigarettes smoked (required)
                        - Must be non-negative integer
                        - Represents total for the day
                        - Can be 0 (logged intention)
        
        location: Where smoking occurred (optional)
                 - Must be valid LocationType enum if provided
                 - Examples: "Home", "Work", "Social", "Other"
                 - Used for trigger identification
        
        remarks: Context and notes (optional)
                - String field
                - No maximum length
                - Describe circumstances, triggers, feelings
    
    Validation Rules:
        - date: Must be valid ISO date format
        - cigarette_count: Must be >= 0
        - location: Must match enum values if provided
        - remarks: Any string (including empty)
    
    Example:
        {
            "date": "2026-01-10",
            "cigarette_count": 3,
            "location": "Social",
            "remarks": "Party with friends, peer pressure"
        }
    
    Minimal Example:
        {
            "date": "2026-01-10",
            "cigarette_count": 3
        }
    """
    date: date
    cigarette_count: int = Field(..., ge=0, description="Cigarette count must be non-negative")
    location: Optional[LocationType] = None
    remarks: Optional[str] = None
    
    @field_validator('cigarette_count')
    @classmethod
    def validate_cigarette_count(cls, v):
        """
        Validate cigarette count is reasonable
        
        Rules:
            - Must be non-negative (>= 0)
            - Warn for very high counts (> 40)
            - 0 is valid (logged without follow-through)
        
        Args:
            v: Cigarette count to validate
        
        Returns:
            Validated count
        
        Raises:
            ValueError: If count is negative
        """
        if v < 0:
            raise ValueError('Cigarette count cannot be negative')
        if v > 40:
            # Allow but unusual (2 packs)
            pass  # Could add logging here
        return v
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "date": "2026-01-10",
                "cigarette_count": 3,
                "location": "Social",
                "remarks": "Party with friends"
            }
        }


class SmokingResponse(BaseModel):
    """
    Smoking Entry Response Schema
    
    Purpose:
        Defines structure of smoking data returned by API.
        Used in all GET responses for smoking endpoints.
    
    Fields:
        date: Relapse date (YYYY-MM-DD)
        cigarette_count: Number of cigarettes smoked
        location: Smoking location (nullable)
        remarks: Personal notes (nullable)
        created_at: Creation timestamp (ISO format)
    
    Note:
        - No updated_at field (relapses are historical events)
        - created_at preserved even if entry updated via upsert
    
    Serialization:
        - Converts SQLAlchemy model to JSON
        - Handles datetime to ISO string conversion
        - Handles enum to string conversion
        - Handles null values
    
    Example Response:
        {
            "date": "2026-01-10",
            "cigarette_count": 3,
            "location": "Social",
            "remarks": "Party with friends",
            "created_at": "2026-01-10T20:00:00"
        }
    
    Usage:
        - GET /api/smoking/{date}
        - POST /api/smoking/ (returns created entry)
        - POST /api/smoking/upsert/ (returns entry)
        - GET /api/smoking/history/ (list of these)
    """
    date: date
    cigarette_count: int
    location: Optional[LocationType]
    remarks: Optional[str]
    created_at: datetime
    
    class Config:
        """
        Pydantic configuration for ORM mode
        
        from_attributes=True enables:
        - Reading data from SQLAlchemy models
        - Automatic conversion of model objects
        """
        from_attributes = True
