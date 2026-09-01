from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_chat_model: str = Field(default="qwen3:4b")
    ollama_embed_model: str = Field(default="embeddinggemma")
    ollama_timeout_seconds: int = Field(default=120)
    frontend_origin: str = Field(default="http://localhost:3000")
    chroma_collection: str = Field(default="coursework_chunks")
    chunk_size: int = Field(default=220)
    chunk_overlap: int = Field(default=40)
    top_k: int = Field(default=4)
    ocr_min_score: float = Field(default=0.45)
    intent_router_min_confidence: float = Field(default=0.60)

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    @property
    def raw_data_dir(self) -> Path:
        return self.project_root / "data" / "raw"

    @property
    def chroma_dir(self) -> Path:
        return self.project_root / "data" / "processed" / "chroma"

    @property
    def intent_router_dir(self) -> Path:
        return self.project_root / "data" / "processed" / "ml" / "intent_router"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.raw_data_dir.mkdir(parents=True, exist_ok=True)
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    settings.intent_router_dir.mkdir(parents=True, exist_ok=True)
    return settings
