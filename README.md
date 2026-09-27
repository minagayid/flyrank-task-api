# Task API

A small in-memory CRUD API built with Python and FastAPI for the FlyRank Backend Track Week 2 assignment. Data intentionally resets when the server restarts; there is no database or file storage.

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --reload
```

The API runs at <http://localhost:8000>. Interactive Swagger UI is at <http://localhost:8000/docs>.

## Endpoints

| Method | Path | Purpose | Success | Errors |
|---|---|---|---:|---|
| GET | `/` | Describe the API | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{id}` | Get one task | 200 | 404 |
| POST | `/tasks` | Create a task (`title` required) | 201 | 400 |
| PUT | `/tasks/{id}` | Update `title` and/or `done` | 200 | 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 |

## Example curl output

```text
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Learn HTTP basics","done":true}
```

## CRUD examples

```bash
curl -i -X POST http://localhost:8000/tasks -H 'Content-Type: application/json' -d '{"title":"Buy milk"}'
curl -i -X PUT http://localhost:8000/tasks/4 -H 'Content-Type: application/json' -d '{"done":true}'
curl -i -X DELETE http://localhost:8000/tasks/4
```

Invalid or empty titles return `400` with a JSON error. Unknown task IDs return `404` with a JSON error. The complete CRUD cycle can also be run from Swagger UI's **Try it out** controls.

## Tests

```bash
.venv/bin/pytest
```
