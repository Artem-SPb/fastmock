import json
import os
from typing import Any

from fastmock.core.config import settings


class AppState:
    def __init__(self) -> None:
        self.spec: dict[str, Any] | None = None
        self.db: dict[str, dict[str, Any]] = {}
        
        self.chaos_delay_ms: int = 0
        self.chaos_error_rate: float = 0.0
        self.chaos_allowed_errors: list[int] = [500, 502, 503]

    def clear_db(self) -> None:
        self.db = {}
        self.save_db()

    def reset_chaos(self) -> None:
        self.chaos_delay_ms = 0
        self.chaos_error_rate = 0.0

    def load_db(self):
        if settings.persist_path and os.path.exists(settings.persist_path):
            try:
                with open(settings.persist_path, "r", encoding="utf-8") as f:
                    self.db = json.load(f)
                print(f"[*] Loaded database state from {settings.persist_path}")
            except Exception as e:
                print(f"[!] Failed to load database state: {e}")

    def save_db(self):
        if settings.persist_path:
            try:
                with open(settings.persist_path, "w", encoding="utf-8") as f:
                    json.dump(self.db, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[!] Failed to save database state: {e}")

app_state = AppState()
