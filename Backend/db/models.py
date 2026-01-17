from sqlalchemy import Column, Integer, String, Date, Text, Boolean, Enum, DateTime
from db.database import Base
from datetime import datetime
import enum


class WorkoutType(str, enum.Enum):
    PUSH = "Push"
    PULL = "Pull"
    LEGS = "Legs"
    UPPER = "Upper"
    LOWER = "Lower"
    CARDIO = "Cardio"
    OTHERS = "Others"


class IntensityLevel(str, enum.Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class SmokingLocation(str, enum.Enum):
    HOME = "Home"
    WORK = "Work"
    SOCIAL = "Social"
    OTHER = "Other"


class WorkoutEntry(Base):
    __tablename__ = "workout_entries"
    
    date = Column(Date, primary_key=True, index=True)
    workout_type = Column(Enum(WorkoutType, native_enum=False, length=50), nullable=False)
    workout_done = Column(Boolean, nullable=False, default=True)
    duration_minutes = Column(Integer, nullable=True)
    intensity = Column(Enum(IntensityLevel, native_enum=False, length=50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SmokingEntry(Base):
    __tablename__ = "smoking_entries"
    
    date = Column(Date, primary_key=True, index=True)
    cigarette_count = Column(Integer, nullable=False, default=1)
    location = Column(Enum(SmokingLocation, native_enum=False, length=50), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class HealthCheck(Base):
    __tablename__ = "health_check"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
