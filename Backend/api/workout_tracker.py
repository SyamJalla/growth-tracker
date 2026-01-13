from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class WorkoutEntry(BaseModel):
	date: str
	activity: str
	duration_minutes: int
	notes: Optional[str] = None


# Intentionally no route handlers here — keep module minimal.
