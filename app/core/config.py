import os


class Settings:
    # General settings
    PROJECT_NAME: str = "FastAPI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"

    # Database
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_HOSTNAME: str = os.getenv("DB_HOSTNAME", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", 5432)
    DB_DATABASE: str = os.getenv("DB_DATABASE", "postgres")

    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql://{ DB_USER }:{ DB_PASSWORD }@{ DB_HOSTNAME }:{ DB_PORT }/{ DB_DATABASE }"
    )

    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = (
        f"db+postgresql://{ DB_USER }:{ DB_PASSWORD }@{ DB_HOSTNAME }:{ DB_PORT }/{ DB_DATABASE }"
    )


settings = Settings()
