import asyncio
import json

from faker import Faker
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
fake = Faker()

@router.websocket("/ws/{path:path}")
async def websocket_endpoint(websocket: WebSocket, path: str):
    """
    Универсальный WebSocket роутер для мокирования.
    Поддерживает:
    1. Эхо-сообщения
    2. Потоковую отдачу фейковых данных ({"action": "stream", "interval": 1})
    """
    await websocket.accept()
    
    streaming_task = None
    
    async def stream_data(interval: float):
        while True:
            try:
                # Генерируем случайные данные для потока
                mock_payload = {
                    "event": "update",
                    "path": f"/{path}",
                    "data": {
                        "id": fake.uuid4(),
                        "value": fake.pyfloat(min_value=10.0, max_value=1000.0, right_digits=2),
                        "timestamp": fake.iso8601()
                    }
                }
                await websocket.send_json(mock_payload)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception:
                break

    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                # Пытаемся распарсить как JSON для поиска команд
                json_data = json.loads(data)
                action = json_data.get("action")
                
                if action == "stream":
                    interval = float(json_data.get("interval", 1.0))
                    if streaming_task is None or streaming_task.done():
                        streaming_task = asyncio.create_task(stream_data(interval))
                        await websocket.send_json({"status": "streaming_started", "interval": interval})
                    else:
                        await websocket.send_json({"status": "already_streaming"})
                
                elif action == "stop":
                    if streaming_task and not streaming_task.done():
                        streaming_task.cancel()
                        streaming_task = None
                        await websocket.send_json({"status": "streaming_stopped"})
                else:
                    # Если это просто JSON, но не команда - делаем эхо
                    await websocket.send_json({"echo": json_data})
                    
            except json.JSONDecodeError:
                # Если пришел обычный текст - просто возвращаем его (эхо)
                await websocket.send_text(f"Echo: {data}")
                
    except WebSocketDisconnect:
        if streaming_task and not streaming_task.done():
            streaming_task.cancel()
