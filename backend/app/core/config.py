from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database & auth
    DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    LLM_TEMPERATURE: float = 0.7
    MAX_HISTORY_MESSAGES: int = 12

    # RAG
    FAISS_INDEX_DIR: str = str(BASE_DIR / "faiss_index")
    DOCUMENT_REGISTRY_PATH: str = str(BASE_DIR / "data" / "document_registry.json")
    RAG_TOP_K: int = 4
    RAG_CHUNK_SIZE: int = 900
    RAG_CHUNK_OVERLAP: int = 150
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Voice / VAD
    SAMPLE_RATE: int = 16000
    SPEECH_ENERGY_THRESHOLD: float = 0.015
    SILENCE_DURATION_SEC: float = 1.2
    MAX_UTTERANCE_DURATION_SEC: float = 30.0
    PRE_SPEECH_BUFFER_SEC: float = 0.3
    CONVERSATION_IDLE_TIMEOUT_SEC: float = 120.0
    MAX_SILENT_TURNS: int = 2

    # Wake word
    WAKE_WORD: str = "hey_jarvis"
    WAKE_WORD_THRESHOLD: float = 0.5

    # Tavily
    TAVILY_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Backward-compatible module-level exports
DATABASE_URL = settings.DATABASE_URL
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
GROQ_API_KEY = settings.GROQ_API_KEY
