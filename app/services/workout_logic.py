from sqlalchemy.orm import Session
from app.models.record import PersonalRecord

def update_pr(db: Session, user_id: int, exercise_name: str, weight_kg: float):
    existing = db.query(PersonalRecord).filter(
        PersonalRecord.user_id == user_id,
        PersonalRecord.exercise_name == exercise_name
    ).first()

    if not existing:
        pr = PersonalRecord(user_id=user_id, exercise_name=exercise_name, max_weight_kg=weight_kg)
        db.add(pr)
        db.commit()
    elif weight_kg > existing.max_weight_kg:
        existing.max_weight_kg = weight_kg
        db.commit()