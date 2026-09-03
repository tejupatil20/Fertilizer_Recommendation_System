from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./fertilizer.db"
    MODEL_PATH: str = "ml/fertilizer_model.pkl"
    METRICS_PATH: str = "ml/model_metrics.json"
    PROJECT_NAME: str = "Smart Fertilizer Recommendation System"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
