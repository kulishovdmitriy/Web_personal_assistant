from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

    secret_key: str = "secret_key"
    algorithm: str = "algorithm"

    MAIL_USERNAME: EmailStr = "example@example.com"
    MAIL_PASSWORD: str = "your_email_password"
    MAIL_FROM: str = "example@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.example.com"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(extra='ignore', env_file='.env', env_file_encoding='utf-8')


settings = Settings()
