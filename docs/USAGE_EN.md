# FastMock: Detailed Usage Guide

Welcome to the FastMock API Engine documentation. This guide explains how to leverage all the features of the mock server.

## 1. Loading your Specification (OpenAPI)

FastMock is driven by your OpenAPI 3.0/3.1 specification. 
There are two ways to feed your spec to the server:

### Method A: Auto-load on Startup
Place a file named `openapi.yaml` in the root folder of the project. When you run `docker compose up` or the `fastmock` CLI command, the server will automatically detect it and generate endpoints.

> 💡 **Quick Test:** The repository includes a ready-to-use `openapi.example.yaml`. To quickly test the engine, just copy it:
> ```bash
> cp openapi.example.yaml openapi.yaml
> ```
> Then restart the server. You'll instantly get working `/users` and `/products` endpoints.

### Method B: Hot-Reload via Admin API
If the server is already running, you can upload a new spec without restarting:
1. Open the Swagger UI: `http://127.0.0.1:8000/docs`
2. Find the `POST /_admin/specs` endpoint.
3. Upload your YAML or JSON file.

---

## 2. Smart Data Generation (Faker)

If your OpenAPI specification doesn't explicitly provide an `example` for a field, FastMock will generate realistic data based on field types and names.

**How does it guess?**
* **By format:** `uuid` -> valid UUIDv4, `email` -> random email address, `date-time` -> ISO8601 timestamp.
* **By field name:** If a field is named `first_name`, it generates a real human name. If it's `phone`, it generates a phone number.
* **By base type:** `string` -> random word, `integer` -> number between 1-100, `array` -> array of 1-3 items.

---

## 3. Stateful Responses (In-Memory CRUD)

FastMock can remember data during a session.
For example, if your spec has `POST /users` and `GET /users`:

1. Send a `POST /users` request with a JSON body.
2. FastMock will generate an `id` for it (if missing) and save it in memory.
3. Send a `GET /users` request, and you will receive an array containing the user you just created!

> **Note:** Data is stored in RAM (In-Memory) and will be lost on server restart. You can manually clear the database by calling `DELETE /_admin/state`.

---

## 4. Network Simulation (Chaos Engineering)

Frontend and mobile applications need to handle poor network conditions and backend failures gracefully. FastMock allows you to simulate this easily.

### Header-based Simulation (Per-Request)
You can inject chaos into specific requests by adding custom headers from your client:
* `X-Mock-Delay: 2000` — Delays the response by exactly 2 seconds (2000 ms).
* `X-Mock-Status: 503` — Forces the server to return a 503 Service Unavailable error.

### Global Simulation (Admin API)
You can enable chaos globally for *all* requests via the Swagger UI (`PUT /_admin/config`):
```json
{
  "chaos_delay_ms": 1500,
  "chaos_error_rate": 0.2,
  "chaos_allowed_errors": [500, 502, 503]
}
```
*In this example: every request will be delayed by 1.5 seconds, and 20% of requests will randomly fail with a 500, 502, or 503 status code.*
