from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Financial Compliance Superintelligence"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"

settings = Settings()
