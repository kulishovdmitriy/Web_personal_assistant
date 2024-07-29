from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

    secret_key: str = "secret_key"
    algorithm: str = "algorithm"

    MAIL_USERNAME: str = "test@test.com"
    MAIL_PASSWORD: str = "123456789"
    MAIL_FROM: str = "test@test.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"

    class Config:
        extra = 'ignore'
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
