import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "FitFlow Gym Management")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gym.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY_BEFORE_DEPLOYMENT")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
