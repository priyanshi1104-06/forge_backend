from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.workout import WorkoutSession
from app.schemas.workout import WorkoutCreate, WorkoutResponse
from app.routers.users import get_current_user
from app.models.user import User

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/", response_model=WorkoutResponse)
def create_workout(data: WorkoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = WorkoutSession(user_id=current_user.id, **data.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get("/", response_model=List[WorkoutResponse])
def get_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(WorkoutSession).filter(WorkoutSession.user_id == current_user.id).all()

@router.delete("/{session_id}")
def delete_workout(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"message": "Deleted successfully"}