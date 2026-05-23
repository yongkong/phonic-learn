from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "WordWorld API"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./wordworld.db"
    AUDIO_DIR: str = "./static/audios"
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
