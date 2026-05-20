from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.exercise import Exercise
from app.models.workout import WorkoutSession
from app.schemas.workout import ExerciseLog, ExerciseResponse
from app.services.workout_logic import update_pr
from app.routers.users import get_current_user
from app.models.user import User

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.post("/", response_model=ExerciseResponse)
def log_exercise(data: ExerciseLog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == data.session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")

    exercise = Exercise(**data.dict())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    update_pr(db, current_user.id, data.name, data.weight_kg)
    return exercise

@router.get("/{session_id}", response_model=List[ExerciseResponse])
def get_exercises(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")

    return db.query(Exercise).filter(Exercise.session_id == session_id).all()
