import asyncio
import random

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from fastmock.core.state import app_state


class ChaosMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Пропускаем админку и корневой роут
        if request.url.path.startswith("/_admin") or request.url.path == "/":
            return await call_next(request)
            
        # 1. Задержка (Network Throttling)
        # Проверяем заголовок X-Mock-Delay, если нет - берем из глобального стейта
        delay_ms_str = request.headers.get("X-Mock-Delay")
        delay_ms = int(delay_ms_str) if delay_ms_str and delay_ms_str.isdigit() else app_state.chaos_delay_ms
        
        if delay_ms > 0:
            await asyncio.sleep(delay_ms / 1000.0)
            
        # 2. Chaos Injection (Случайные или принудительные ошибки)
        # Проверяем заголовок X-Mock-Status, если он есть - принудительно отдаем ошибку
        forced_status = request.headers.get("X-Mock-Status")
        if forced_status and forced_status.isdigit():
            status_code = int(forced_status)
            return JSONResponse(
                content={"error": "Chaos Monkey injected forced error", "status": status_code},
                status_code=status_code
            )
            
        # Либо генерируем ошибку случайно по рейту
        if app_state.chaos_error_rate > 0.0:
            if random.random() < app_state.chaos_error_rate:
                status_code = random.choice(app_state.chaos_allowed_errors)
                return JSONResponse(
                    content={"error": "Chaos Monkey injected random error", "status": status_code},
                    status_code=status_code
                )
                
        # 3. Если хаос не сработал - пропускаем запрос к роутеру
        response = await call_next(request)
        return response
