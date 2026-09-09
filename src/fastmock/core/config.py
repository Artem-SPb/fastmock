from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastMock API Engine"
    host: str = "0.0.0.0"
    port: int = 8000
    default_spec_path: str = "openapi.yaml"
    debug: bool = True

settings = Settings()
