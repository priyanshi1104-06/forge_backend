from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.exercise import Exercise
from app.models.record import PersonalRecord
from app.models.workout import WorkoutSession
from app.routers.users import get_current_user
from app.models.user import User

router = APIRouter(prefix="/progress", tags=["Progress"])

COMPARISON_OBJECTS = [
    {"object_name": "loaded suitcase", "object_weight_kg": 25},
    {"object_name": "washing machine", "object_weight_kg": 70},
    {"object_name": "motorcycle", "object_weight_kg": 180},
    {"object_name": "grand piano", "object_weight_kg": 300},
    {"object_name": "great white shark", "object_weight_kg": 1275},
    {"object_name": "small car", "object_weight_kg": 1500},
    {"object_name": "delivery truck", "object_weight_kg": 3500},
]

def get_volume_comparison(total_volume_kg: float):
    if total_volume_kg <= 0:
        return {
            "object_name": "empty barbell",
            "object_weight_kg": 20,
            "text": "Log your first workout to unlock a weight comparison."
        }

    comparison = min(
        COMPARISON_OBJECTS,
        key=lambda item: abs(item["object_weight_kg"] - total_volume_kg)
    )
    return {
        **comparison,
        "text": f"That's like lifting a {comparison['object_name']}!"
    }

@router.get("/prs")
def get_all_prs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    records = db.query(PersonalRecord).filter(PersonalRecord.user_id == current_user.id).all()
    return records

@router.get("/summary")
def get_progress_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workouts = db.query(WorkoutSession).filter(WorkoutSession.user_id == current_user.id).all()
    workout_ids = [workout.id for workout in workouts]

    exercises = []
    if workout_ids:
        exercises = db.query(Exercise).filter(Exercise.session_id.in_(workout_ids)).all()

    records_count = db.query(PersonalRecord).filter(PersonalRecord.user_id == current_user.id).count()
    total_volume_kg = sum(exercise.sets * exercise.reps * exercise.weight_kg for exercise in exercises)
    total_duration_mins = sum(workout.duration_mins or 0 for workout in workouts)

    heaviest = max(exercises, key=lambda exercise: exercise.weight_kg, default=None)
    best_volume = max(
        exercises,
        key=lambda exercise: exercise.sets * exercise.reps * exercise.weight_kg,
        default=None
    )

    recent_workout = max(workouts, key=lambda workout: (workout.date, workout.id), default=None)
    recent_exercises = []
    if recent_workout:
        recent_exercises = [
            exercise for exercise in exercises
            if exercise.session_id == recent_workout.id
        ]

    return {
        "total_volume_kg": round(total_volume_kg, 2),
        "total_workouts": len(workouts),
        "total_exercises": len(exercises),
        "records_count": records_count,
        "total_duration_mins": total_duration_mins,
        "heaviest_lift": {
            "exercise_name": heaviest.name,
            "weight_kg": heaviest.weight_kg
        } if heaviest else None,
        "best_set_volume": {
            "exercise_name": best_volume.name,
            "volume_kg": round(best_volume.sets * best_volume.reps * best_volume.weight_kg, 2)
        } if best_volume else None,
        "comparison": get_volume_comparison(total_volume_kg),
        "latest_workout": {
            "id": recent_workout.id,
            "date": recent_workout.date,
            "duration_mins": recent_workout.duration_mins,
            "notes": recent_workout.notes,
            "exercises": [
                {
                    "id": exercise.id,
                    "name": exercise.name,
                    "sets": exercise.sets,
                    "reps": exercise.reps,
                    "weight_kg": exercise.weight_kg
                }
                for exercise in recent_exercises
            ]
        } if recent_workout else None
    }

@router.get("/prs/{exercise_name}")
def get_exercise_pr(exercise_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(PersonalRecord).filter(
        PersonalRecord.user_id == current_user.id,
        PersonalRecord.exercise_name == exercise_name
    ).first()
    return record
