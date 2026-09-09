<div align="right">
  <a href="README_RU.md">🇷🇺 Русский</a> | <b>🇬🇧 English</b>
</div>

# ⚡ FastMock API Engine

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)

**FastMock** is a lightweight, local Mock server built on FastAPI. It's designed for frontend and mobile developers who need a reliable, realistic REST API instantly, without waiting for the backend team.

![FastMock Preview](docs/assets/preview.png) *(You can place the generated image here)*

## 🚀 Features at a glance
1. **Dynamic OpenAPI Ingestion**: Drop your `openapi.yaml` in the folder or upload via Admin API. The endpoints are generated on the fly.
2. **Realistic Payload Generation**: Automatically generates realistic data (names, emails, UUIDs, dates) based on JSON Schema types using `Faker`.
3. **In-Memory CRUD**: Remembers what you `POST` and returns it on `GET`.
4. **Chaos Engineering**: Simulate slow 3G networks or random server crashes (HTTP 500, 503) globally or per-request using HTTP headers.

## 📖 Detailed Documentation
For deep-dive instructions, check the full usage guide:
👉 **[Read the Full Documentation (English)](docs/USAGE_EN.md)**

## 🛠 Quick Start (Docker)

The easiest way to run FastMock is via Docker.

1. Clone the repository:
```bash
git clone https://github.com/Artem-SPb/fastmock.git
cd fastmock
```
2. Place your `openapi.yaml` in the root directory (optional).
3. Run the container:
```bash
docker compose up
```
4. Open **http://127.0.0.1:8000/docs** in your browser!

## 👨‍💻 Author
**Artem-SPb** 
- GitHub: [@Artem-SPb](https://github.com/Artem-SPb)

Created as a portfolio project showcasing modern Python architecture, FastAPI ecosystem, and Developer Experience (DX) best practices.

*Feel free to star ⭐ this repository if you found it helpful!*
