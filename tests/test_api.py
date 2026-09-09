import pytest
from fastapi.testclient import TestClient

from fastmock.core.state import app_state
from fastmock.main import app

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
    # Настраиваем задержку
    client.put("/_admin/config", json={"chaos_delay_ms": 100, "chaos_error_rate": 0, "chaos_allowed_errors": []})
    
    import time
    start = time.time()
    client.get("/")
    end = time.time()
    
    assert (end - start) >= 0.1

def test_websockets():
    with client.websocket_connect("/ws/test") as websocket:
        # Тестируем эхо
        websocket.send_json({"message": "hello"})
        data = websocket.receive_json()
        assert "echo" in data
        assert data["echo"]["message"] == "hello"

        # Тестируем стриминг
        websocket.send_json({"action": "stream", "interval": 0.1})
        response = websocket.receive_json()
        assert response["status"] == "streaming_started"
        
        # Ловим первый пакет данных
        stream_data = websocket.receive_json()
        assert stream_data["event"] == "update"
        assert stream_data["path"] == "/test"
        
        # Останавливаем стриминг
        websocket.send_json({"action": "stop"})
        response = websocket.receive_json()
        assert response["status"] == "streaming_stopped"

def test_crud_operations():
    # Загружаем простую схему, чтобы роутер пропускал запросы
    mock_spec = """
    openapi: 3.0.0
    info:
      title: CRUD API
      version: 1.0.0
    paths:
      /items:
        post:
          responses:
            '201':
              content:
                application/json:
                  schema:
                    type: object
        get:
          responses:
            '200':
              content:
                application/json:
                  schema:
                    type: array
      /items/{id}:
        delete:
          responses:
            '200':
              content:
                application/json:
                  schema:
                    type: object
    """
    client.post("/_admin/specs", files={"file": ("openapi.yaml", mock_spec.encode("utf-8"), "application/x-yaml")})

    # 1. POST (Create)
    post_resp = client.post("/items", json={"name": "Item 1", "price": 100})
    assert post_resp.status_code == 201
    item_id = post_resp.json().get("id")
    assert item_id is not None

    # 2. GET (Read)
    get_resp = client.get("/items")
    assert get_resp.status_code == 200
    items = get_resp.json()
    assert isinstance(items, list)
    # FastMock мог сгенерировать фейковые данные помимо нашего POST-а, но наш элемент должен там быть
    assert any(i.get("id") == item_id for i in items)

    # 3. DELETE (Delete)
    del_resp = client.delete(f"/items/{item_id}")
    assert del_resp.status_code == 200

    # Проверяем, что удалилось
    get_resp_after = client.get("/items")
    items_after = get_resp_after.json()
    assert not any(i.get("id") == item_id for i in items_after)
