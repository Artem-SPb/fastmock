from typing import Any, Dict

class AppState:
    def __init__(self) -> None:
        # Глобальная спецификация (разобранная)
        self.spec: Dict[str, Any] | None = None
        
        # In-Memory база данных: словарь словарей для базового CRUD
        # Пример: {"users": {"1": {"id": "1", "name": "Test"}}}
        self.db: Dict[str, Dict[str, Any]] = {}
        
        # Глобальные настройки хаоса
        self.chaos_delay_ms: int = 0
        self.chaos_error_rate: float = 0.0
        self.chaos_allowed_errors: list[int] = [500, 502, 503]

    def clear_db(self) -> None:
        """Очищает In-Memory базу данных."""
        self.db = {}

    def reset_chaos(self) -> None:
        """Сбрасывает настройки хаоса по умолчанию."""
        self.chaos_delay_ms = 0
        self.chaos_error_rate = 0.0

# Глобальный singleton-объект состояния
app_state = AppState()
