from fastapi.testclient import TestClient

from main import Task, app, tasks

client = TestClient(app)


def setup_function():
    tasks[:] = [
        Task(id=1, title="Learn HTTP basics", done=True),
        Task(id=2, title="Build a CRUD API", done=False),
        Task(id=3, title="Test with Swagger UI", done=False),
    ]


def test_root_health_and_docs():
    assert client.get("/").json()["name"] == "Task API"
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200


def test_full_crud_cycle_and_errors():
    assert client.get("/tasks").status_code == 200
    assert client.get("/tasks/1").json()["id"] == 1
    missing = client.get("/tasks/99")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Task 99 not found"

    invalid = client.post("/tasks", json={})
    assert invalid.status_code == 400
    created = client.post("/tasks", json={"title": "Buy milk"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    updated = client.put(f"/tasks/{task_id}", json={"done": True})
    assert updated.status_code == 200
    assert updated.json()["done"] is True
    assert client.put(f"/tasks/{task_id}", json={}).status_code == 400

    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404
    assert client.delete("/tasks/99").status_code == 404
