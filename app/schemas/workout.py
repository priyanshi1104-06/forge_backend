from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class WorkoutCreate(BaseModel):
    date: date
    duration_mins: Optional[int] = None
    notes: Optional[str] = None

class WorkoutResponse(BaseModel):
    id: int
    date: date
    duration_mins: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True

class ExerciseLog(BaseModel):
    session_id: int
    name: str
    sets: int
    reps: int
    weight_kg: float

class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets: int
    reps: int
    weight_kg: float

    class Config:
        from_attributes = True