"""
SQLAlchemy Database Models

This module defines all database table structures using SQLAlchemy ORM.
Each class represents a table with columns, types, constraints, and relationships.

Purpose:
    - Define database schema in Python code
    - Provide ORM interface for database operations
    - Enforce data types and constraints at application level
    - Support automatic table creation and migrations
    - Enable type-safe database queries

Tables:
    - health_check: System health monitoring
    - workout_entries: Daily workout logging
    - smoking_entries: Smoking cessation tracking

Design Principles:
    - Date-based primary keys for daily tracking
    - Enum fields for controlled vocabularies
    - Nullable fields for optional data
    - Automatic timestamp management
    - No foreign keys (independent tracking systems)
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from db.database import Base


class WorkoutType(str, enum.Enum):
    """
    Workout Type Enumeration
    
    Purpose:
        Defines valid workout categories for classification and
        filtering. Each type represents a different training split
        or exercise modality.
    
    Values:
        Push: Push exercises (chest, shoulders, triceps)
              Example: Bench press, overhead press, dips
        
        Pull: Pull exercises (back, biceps)
              Example: Rows, pull-ups, curls
        
        Legs: Lower body exercises
              Example: Squats, lunges, leg press
        
        Upper: Upper body mixed (push + pull)
               Example: Full upper body workout
        
        Lower: Lower body focused
               Example: Legs and glutes emphasis
        
        Cardio: Cardiovascular exercises
                Example: Running, cycling, swimming
        
        Others: Any other workout type
                Example: Sports, yoga, flexibility
    
    Usage:
        - Workout classification and organization
        - Statistics by workout type
        - Most common workout type calculation
        - Training program tracking
        - Progress analysis by category
    
    Frontend Integration:
        - Dropdown/picker options
        - Filter workouts by type
        - Color coding in calendar
        - Chart/graph categorization
    
    Version History:
        - v2.3: Synchronized with frontend enum values
        - v2.0: Initial workout type definitions
    """
    PUSH = "Push"
    PULL = "Pull"
    LEGS = "Legs"
    UPPER = "Upper"
    LOWER = "Lower"
    CARDIO = "Cardio"
    OTHERS = "Others"


class IntensityLevel(str, enum.Enum):
    """
    Intensity Level Enumeration
    
    Purpose:
        Defines workout intensity levels for effort tracking
        and progress monitoring over time.
    
    Values:
        Low: Light effort, easy workout
             Example: Recovery day, light cardio
             RPE: 1-3 (Rate of Perceived Exertion)
        
        Moderate: Medium effort, comfortable pace
                  Example: Standard training session
                  RPE: 4-6
        
        High: Maximum effort, challenging workout
              Example: PR attempts, HIIT sessions
              RPE: 7-10
    
    Usage:
        - Track workout difficulty
        - Monitor training load
        - Prevent overtraining
        - Analyze intensity patterns
        - Adjust training programs
    
    Training Guidelines:
        - Low: Active recovery, skill work
        - Moderate: Base building, technique focus
        - High: Strength/power development, competitions
    
    Version History:
        - v2.3: Changed "Medium" to "Moderate" for consistency
        - v2.0: Initial intensity level definitions
    """
    LOW = "Low"
    MODERATE = "Moderate"  # v2.3: Changed from "Medium"
    HIGH = "High"


class LocationType(str, enum.Enum):
    """
    Location Type Enumeration (Smoking Tracker)
    
    Purpose:
        Categorizes smoking locations to identify triggers
        and high-risk situations for cessation support.
    
    Values:
        Home: At residential location
              Risk factor: Access to cigarettes, habits, stress
        
        Work: At workplace or office
              Risk factor: Work stress, colleague influence
        
        Social: Social gatherings, parties, bars
                Risk factor: Peer pressure, alcohol, celebrations
        
        Other: Any other location
               Example: Car, outdoors, traveling
    
    Usage:
        - Identify smoking triggers
        - Track most common smoking locations
        - Develop location-specific coping strategies
        - Analyze risk patterns
        - Support behavior modification
    
    Trigger Analysis:
        - Helps identify environmental cues
        - Reveals situational patterns
        - Guides intervention strategies
        - Supports relapse prevention
    
    Frontend Integration:
        - Location picker when logging relapse
        - Heatmap of smoking locations
        - Trigger warning system
        - Location-based statistics
    """
    HOME = "Home"
    WORK = "Work"
    SOCIAL = "Social"
    OTHER = "Other"


class HealthCheck(Base):
    """
    Health Check Table
    
    Purpose:
        Stores system health messages for database connectivity
        verification and monitoring. Simple table for testing
        database operations without affecting tracking data.
    
    Columns:
        id: Auto-incrementing primary key
        message: Health status message
        created_at: Timestamp of record creation
    
    Use Cases:
        - Database connectivity tests
        - Health check endpoints
        - Connection pool verification
        - Monitoring system integration
    
    Example Records:
        (1, "Database is healthy", "2026-01-01 00:00:00")
        (2, "Connection verified", "2026-01-01 12:00:00")
    """
    __tablename__ = "health_check"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorkoutEntry(Base):
    """
    Workout Entries Table
    
    Purpose:
        Stores daily workout tracking data including type, duration,
        intensity, and personal notes. Primary table for fitness
        progress monitoring and streak calculations.
    
    Columns:
        date: Primary key (YYYY-MM-DD)
              - One entry per day maximum
              - Enables date-based queries and streak calculations
              - Indexed for fast lookups
        
        workout_type: Type of workout performed
                     - Required field (no null)
                     - Enum-constrained values
                     - Used for statistics and filtering
        
        workout_done: Boolean flag indicating completion
                     - Required field
                     - Always true when entry exists
                     - Future use: partial completion tracking
        
        duration_minutes: Workout duration in minutes
                         - Required field
                         - Must be positive integer
                         - Used for average duration calculation
        
        intensity: Workout intensity level
                  - Optional field (nullable)
                  - Enum-constrained values
                  - Used for training load monitoring
        
        notes: Personal notes and observations
              - Optional field (nullable)
              - Text field for unlimited length
              - User's subjective feedback
        
        created_at: Record creation timestamp
                   - Automatically set on INSERT
                   - Never updated
                   - UTC timezone
        
        updated_at: Record update timestamp
                   - Automatically set on INSERT
                   - Updated on every UPDATE
                   - UTC timezone
    
    Indexes:
        - Primary key index on date (automatic)
        - Consider adding index on created_at for recent queries
    
    Constraints:
        - PRIMARY KEY (date)
        - NOT NULL (date, workout_type, workout_done, duration_minutes)
        - CHECK (duration_minutes > 0) - enforced at application level
    
    Relationships:
        - None (independent tracking system)
    
    Business Logic:
        - Entry exists = workout completed that day
        - No entry = rest day or no data
        - One entry per day maximum (upsert pattern)
        - Can log historical workouts (past dates)
    
    Statistics Calculations:
        - Current streak: Consecutive days with entries
        - Longest streak: Maximum consecutive days
        - Total workout days: Count of all entries
        - Average duration: Mean of duration_minutes
        - Most common type: Mode of workout_type
    
    Data Validation:
        - Date: Valid date format, not future date
        - Workout type: Must be valid enum value
        - Duration: Must be positive integer
        - Intensity: Must be valid enum value if provided
    
    Usage Example:
        ```python
        workout = WorkoutEntry(
            date=date(2026, 1, 17),
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            duration_minutes=45,
            intensity=IntensityLevel.HIGH,
            notes="Great chest and triceps session!"
        )
        ```
    
    Query Examples:
        ```python
        # Get workout by date
        workout = session.query(WorkoutEntry).filter_by(date='2026-01-17').first()
        
        # Get all Push workouts
        push_workouts = session.query(WorkoutEntry)\
            .filter_by(workout_type=WorkoutType.PUSH)\
            .all()
        
        # Get workouts in date range
        workouts = session.query(WorkoutEntry)\
            .filter(WorkoutEntry.date.between('2026-01-01', '2026-01-31'))\
            .order_by(WorkoutEntry.date.desc())\
            .all()
        ```
    """
    __tablename__ = "workout_entries"
    
    date = Column(Date, primary_key=True, index=True)
    workout_type = Column(SQLEnum(WorkoutType), nullable=False)
    workout_done = Column(Boolean, nullable=False, default=True)
    duration_minutes = Column(Integer, nullable=False)
    intensity = Column(SQLEnum(IntensityLevel), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class SmokingEntry(Base):
    """
    Smoking Entries Table
    
    Purpose:
        Stores smoking relapse data for cessation tracking. Each entry
        represents a day when smoking occurred. Absence of entry indicates
        a clean day. Used for clean streak calculations and trigger analysis.
    
    Columns:
        date: Primary key (YYYY-MM-DD)
              - One entry per day maximum
              - Entry exists = relapse day
              - No entry = clean day
              - Indexed for fast lookups
        
        cigarette_count: Number of cigarettes smoked
                        - Required field (must be >= 0)
                        - Aggregated for total consumption statistics
                        - Can be 0 (logged intention without follow-through)
        
        location: Where smoking occurred
                 - Optional field (nullable)
                 - Enum-constrained values
                 - Used for trigger identification
                 - Helps pattern recognition
        
        remarks: Personal notes about circumstances
                - Optional field (nullable)
                - Text field for unlimited length
                - Context, feelings, triggers
                - Reflection and insight
        
        created_at: Record creation timestamp
                   - Automatically set on INSERT
                   - Never updated (relapses are historical events)
                   - UTC timezone
    
    Indexes:
        - Primary key index on date (automatic)
        - Consider adding index on location for trigger analysis
    
    Constraints:
        - PRIMARY KEY (date)
        - NOT NULL (date, cigarette_count)
        - CHECK (cigarette_count >= 0) - enforced at application level
    
    Relationships:
        - None (independent tracking system)
    
    Business Logic:
        - Entry exists = Relapse day (user smoked)
        - No entry = Clean day (user did not smoke)
        - One entry per day maximum (upsert pattern)
        - Can log historical relapses (past dates)
        - Cigarette count can be updated if misremembered
    
    Statistics Calculations:
        - Current clean streak: Days since last entry
        - Longest clean streak: Maximum gap between entries
        - Total relapses: Count of all entries
        - Total cigarettes: Sum of cigarette_count
        - Most common location: Mode of location field
    
    Clean Streak Logic:
        - Start from today, count backwards
        - Stop at first entry (relapse)
        - Gaps between entries = clean periods
        - No entries ever = clean since tracking began
    
    Data Validation:
        - Date: Valid date format, not future date
        - Cigarette count: Non-negative integer
        - Location: Must be valid enum value if provided
    
    Usage Example:
        ```python
        relapse = SmokingEntry(
            date=date(2026, 1, 10),
            cigarette_count=3,
            location=LocationType.SOCIAL,
            remarks="Party with friends, peer pressure"
        )
        ```
    
    Query Examples:
        ```python
        # Get relapse by date
        relapse = session.query(SmokingEntry).filter_by(date='2026-01-10').first()
        
        # Get all Social location relapses
        social_relapses = session.query(SmokingEntry)\
            .filter_by(location=LocationType.SOCIAL)\
            .all()
        
        # Get relapses in date range
        relapses = session.query(SmokingEntry)\
            .filter(SmokingEntry.date.between('2026-01-01', '2026-01-31'))\
            .order_by(SmokingEntry.date.desc())\
            .all()
        
        # Check if date is clean day
        is_clean = session.query(SmokingEntry).filter_by(date='2026-01-15').first() is None
        ```
    
    Trigger Analysis:
        ```python
        # Most common smoking location
        from sqlalchemy import func
        
        most_common = session.query(
            SmokingEntry.location,
            func.count(SmokingEntry.location).label('count')
        )\
        .filter(SmokingEntry.location.isnot(None))\
        .group_by(SmokingEntry.location)\
        .order_by(func.count(SmokingEntry.location).desc())\
        .first()
        ```
    
    Cessation Support:
        - Identify high-risk situations (location patterns)
        - Track progress (increasing gaps between entries)
        - Provide motivation (clean streak counter)
        - Analyze triggers (location + remarks analysis)
        - Monitor cigarette count trends
    """
    __tablename__ = "smoking_entries"
    
    date = Column(Date, primary_key=True, index=True)
    cigarette_count = Column(Integer, nullable=False)
    location = Column(SQLEnum(LocationType), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
