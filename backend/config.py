from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-6"
    chroma_persist_dir: str = "./data/chroma"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    whisper_model: str = "medium"
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
