import os
import yaml
import jsonref
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator

from fastmock.core.config import settings
from fastmock.core.state import app_state


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan события для запуска и остановки сервера."""
    
    # Пытаемся загрузить дефолтную спеку при старте
    if os.path.exists(settings.default_spec_path):
        print(f"[*] Found default spec at {settings.default_spec_path}. Loading...")
        try:
            with open(settings.default_spec_path, "r", encoding="utf-8") as f:
                raw_spec = yaml.safe_load(f)
                
                # jsonref автоматически заменяет все $ref на реальные объекты
                # Это избавляет нас от необходимости писать свой сложный резолвер
                resolved_spec = jsonref.replace_refs(raw_spec)
                app_state.spec = resolved_spec  # type: ignore
                
            print(f"[*] Spec '{app_state.spec.get('info', {}).get('title', 'Unknown')}' loaded successfully.")
        except Exception as e:
            print(f"[!] Error loading spec: {e}")
    else:
        print(f"[*] No default spec found at {settings.default_spec_path}. Please upload via Admin API.")
    
    yield
    
    # Очистка при выключении
    print("[*] Shutting down FastMock...")


app = FastAPI(
    title=settings.app_name,
    description="""
**EN:** A lightweight, local Mock server on FastAPI for frontend and mobile teams.
Upload your OpenAPI spec via `/_admin/specs` and get a working mock API instantly.

**RU:** Легковесный, локальный Mock-сервер на FastAPI для фронтенд- и мобильных команд.
Загрузите вашу OpenAPI спецификацию через `/_admin/specs` и мгновенно получите работающий мок-API.
    """,
    version="0.1.0",
    lifespan=lifespan
)

from fastmock.api.middlewares import ChaosMiddleware
from fastmock.api.admin_routes import router as admin_router
from fastmock.api.dynamic_router import router as mock_router

# Добавляем Middleware (порядок важен)
app.add_middleware(ChaosMiddleware)

# Подключаем админку
app.include_router(admin_router)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.app_name}. Use /_admin to manage the server."}

# Подключаем catch-all роутер последним!
app.include_router(mock_router)

def start() -> None:
    """Точка входа для запуска из терминала (команда fastmock)."""
    uvicorn.run(
        "fastmock.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

if __name__ == "__main__":
    start()
