# API Health Dashboard — Backend

## About

**API Health Dashboard** is a small developer-focused tool for tracking internal service health, ownership, and response times. Users can add services with endpoint URLs, run health checks, and see whether each service is healthy, degraded, or down. The dashboard can show last checked time, response latency, owner, notes, and simple stats across all services.

This directory contains the **FastAPI** backend. The frontend (Vue) will live in a sibling directory.

## Stack

- **FastAPI** — HTTP API
- **SQLModel** — ORM + Pydantic schemas in one
- **SQLite** — local dev database (`health.db`, auto-created on startup)
- **uvicorn** — ASGI server
- **uv** — dependency / venv manager
- **httpx** — outbound HTTP for health probes
- **pytest** — tests

## Prerequisites

- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) installed

## Setup

```bash
cd backend
uv sync          # creates .venv and installs deps from uv.lock
```

## Running the dev server

```bash
uv run uvicorn main:app --reload
```

Server runs on `http://127.0.0.1:8000`. Interactive API docs at `http://127.0.0.1:8000/docs`.

Breakdown:
- `uv run` — execute the command inside the project's virtualenv
- `uvicorn` — the ASGI server
- `main:app` — load the `app` object from `main.py`
- `--reload` — restart on file changes (dev only)

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/services` | List all registered services |
| `POST` | `/services` | Register a new service |

### Status values

`status` is accepted and returned as a **string** at the API boundary, but stored as an **int** in the database:

| String | Int |
| --- | --- |
| `pending` | 0 |
| `healthy` | 1 |
| `degraded` | 2 |
| `down` | 3 |

### Example

```bash
# create
curl -X POST localhost:8000/services \
  -H 'Content-Type: application/json' \
  -d '{"name":"api","url":"https://example.com","status":"healthy"}'

# list
curl localhost:8000/services
```

## Project layout

```
backend/
  main.py        # FastAPI app + routes
  models.py     # SQLModel tables + Pydantic schemas + ServiceStatus enum
  database.py    # engine, session dependency, create_db()
  health.db      # SQLite file (gitignored, auto-created)
  pyproject.toml
  uv.lock
```

## Status

### Done
- Project scaffolding (uv, pyproject, SQLite engine)
- `Service` table model
- `ServiceCreate` / `ServiceRead` / `ServiceUpdate` schemas
- `ServiceStatus` enum with string-in / int-stored / string-out conversion
- `GET /services` and `POST /services` endpoints

### Pending
- `GET /services/{id}` — fetch a single service
- `PATCH /services/{id}` — wire up `ServiceUpdate`
- `DELETE /services/{id}`
- Health-check executor — actually probe each `url` with `httpx` and update `status`, `response_time`, `last_checked_at`
- Background scheduler to run health checks periodically
- Add `owner` and `notes` columns (mentioned in the project description, not yet modeled)
- Aggregate stats endpoint (counts by status, average latency, etc.)
- Tests (pytest is installed but no tests yet)
- Replace deprecated `@app.on_event("startup")` with `lifespan` context manager
- Configure CORS for the Vue frontend
- Set SQLite `check_same_thread=False` on the engine for safe use under FastAPI's threadpool
- `updated_at` `onupdate` trigger so it actually bumps on updates
- Frontend (Vue) — separate directory, not started
```