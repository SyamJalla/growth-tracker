from sqlalchemy import Column, Integer, String, Date, Text
from db.database import Base


class SmokingEntry(Base):
    __tablename__ = "smoking_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    cigarettes = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)


class WorkoutEntry(Base):
    __tablename__ = "workout_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    activity = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
