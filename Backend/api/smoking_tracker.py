from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class SmokingEntry(BaseModel):
	date: str
	cigarettes: int
	notes: Optional[str] = None


# Intentionally no route handlers here — keep module minimal.
