from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    chroma_path: str = "./chroma_data"
    collection_name: str = "gacha_shops"
    rag_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
