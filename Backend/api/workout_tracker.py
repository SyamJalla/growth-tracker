from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import get_db
from db.models import WorkoutEntry, WorkoutType, IntensityLevel

router = APIRouter()


class WorkoutCreate(BaseModel):
    date: date
    workout_type: WorkoutType
    workout_done: bool = True
    duration_minutes: Optional[int] = None
    intensity: Optional[IntensityLevel] = None
    notes: Optional[str] = None


class WorkoutUpdate(BaseModel):
    workout_type: Optional[WorkoutType] = None
    workout_done: Optional[bool] = None
    duration_minutes: Optional[int] = None
    intensity: Optional[IntensityLevel] = None
    notes: Optional[str] = None


class WorkoutResponse(BaseModel):
    date: date
    workout_type: WorkoutType
    workout_done: bool
    duration_minutes: Optional[int]
    intensity: Optional[IntensityLevel]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=WorkoutResponse, status_code=201)
def create_workout_entry(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """Create a new workout entry for a specific date"""
    # Check if entry already exists for this date
    existing = db.query(WorkoutEntry).filter(WorkoutEntry.date == workout.date).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Workout entry already exists for {workout.date}")
    
    db_workout = WorkoutEntry(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.get("/{entry_date}", response_model=WorkoutResponse)
def get_workout_entry(entry_date: date, db: Session = Depends(get_db)):
    """Get workout entry for a specific date"""
    workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not workout:
        raise HTTPException(status_code=404, detail=f"No workout entry found for {entry_date}")
    return workout


@router.put("/{entry_date}", response_model=WorkoutResponse)
def update_workout_entry(entry_date: date, workout: WorkoutUpdate, db: Session = Depends(get_db)):
    """Update workout entry for a specific date"""
    db_workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail=f"No workout entry found for {entry_date}")
    
    # Update only provided fields
    update_data = workout.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_workout, key, value)
    
    db_workout.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete("/{entry_date}", status_code=204)
def delete_workout_entry(entry_date: date, db: Session = Depends(get_db)):
    """Delete workout entry for a specific date"""
    db_workout = db.query(WorkoutEntry).filter(WorkoutEntry.date == entry_date).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail=f"No workout entry found for {entry_date}")
    
    db.delete(db_workout)
    db.commit()
    return None


@router.get("/history/", response_model=List[WorkoutResponse])
def get_workout_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get workout history with optional date range filtering"""
    query = db.query(WorkoutEntry)
    
    if start_date:
        query = query.filter(WorkoutEntry.date >= start_date)
    if end_date:
        query = query.filter(WorkoutEntry.date <= end_date)
    
    workouts = query.order_by(WorkoutEntry.date.desc()).all()
    return workouts
