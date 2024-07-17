from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

    secret_key: str = "secret_key"
    algorithm: str = "algorithm"

    model_config = SettingsConfigDict(extra='ignore', env_file='.env', env_file_encoding='utf-8')


settings = Settings()
