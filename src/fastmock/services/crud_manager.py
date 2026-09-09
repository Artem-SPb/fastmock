import uuid
from typing import Any, Dict, Optional, Tuple

from fastmock.core.state import app_state

def _get_collection_and_id(path: str) -> Tuple[str, Optional[str]]:
    """Эвристика: разбиваем путь на коллекцию и ID (например, /users/123 -> users, 123)."""
    parts = [p for p in path.split("/") if p]
    if not parts:
        return "root", None
        
    if len(parts) % 2 == 0:
        # Четное количество частей: /users/123 -> collection="users", id="123"
        return parts[-2], parts[-1]
    else:
        # Нечетное количество: /users -> collection="users", id=None
        return parts[-1], None

def save_data(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Сохраняет данные из POST/PUT в In-Memory БД."""
    collection, item_id = _get_collection_and_id(path)
    
    if collection not in app_state.db:
        app_state.db[collection] = {}
        
    # Генерируем ID если его нет и это добавление в коллекцию
    if not item_id:
        item_id = str(data.get("id", uuid.uuid4()))
        data["id"] = item_id
        
    app_state.db[collection][item_id] = data
    app_state.save_db()
    return data

def delete_data(path: str) -> bool:
    """Удаляет данные из In-Memory БД (для DELETE запросов)."""
    collection, item_id = _get_collection_and_id(path)
    if collection in app_state.db and item_id in app_state.db[collection]:
        del app_state.db[collection][item_id]
        app_state.save_db()
        return True
    return False

def get_data(path: str) -> Optional[Any]:
    """Ищет данные в In-Memory БД (для GET запросов)."""
    collection, item_id = _get_collection_and_id(path)
    
    if collection not in app_state.db:
        return None
        
    if item_id:
        # Запрос конкретного элемента
        return app_state.db[collection].get(item_id)
    else:
        # Запрос списка
        return list(app_state.db[collection].values())
