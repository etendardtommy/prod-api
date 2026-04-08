import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/eclyps_db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

ALLOWED_ORIGINS = [
    "https://eclyps-esport.fr",
    "https://portfolio.t-etendard.fr",
    "https://admin.t-etendard.fr",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5174",
]

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
API_PUBLIC_URL = os.getenv("API_PUBLIC_URL", "https://api.t-etendard.fr")
