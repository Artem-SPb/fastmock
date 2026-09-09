import yaml
import jsonref
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field

from fastmock.core.state import app_state

router = APIRouter(prefix="/_admin", tags=["Admin API | Управление сервером"])

class ChaosConfig(BaseModel):
    chaos_delay_ms: int = Field(
        0, 
        description="**EN:** Global delay in milliseconds for all requests.\n\n**RU:** Глобальная задержка в миллисекундах для всех запросов.",
        json_schema_extra={"example": 500}
    )
    chaos_error_rate: float = Field(
        0.0, 
        description="**EN:** Probability of random errors (from 0.0 to 1.0).\n\n**RU:** Вероятность случайных ошибок (от 0.0 до 1.0).",
        json_schema_extra={"example": 0.2}
    )
    chaos_allowed_errors: list[int] = Field(
        [500, 502, 503], 
        description="**EN:** List of allowed HTTP status codes for chaos errors.\n\n**RU:** Список разрешенных HTTP-статусов для случайных ошибок.",
        json_schema_extra={"example": [400, 403, 500, 503]}
    )

@router.get(
    "/config",
    summary="Get Chaos Config | Получить настройки хаоса",
    description="**EN:** Returns the current global network throttling and chaos engineering settings.\n\n**RU:** Возвращает текущие глобальные настройки задержек сети и случайных ошибок."
)
async def get_config() -> ChaosConfig:
    return ChaosConfig(
        chaos_delay_ms=app_state.chaos_delay_ms,
        chaos_error_rate=app_state.chaos_error_rate,
        chaos_allowed_errors=app_state.chaos_allowed_errors
    )

@router.put(
    "/config",
    summary="Update Chaos Config | Обновить настройки хаоса",
    description="**EN:** Updates global delays and error rates. These settings apply to all mock routes.\n\n**RU:** Обновляет глобальные задержки и частоту ошибок. Эти настройки применяются ко всем мок-эндпоинтам."
)
async def set_config(config: ChaosConfig):
    app_state.chaos_delay_ms = config.chaos_delay_ms
    app_state.chaos_error_rate = config.chaos_error_rate
    app_state.chaos_allowed_errors = config.chaos_allowed_errors
    return {"message": "Chaos configuration updated", "config": config.model_dump()}

@router.delete(
    "/state",
    summary="Clear In-Memory State | Очистить базу данных",
    description="**EN:** Clears the in-memory database used for CRUD operations (POST/PUT/GET).\n\n**RU:** Очищает In-Memory базу данных, используемую для CRUD операций (сохраненные мок-сущности)."
)
async def clear_state():
    app_state.clear_db()
    return {"message": "In-Memory database cleared."}

@router.post(
    "/specs",
    summary="Upload OpenAPI Spec | Загрузить спецификацию",
    description="**EN:** Upload an OpenAPI 3.0/3.1 specification file (YAML or JSON) to dynamically generate mock routes.\n\n**RU:** Загрузите файл спецификации OpenAPI 3.0/3.1 (YAML или JSON) для динамической генерации мок-роутов."
)
async def upload_spec(file: UploadFile = File(..., description="**EN:** OpenAPI spec file (.yaml or .json)\n\n**RU:** Файл спецификации (.yaml или .json)")):
    content = await file.read()
    try:
        raw_spec = yaml.safe_load(content.decode("utf-8"))
        resolved_spec = jsonref.replace_refs(raw_spec)
        app_state.spec = resolved_spec # type: ignore
        title = app_state.spec.get("info", {}).get("title", "Unknown") if isinstance(app_state.spec, dict) else "Unknown"
        return {"message": f"Spec '{title}' loaded successfully."}
    except Exception as e:
        return {"error": f"Failed to parse spec: {str(e)}"}

@router.get(
    "/routes",
    summary="List Mocked Routes | Список мок-роутов",
    description="**EN:** Returns a list of all dynamically generated mock endpoints currently active.\n\n**RU:** Возвращает список всех динамически сгенерированных мок-эндпоинтов, которые сейчас готовы к работе."
)
async def list_routes():
    if not app_state.spec or "paths" not in app_state.spec:
        return {"routes": []}
        
    routes = []
    for path, path_item in app_state.spec["paths"].items():
        if isinstance(path_item, dict):
            for method in path_item.keys():
                if method.lower() in ["get", "post", "put", "delete", "patch"]:
                    routes.append(f"{method.upper()} {path}")
                
    return {"routes": routes}
