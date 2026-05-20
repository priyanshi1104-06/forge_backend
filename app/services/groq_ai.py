from groq import Groq
from app.config import GROQ_KEY

client = Groq(api_key=GROQ_KEY)

def get_recommendation(profile: dict, goal: str, include_diet: bool, include_workout: bool) -> str:
    prompt = f"""
    Create a personalized fitness plan for:
    - Age: {profile.get('age')}
    - Weight: {profile.get('weight_kg')}kg
    - Height: {profile.get('height_cm')}cm
    - Goal: {goal}
    - Experience: {profile.get('experience_level')}

    {"Include a detailed weekly workout split with sets and reps." if include_workout else ""}
    {"Include a daily meal plan with macros and calories." if include_diet else ""}
    Be specific and practical.
    """

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",

        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content