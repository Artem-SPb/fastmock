import pytest
from fastapi.testclient import TestClient
from fastmock.main import app
from fastmock.core.state import app_state

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_state():
    """Очищаем состояние перед каждым тестом."""
    app_state.clear_db()
    app_state.reset_chaos()
    app_state.spec = None
    yield

def test_admin_ping():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastMock API Engine" in response.json()["message"]

def test_upload_spec():
    # Мокаем спецификацию
    mock_spec = """
    openapi: 3.0.0
    info:
      title: Test API
      version: 1.0.0
    paths:
      /users:
        get:
          responses:
            '200':
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
    """
    response = client.post(
        "/_admin/specs", 
        files={"file": ("openapi.yaml", mock_spec.encode("utf-8"), "application/x-yaml")}
    )
    assert response.status_code == 200
    assert "Test API" in response.json()["message"]

    # Проверяем, что роут появился
    routes_resp = client.get("/_admin/routes")
    assert "GET /users" in routes_resp.json()["routes"]

    # Вызываем мок-роут
    mock_resp = client.get("/users")
    assert mock_resp.status_code == 200
    # Генератор должен был создать массив пользователей
    assert isinstance(mock_resp.json(), list)
    
def test_chaos_middleware_delay():
    # Задаем задержку через админку
    client.put("/_admin/config", json={"chaos_delay_ms": 100, "chaos_error_rate": 0, "chaos_allowed_errors": []})
    
    import time
    start = time.time()
    client.get("/") # Корневой путь пропускает хаос, так что проверим на /fake
    client.get("/fake")
    end = time.time()
    
    assert (end - start) >= 0.1
