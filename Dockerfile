FROM python:3.12-slim

WORKDIR /app

# Отключаем создание байт-кода и буферизацию
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка зависимостей (используем pip, так как pyproject.toml поддерживает PEP 621)
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

# Ожидается, что пользователь примонтирует openapi.yaml в /app/openapi.yaml
# или загрузит его через API
EXPOSE 8000

CMD ["fastmock"]
