from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ai_recommendation import AIRecommendation
from app.models.profile import UserProfile
from app.schemas.ai import RecommendationRequest, RecommendationResponse
from app.services.groq_ai import get_recommendation
from app.routers.users import get_current_user
from app.models.user import User
router = APIRouter(prefix="/ai", tags=["AI"])
@router.post("/recommend", response_model=RecommendationResponse)
def recommend(data: RecommendationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_dict = {
        "age": profile.age,
        "weight_kg": profile.weight_kg,
        "height_cm": profile.height_cm,
        "experience_level": profile.experience_level
    }

    try:
        content = get_recommendation(
            profile_dict,
            data.goal,
            data.include_diet,
            data.include_workout
        )
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"AI service failed: {str(error)}"
        )

    rec = AIRecommendation(user_id=current_user.id, type="workout_diet", content=content)
    db.add(rec)
    db.commit()

    return {"content": content, "type": "workout_diet"}
