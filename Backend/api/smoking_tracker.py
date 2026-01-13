from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import SmokingEntry, SmokingLocation

router = APIRouter()


class SmokingCreate(BaseModel):
    date: date
    cigarette_count: int = Field(default=1, ge=1)
    location: Optional[SmokingLocation] = None
    remarks: Optional[str] = None


class SmokingResponse(BaseModel):
    date: date
    cigarette_count: int
    location: Optional[SmokingLocation]
    remarks: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=SmokingResponse, status_code=201)
def create_smoking_entry(smoking: SmokingCreate, db: Session = Depends(get_db)):
    """Create a new smoking entry for a specific date"""
    # Check if entry already exists for this date
    existing = db.query(SmokingEntry).filter(SmokingEntry.date == smoking.date).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Smoking entry already exists for {smoking.date}")
    
    db_smoking = SmokingEntry(**smoking.dict())
    db.add(db_smoking)
    db.commit()
    db.refresh(db_smoking)
    return db_smoking


@router.get("/{entry_date}", response_model=SmokingResponse)
def get_smoking_entry(entry_date: date, db: Session = Depends(get_db)):
    """Get smoking entry for a specific date"""
    smoking = db.query(SmokingEntry).filter(SmokingEntry.date == entry_date).first()
    if not smoking:
        raise HTTPException(status_code=404, detail=f"No smoking entry found for {entry_date}")
    return smoking


@router.delete("/{entry_date}", status_code=204)
def delete_smoking_entry(entry_date: date, db: Session = Depends(get_db)):
    """Delete smoking entry for a specific date"""
    db_smoking = db.query(SmokingEntry).filter(SmokingEntry.date == entry_date).first()
    if not db_smoking:
        raise HTTPException(status_code=404, detail=f"No smoking entry found for {entry_date}")
    
    db.delete(db_smoking)
    db.commit()
    return None


@router.get("/history/", response_model=List[SmokingResponse])
def get_smoking_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get smoking history with optional date range filtering"""
    query = db.query(SmokingEntry)
    
    if start_date:
        query = query.filter(SmokingEntry.date >= start_date)
    if end_date:
        query = query.filter(SmokingEntry.date <= end_date)
    
    smoking_entries = query.order_by(SmokingEntry.date.desc()).all()
    return smoking_entries
