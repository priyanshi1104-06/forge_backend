from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    goal: str
    include_diet: bool = True
    include_workout: bool = True

class RecommendationResponse(BaseModel):
    content: str
    type: str