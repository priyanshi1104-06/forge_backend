from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_goal: Optional[str] = None
    experience_level: Optional[str] = None

class ProfileResponse(BaseModel):
    age: Optional[int]
    weight_kg: Optional[float]
    height_cm: Optional[float]
    fitness_goal: Optional[str]
    experience_level: Optional[str]

    class Config:
        from_attributes = True