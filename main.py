from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, users, workouts, exercises, progress, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FORGE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(progress.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "FORGE API is running"}
