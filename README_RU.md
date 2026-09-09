<div align="right">
  <b>🇷🇺 Русский</b> | <a href="README.md">🇬🇧 English</a>
</div>

# ⚡ FastMock API Engine

[![PyPI version](https://img.shields.io/pypi/v/fastmock-api.svg)](https://pypi.org/project/fastmock-api/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Build Status](https://github.com/Artem-SPb/fastmock/actions/workflows/ci.yml/badge.svg)](https://github.com/Artem-SPb/fastmock/actions)

**FastMock** — это легковесный, локальный Mock-сервер на базе FastAPI. Он создан для фронтенд- и мобильных разработчиков, которым нужен работающий, реалистичный REST API "здесь и сейчас", без ожидания бэкенд-команды.

![FastMock Preview](docs/assets/preview.png) *(Здесь будет ваше превью)*

## 🚀 Ключевые возможности
1. **Динамическая загрузка OpenAPI**: Просто положите `openapi.yaml` в папку с проектом или загрузите через Admin API, и эндпоинты сгенерируются на лету.
2. **Реалистичная генерация данных**: Автоматически создает правдоподобные данные (имена, email, UUID, даты) на основе типов в JSON Schema с помощью библиотеки `Faker`.
3. **In-Memory CRUD**: Запоминает данные, которые вы отправляете через `POST`, и возвращает их при `GET` запросах.
4. **Chaos Engineering**: Симулируйте медленные 3G-сети или случайные падения сервера (HTTP 500, 503) глобально или для конкретных запросов через HTTP-заголовки.

## 📖 Подробная документация
Для глубокого погружения и примеров изучите полную инструкцию:
👉 **[Читать полную документацию (на русском)](docs/USAGE_RU.md)**

## 🛠 Быстрый старт (Docker)

Самый простой способ запустить FastMock — использовать Docker.

1. Склонируйте репозиторий:
```bash
git clone https://github.com/Artem-SPb/fastmock.git
cd fastmock
```
2. Положите вашу спецификацию `openapi.yaml` в корень проекта (необязательно).
3. Запустите контейнер:
```bash
docker compose up
```
4. Откройте **http://127.0.0.1:8000/docs** в вашем браузере!

## 👨‍💻 Автор
**Artem-SPb** 
- GitHub: [@Artem-SPb](https://github.com/Artem-SPb)

Создано в качестве портфолио-проекта, демонстрирующего современную архитектуру на Python, работу с экосистемой FastAPI и фокус на Developer Experience (DX).

*Если проект оказался полезным, не забудьте поставить звездочку ⭐!*
