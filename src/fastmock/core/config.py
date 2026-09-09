from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastMock API Engine"
    host: str = "0.0.0.0"
    port: int = 8000
    default_spec_path: str = "openapi.yaml"
    persist_path: str | None = None  # Путь к файлу для сохранения БД (например, db.json)
    debug: bool = True

settings = Settings()
