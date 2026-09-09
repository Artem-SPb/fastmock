from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from fastmock.core.state import app_state
from fastmock.services import openapi_parser, data_generator, crud_manager

router = APIRouter()

@router.api_route(
    "/{path:path}", 
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    summary="Dynamic Mock Router | Динамический генератор ответов",
    description="**EN:** Catch-all endpoint that intercepts requests and responds with generated mock data based on the uploaded OpenAPI spec.\n\n**RU:** Эндпоинт, который перехватывает все запросы и отвечает сгенерированными мок-данными на основе загруженной OpenAPI спецификации."
)
async def catch_all(request: Request, path: str):
    # Добавляем слэш в начале
    full_path = f"/{path}"
    
    # 1. Если спеки нет, отдаем ошибку
    if not app_state.spec:
        raise HTTPException(
            status_code=400, 
            detail="OpenAPI spec not loaded. Use POST /_admin/specs to upload or provide openapi.yaml."
        )
        
    # 2. Ищем операцию в спеке
    spec_path, operation = openapi_parser.find_operation(request.method, full_path)
    
    if not operation:
        raise HTTPException(
            status_code=404, 
            detail=f"Path {full_path} not found in OpenAPI spec for method {request.method}."
        )
        
    # 3. Эвристика сохранения (CRUD) для POST/PUT/PATCH
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
            if isinstance(body, dict):
                saved_data = crud_manager.save_data(full_path, body)
                # Возвращаем сохраненные данные, чтобы симулировать успешное создание
                return JSONResponse(
                    content=saved_data, 
                    status_code=201 if request.method == "POST" else 200
                )
        except Exception:
            pass # Если тело не JSON или не распарсилось, генерируем мок по схеме
            
    # 4. Поиск сохраненных данных для GET
    if request.method == "GET":
        saved_data = crud_manager.get_data(full_path)
        if saved_data:
            # Отдаем сохраненные данные только если они есть (если список пуст - сгенерируем фикстуры)
            if not isinstance(saved_data, list) or len(saved_data) > 0:
                return JSONResponse(content=saved_data, status_code=200)

    # 5. Если данных нет - генерируем фиктивные данные по схеме ответа
    schema = openapi_parser.get_response_schema(operation, status_code="200")
    status_code = 200
    
    if not schema:
        # Если схемы для 200 нет, пробуем 201 (для POST)
        schema = openapi_parser.get_response_schema(operation, status_code="201")
        status_code = 201 if schema else 200
        
    if schema:
        mock_data = data_generator.generate_mock_data(schema)
        # Опционально: можно сохранить сгенерированные списки, чтобы они не менялись каждый раз
        if request.method == "GET" and isinstance(mock_data, list):
            for item in mock_data:
                if isinstance(item, dict):
                    crud_manager.save_data(full_path, item)
                    
        return JSONResponse(content=mock_data, status_code=status_code)
        
    return JSONResponse(
        content={"message": "Mock response generated, but no JSON schema found in OpenAPI."}, 
        status_code=status_code
    )
