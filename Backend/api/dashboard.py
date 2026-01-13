from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import get_db
from db.models import WorkoutEntry, SmokingEntry

router = APIRouter()

# Start date for 2026 tracking
YEAR_START = date(2026, 1, 1)
YEAR_END = date(2026, 12, 31)


class WorkoutStats(BaseModel):
    current_streak: int
    longest_streak: int
    total_workout_days: int
    total_days: int
    workout_percentage: float
    average_duration: Optional[float]
    most_common_type: Optional[str]


class SmokingStats(BaseModel):
    current_clean_streak: int
    total_relapses: int
    longest_clean_streak: int
    total_cigarettes: int
    most_common_location: Optional[str]


class DashboardResponse(BaseModel):
    workout: WorkoutStats
    smoking: SmokingStats
    last_updated: date


def calculate_workout_stats(db: Session) -> WorkoutStats:
    """Calculate all workout KPIs for 2026"""
    # Get all workout entries for 2026
    workouts = db.query(WorkoutEntry).filter(
        WorkoutEntry.date >= YEAR_START,
        WorkoutEntry.date <= YEAR_END
    ).order_by(WorkoutEntry.date).all()
    
    if not workouts:
        return WorkoutStats(
            current_streak=0,
            longest_streak=0,
            total_workout_days=0,
            total_days=0,
            workout_percentage=0.0,
            average_duration=None,
            most_common_type=None
        )
    
    # Get last update date and calculate total days
    last_update = workouts[-1].date
    total_days = (last_update - YEAR_START).days + 1
    
    # Filter only days where workout was done
    workout_dates = [w.date for w in workouts if w.workout_done]
    total_workout_days = len(workout_dates)
    workout_percentage = (total_workout_days / total_days * 100) if total_days > 0 else 0.0
    
    # Calculate current streak (from end backwards)
    current_streak = 0
    check_date = date.today()
    while check_date >= YEAR_START:
        if check_date in workout_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Calculate longest streak
    longest_streak = 0
    current = 0
    check_date = YEAR_START
    
    while check_date <= last_update:
        if check_date in workout_dates:
            current += 1
            longest_streak = max(longest_streak, current)
        else:
            current = 0
        check_date += timedelta(days=1)
    
    # Calculate average duration
    durations = [w.duration_minutes for w in workouts if w.duration_minutes is not None]
    average_duration = sum(durations) / len(durations) if durations else None
    
    # Find most common workout type
    type_counts = {}
    for w in workouts:
        if w.workout_done:
            type_counts[w.workout_type.value] = type_counts.get(w.workout_type.value, 0) + 1
    most_common_type = max(type_counts, key=type_counts.get) if type_counts else None
    
    return WorkoutStats(
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_workout_days=total_workout_days,
        total_days=total_days,
        workout_percentage=round(workout_percentage, 2),
        average_duration=round(average_duration, 1) if average_duration else None,
        most_common_type=most_common_type
    )


def calculate_smoking_stats(db: Session) -> SmokingStats:
    """Calculate all smoking KPIs for 2026"""
    # Get all smoking entries for 2026
    smoking_entries = db.query(SmokingEntry).filter(
        SmokingEntry.date >= YEAR_START,
        SmokingEntry.date <= YEAR_END
    ).order_by(SmokingEntry.date).all()
    
    total_relapses = len(smoking_entries)
    
    if total_relapses == 0:
        # Perfect clean year!
        today = date.today()
        current_clean_streak = (today - YEAR_START).days + 1 if today >= YEAR_START else 0
        return SmokingStats(
            current_clean_streak=current_clean_streak,
            total_relapses=0,
            longest_clean_streak=current_clean_streak,
            total_cigarettes=0,
            most_common_location=None
        )
    
    smoking_dates = [s.date for s in smoking_entries]
    
    # Calculate current clean streak (from today backwards)
    current_clean_streak = 0
    check_date = date.today()
    while check_date >= YEAR_START:
        if check_date not in smoking_dates:
            current_clean_streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Calculate longest clean streak
    longest_clean_streak = 0
    current = 0
    check_date = YEAR_START
    last_smoking_date = smoking_entries[-1].date
    
    while check_date <= date.today():
        if check_date not in smoking_dates:
            current += 1
            longest_clean_streak = max(longest_clean_streak, current)
        else:
            current = 0
        check_date += timedelta(days=1)
    
    # Calculate total cigarettes
    total_cigarettes = sum(s.cigarette_count for s in smoking_entries)
    
    # Find most common location
    location_counts = {}
    for s in smoking_entries:
        if s.location:
            loc = s.location.value
            location_counts[loc] = location_counts.get(loc, 0) + 1
    most_common_location = max(location_counts, key=location_counts.get) if location_counts else None
    
    return SmokingStats(
        current_clean_streak=current_clean_streak,
        total_relapses=total_relapses,
        longest_clean_streak=longest_clean_streak,
        total_cigarettes=total_cigarettes,
        most_common_location=most_common_location
    )


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """Get combined dashboard with workout and smoking statistics"""
    workout_stats = calculate_workout_stats(db)
    smoking_stats = calculate_smoking_stats(db)
    
    return DashboardResponse(
        workout=workout_stats,
        smoking=smoking_stats,
        last_updated=date.today()
    )
