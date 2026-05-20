from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET    = os.getenv("JWT_SECRET_KEY", "supersecretkey123")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY    = int(os.getenv("JWT_EXPIRY_MINUTES", 60))
GROQ_KEY      = os.getenv("GROQ_API_KEY")