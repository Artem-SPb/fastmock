import re
from typing import Any, Dict, Optional, Tuple, Pattern

from fastmock.core.state import app_state

def path_to_regex(openapi_path: str) -> Pattern[str]:
    """Преобразует OpenAPI путь (/users/{id}) в регулярное выражение для матчинга."""
    # Заменяем {param} на захватывающую группу (?P<param>[^/]+)
    pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', openapi_path)
    return re.compile(f"^{pattern}$")

def find_operation(method: str, path: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Ищет операцию в загруженной спецификации по HTTP методу и пути.
    Возвращает (openapi_path_key, operation_dict).
    """
    if not app_state.spec or "paths" not in app_state.spec:
        return None, None

    method = method.lower()
    
    # Сначала пытаемся найти точное совпадение (без параметров)
    if path in app_state.spec["paths"]:
        op = app_state.spec["paths"][path].get(method)
        if op:
            return path, op
            
    # Если точного нет, ищем по шаблонам с {param}
    for spec_path, path_item in app_state.spec["paths"].items():
        if "{" in spec_path:
            regex = path_to_regex(spec_path)
            if regex.match(path):
                op = path_item.get(method)
                if op:
                    return spec_path, op
                    
    return None, None

def get_response_schema(operation: Dict[str, Any], status_code: str = "200") -> Optional[Dict[str, Any]]:
    """Извлекает JSON Schema для ответа с указанным кодом (по умолчанию 200)."""
    responses = operation.get("responses", {})
    response = responses.get(status_code) or responses.get(int(status_code)) or responses.get("default")
    
    if not response:
        return None
        
    content = response.get("content", {})
    json_content = content.get("application/json", {})
    return json_content.get("schema")
