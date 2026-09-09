<div align="right">
  <a href="README_RU.md">🇷🇺 Русский</a> | <b>🇬🇧 English</b>
</div>

# ⚡ FastMock API Engine

[![PyPI version](https://img.shields.io/pypi/v/fastmock-api.svg)](https://pypi.org/project/fastmock-api/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Build Status](https://github.com/Artem-SPb/fastmock/actions/workflows/ci.yml/badge.svg)](https://github.com/Artem-SPb/fastmock/actions)

**FastMock** is a lightweight, local Mock server built on FastAPI. It's designed for frontend and mobile developers who need a reliable, realistic REST API instantly, without waiting for the backend team.

![FastMock Preview](docs/assets/preview.png) *(You can place the generated image here)*

## 🚀 Quick Start

### Option 1: Install via pip (Recommended)
```bash
pip install fastmock-api
fastmock --port 8080
```

> ⚠️ **Important Note for Windows Users:** The console might say `Uvicorn running on http://0.0.0.0:8080`. This means the server is accessible on your local network. However, Windows browsers **cannot** open `0.0.0.0` directly. Please use **[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)** instead.

### Option 2: Run via Docker
```bash
git clone https://github.com/Artem-SPb/fastmock.git
cd fastmock
docker compose up
```
Open **http://127.0.0.1:8000/docs** in your browser.

## 👨‍💻 Author
**Artem-SPb** 
- GitHub: [@Artem-SPb](https://github.com/Artem-SPb)

Created as a portfolio project showcasing modern Python architecture, FastAPI ecosystem, and Developer Experience (DX) best practices.

*Feel free to star ⭐ this repository if you found it helpful!*
