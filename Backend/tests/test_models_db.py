"""
Tests for database models
"""
import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from db.models import WorkoutEntry, SmokingEntry, WorkoutType, IntensityLevel, SmokingLocation


def test_create_workout_entry_model(db_session):
    """Test creating a WorkoutEntry model instance"""
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True,
        duration_minutes=60,
        intensity=IntensityLevel.MODERATE,
        notes="Test workout"
    )
    
    db_session.add(workout)
    db_session.commit()
    
    # Query back
    retrieved = db_session.query(WorkoutEntry).filter_by(date=date(2026, 1, 13)).first()
    assert retrieved is not None
    assert retrieved.workout_type == WorkoutType.PUSH
    assert retrieved.workout_done is True
    assert retrieved.duration_minutes == 60
    assert retrieved.intensity == IntensityLevel.MODERATE
    assert retrieved.notes == "Test workout"


def test_workout_entry_date_primary_key(db_session):
    """Test that date is primary key and enforces uniqueness"""
    workout1 = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True
    )
    db_session.add(workout1)
    db_session.commit()
    
    # Try to add another entry with same date
    workout2 = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PULL,
        workout_done=True
    )
    db_session.add(workout2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_workout_type_enum(db_session):
    """Test WorkoutType enum values"""
    valid_types = [WorkoutType.PUSH, WorkoutType.PULL, WorkoutType.LEGS]
    
    for i, workout_type in enumerate(valid_types):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=workout_type,
            workout_done=True
        )
        db_session.add(workout)
    
    db_session.commit()
    
    # Verify all were saved correctly
    count = db_session.query(WorkoutEntry).count()
    assert count == 3


def test_intensity_level_enum(db_session):
    """Test IntensityLevel enum values"""
    intensities = [IntensityLevel.LOW, IntensityLevel.MODERATE, IntensityLevel.HIGH]
    
    for i, intensity in enumerate(intensities):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            intensity=intensity
        )
        db_session.add(workout)
    
    db_session.commit()
    
    # Verify all intensities were saved
    workouts = db_session.query(WorkoutEntry).all()
    assert len(workouts) == 3
    assert all(w.intensity in intensities for w in workouts)


def test_workout_optional_fields(db_session):
    """Test that optional fields can be None"""
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=False
        # duration_minutes, intensity, notes not provided
    )
    
    db_session.add(workout)
    db_session.commit()
    
    retrieved = db_session.query(WorkoutEntry).first()
    assert retrieved.duration_minutes is None
    assert retrieved.intensity is None
    assert retrieved.notes is None


def test_create_smoking_entry_model(db_session):
    """Test creating a SmokingEntry model instance"""
    smoking = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=5,
        location=SmokingLocation.HOME,
        remarks="Test entry"
    )
    
    db_session.add(smoking)
    db_session.commit()
    
    # Query back
    retrieved = db_session.query(SmokingEntry).filter_by(date=date(2026, 1, 13)).first()
    assert retrieved is not None
    assert retrieved.cigarette_count == 5
    assert retrieved.location == SmokingLocation.HOME
    assert retrieved.remarks == "Test entry"


def test_smoking_entry_date_primary_key(db_session):
    """Test that date is primary key for smoking entries"""
    smoking1 = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=5
    )
    db_session.add(smoking1)
    db_session.commit()
    
    # Try to add another entry with same date
    smoking2 = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=10
    )
    db_session.add(smoking2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_smoking_location_enum(db_session):
    """Test SmokingLocation enum values"""
    locations = [SmokingLocation.HOME, SmokingLocation.WORK, SmokingLocation.SOCIAL, SmokingLocation.OTHER]
    
    for i, location in enumerate(locations):
        smoking = SmokingEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            cigarette_count=5,
            location=location
        )
        db_session.add(smoking)
    
    db_session.commit()
    
    # Verify all locations were saved
    entries = db_session.query(SmokingEntry).all()
    assert len(entries) == 4
    assert all(e.location in locations for e in entries)


def test_smoking_zero_cigarettes(db_session):
    """Test that cigarette_count can be zero (smoke-free day)"""
    smoking = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=0,
        remarks="Smoke-free day!"
    )
    
    db_session.add(smoking)
    db_session.commit()
    
    retrieved = db_session.query(SmokingEntry).first()
    assert retrieved.cigarette_count == 0


def test_smoking_optional_fields(db_session):
    """Test that optional fields can be None"""
    smoking = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=0
        # location and remarks not provided
    )
    
    db_session.add(smoking)
    db_session.commit()
    
    retrieved = db_session.query(SmokingEntry).first()
    assert retrieved.location is None
    assert retrieved.remarks is None


def test_query_multiple_workout_entries(db_session):
    """Test querying multiple workout entries"""
    # Add multiple entries
    for i in range(5):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=True
        )
        db_session.add(workout)
    
    db_session.commit()
    
    # Query all
    entries = db_session.query(WorkoutEntry).all()
    assert len(entries) == 5


def test_query_multiple_smoking_entries(db_session):
    """Test querying multiple smoking entries"""
    # Add multiple entries
    for i in range(5):
        smoking = SmokingEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            cigarette_count=i
        )
        db_session.add(smoking)
    
    db_session.commit()
    
    # Query all
    entries = db_session.query(SmokingEntry).all()
    assert len(entries) == 5


def test_update_workout_entry(db_session):
    """Test updating an existing workout entry"""
    # Create entry
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True,
        duration_minutes=60
    )
    db_session.add(workout)
    db_session.commit()
    
    # Update entry
    workout.duration_minutes = 90
    workout.notes = "Extended session"
    db_session.commit()
    
    # Verify update
    retrieved = db_session.query(WorkoutEntry).filter_by(date=date(2026, 1, 13)).first()
    assert retrieved.duration_minutes == 90
    assert retrieved.notes == "Extended session"


def test_delete_workout_entry(db_session):
    """Test deleting a workout entry"""
    # Create entry
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True
    )
    db_session.add(workout)
    db_session.commit()
    
    # Delete entry
    db_session.delete(workout)
    db_session.commit()
    
    # Verify deletion
    count = db_session.query(WorkoutEntry).count()
    assert count == 0


def test_delete_smoking_entry(db_session):
    """Test deleting a smoking entry"""
    # Create entry
    smoking = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=5
    )
    db_session.add(smoking)
    db_session.commit()
    
    # Delete entry
    db_session.delete(smoking)
    db_session.commit()
    
    # Verify deletion
    count = db_session.query(SmokingEntry).count()
    assert count == 0


def test_workout_and_smoking_same_date(db_session):
    """Test that workout and smoking entries can exist for the same date"""
    # Create workout entry
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True
    )
    db_session.add(workout)
    
    # Create smoking entry for same date
    smoking = SmokingEntry(
        date=date(2026, 1, 13),
        cigarette_count=3
    )
    db_session.add(smoking)
    
    db_session.commit()
    
    # Verify both exist
    assert db_session.query(WorkoutEntry).count() == 1
    assert db_session.query(SmokingEntry).count() == 1


# Import timedelta for date arithmetic
from datetime import timedelta
