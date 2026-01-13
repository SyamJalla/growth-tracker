"""
Tests for KPI calculation logic in dashboard
"""
import pytest
from datetime import date, timedelta
from db.models import WorkoutEntry, SmokingEntry, WorkoutType, IntensityLevel, SmokingLocation


def test_workout_streak_calculation_single_day(client, db_session):
    """Test workout streak with single workout day"""
    workout = WorkoutEntry(
        date=date(2026, 1, 13),
        workout_type=WorkoutType.PUSH,
        workout_done=True,
        duration_minutes=60
    )
    db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    assert stats["current_workout_streak"] == 1
    assert stats["longest_workout_streak"] == 1


def test_workout_streak_consecutive_days(client, db_session):
    """Test workout streak with consecutive workout days"""
    # Create consecutive workouts
    for i in range(5):
        workout = WorkoutEntry(
            date=date(2026, 1, 9) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            duration_minutes=60
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    assert stats["longest_workout_streak"] >= 5


def test_workout_streak_broken(client, db_session):
    """Test workout streak calculation with break in between"""
    # Create workout entries with a gap
    dates = [
        date(2026, 1, 10),
        date(2026, 1, 11),
        # Gap on Jan 12
        date(2026, 1, 13)
    ]
    
    for d in dates:
        workout = WorkoutEntry(
            date=d,
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            duration_minutes=60
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    # Longest streak should be 2 (Jan 10-11)
    assert stats["longest_workout_streak"] == 2
    # Current streak depends on today's date


def test_workout_completion_rate(client, db_session):
    """Test workout completion rate calculation"""
    # Create mix of completed and skipped workouts
    workouts = [
        (date(2026, 1, 10), True, 60),
        (date(2026, 1, 11), True, 45),
        (date(2026, 1, 12), False, 0),
        (date(2026, 1, 13), True, 30)
    ]
    
    for d, done, duration in workouts:
        workout = WorkoutEntry(
            date=d,
            workout_type=WorkoutType.PUSH,
            workout_done=done,
            duration_minutes=duration
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    assert stats["total_workouts_completed"] == 3
    assert stats["total_workout_days"] == 4
    assert stats["workout_completion_rate"] == 75.0  # 3/4 = 75%


def test_workout_average_duration(client, db_session):
    """Test average duration calculation"""
    durations = [45, 60, 30, 90]
    
    for i, duration in enumerate(durations):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            duration_minutes=duration
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    expected_avg = sum(durations) / len(durations)
    assert abs(stats["avg_duration_minutes"] - expected_avg) < 0.1


def test_smoking_streak_calculation_zero_days(client, db_session):
    """Test smoking streak with smoke-free days"""
    # Create entries with cigarette_count = 0
    for i in range(3):
        entry = SmokingEntry(
            date=date(2026, 1, 11) + timedelta(days=i),
            cigarette_count=0,
            remarks="Smoke-free!"
        )
        db_session.add(entry)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"smoking\"]
    # All days are smoke-free
    assert stats["current_smoke_free_streak"] >= 3


def test_smoking_streak_with_relapses(client, db_session):
    """Test smoking streak calculation with relapses"""
    entries = [
        (date(2026, 1, 10), 5),
        (date(2026, 1, 11), 0),
        (date(2026, 1, 12), 0),
        (date(2026, 1, 13), 3)
    ]
    
    for d, count in entries:
        entry = SmokingEntry(
            date=d,
            cigarette_count=count,
            location=SmokingLocation.HOME if count > 0 else None
        )
        db_session.add(entry)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"smoking\"]
    # Longest smoke-free streak should be 2 (Jan 11-12)
    assert stats["longest_smoke_free_streak"] == 2
    # Current streak is 0 because Jan 13 has cigarettes
    assert stats["current_smoke_free_streak"] == 0


def test_smoking_total_cigarettes(client, db_session):
    """Test total cigarettes calculation"""
    counts = [5, 0, 3, 0, 8]
    
    for i, count in enumerate(counts):
        entry = SmokingEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            cigarette_count=count,
            location=SmokingLocation.HOME if count > 0 else None
        )
        db_session.add(entry)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"smoking\"]
    assert stats["total_cigarettes"] == sum(counts)  # 16


def test_smoking_average_per_day(client, db_session):
    """Test average cigarettes per day calculation"""
    counts = [5, 0, 3, 8]
    
    for i, count in enumerate(counts):
        entry = SmokingEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            cigarette_count=count
        )
        db_session.add(entry)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"smoking\"]
    expected_avg = sum(counts) / len(counts)  # 16 / 4 = 4.0
    assert abs(stats["avg_cigarettes_per_day"] - expected_avg) < 0.1


def test_empty_data_returns_zero_stats(client, db_session):
    """Test that empty database returns all zero statistics"""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    data = response.json()
    
    # Workout stats should all be zero
    workout = data["workout"]
    assert workout["total_workouts_completed"] == 0
    assert workout["current_workout_streak"] == 0
    assert workout["longest_workout_streak"] == 0
    
    # Smoking stats should all be zero
    smoking = data["smoking"]
    assert smoking["total_cigarettes"] == 0
    assert smoking["current_smoke_free_streak"] == 0


def test_workout_only_skipped_days(client, db_session):
    """Test statistics when all workout days are skipped"""
    for i in range(3):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=False,
            duration_minutes=0
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"workout\"]
    assert stats["total_workouts_completed"] == 0
    assert stats["workout_completion_rate"] == 0.0
    assert stats["current_workout_streak"] == 0


def test_mixed_intensity_levels(client, db_session):
    """Test with different intensity levels"""
    intensities = [IntensityLevel.LOW, IntensityLevel.MODERATE, IntensityLevel.HIGH]
    
    for i, intensity in enumerate(intensities):
        workout = WorkoutEntry(
            date=date(2026, 1, 10) + timedelta(days=i),
            workout_type=WorkoutType.PUSH,
            workout_done=True,
            duration_minutes=60,
            intensity=intensity
        )
        db_session.add(workout)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    # Should successfully calculate stats with mixed intensities
    assert response.json()["workout"]["total_workouts_completed"] == 3


def test_smoking_days_counting(client, db_session):
    """Test that only days with cigarettes count as smoking days"""
    entries = [
        (date(2026, 1, 10), 5),
        (date(2026, 1, 11), 0),
        (date(2026, 1, 12), 3),
        (date(2026, 1, 13), 0)
    ]
    
    for d, count in entries:
        entry = SmokingEntry(
            date=d,
            cigarette_count=count
        )
        db_session.add(entry)
    db_session.commit()
    
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    
    stats = response.json()[\"smoking\"]
    # Only 2 days had cigarettes (Jan 10 and Jan 12)
    assert stats["total_smoking_days"] == 2
