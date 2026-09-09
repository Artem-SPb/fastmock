from typing import Any, Dict
from faker import Faker

fake = Faker()

def generate_mock_data(schema: Dict[str, Any]) -> Any:
    """Генерирует фиктивные данные на основе JSON Schema."""
    if not schema:
        return None
        
    # Если есть example или default - отдаем его
    if "example" in schema:
        return schema["example"]
    if "default" in schema:
        return schema["default"]
        
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        properties = schema.get("properties", {})
        result = {}
        for prop_name, prop_schema in properties.items():
            result[prop_name] = generate_field(prop_name, prop_schema)
        return result
        
    elif schema_type == "array":
        items_schema = schema.get("items", {})
        # Генерируем от 1 до 3 элементов
        return [generate_mock_data(items_schema) for _ in range(fake.random_int(min=1, max=3))]
        
    else:
        return generate_field("unknown", schema)

def generate_field(name: str, schema: Dict[str, Any]) -> Any:
    """Генерирует значение для конкретного поля, учитывая его имя и формат."""
    
    if "example" in schema:
        return schema["example"]
        
    # Сначала проверяем формат (uuid, date-time, email)
    fmt = schema.get("format")
    if fmt == "uuid":
        return fake.uuid4()
    elif fmt == "email":
        return fake.email()
    elif fmt == "date-time":
        return fake.iso8601()
    elif fmt == "date":
        return fake.date()
        
    # Затем пытаемся угадать по имени поля
    name_lower = name.lower()
    if "name" in name_lower and "user" in name_lower:
        return fake.name()
    elif "first_name" in name_lower:
        return fake.first_name()
    elif "last_name" in name_lower:
        return fake.last_name()
    elif "phone" in name_lower:
        return fake.phone_number()
    elif "url" in name_lower or "link" in name_lower:
        return fake.url()
    elif "address" in name_lower:
        return fake.address()
    elif "id" in name_lower:
        return fake.uuid4() if schema.get("type") == "string" else fake.random_int(min=1, max=1000)
        
    # Если не угадали, генерируем просто по типу
    schema_type = schema.get("type", "string")
    if schema_type == "string":
        return fake.word()
    elif schema_type == "integer":
        return fake.random_int(min=1, max=100)
    elif schema_type == "number":
        return fake.pyfloat(positive=True, max_value=1000.0)
    elif schema_type == "boolean":
        return fake.boolean()
        
    return None
