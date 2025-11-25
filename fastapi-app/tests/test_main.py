import os
import sys
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

# Ensure fastapi-app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fastapi-app")))

from app.api.dependencies import get_repository, get_todo_service  # noqa: E402
from app.domain.services import TodoService  # noqa: E402
from app.infrastructure.json_repository import JsonTodoRepository  # noqa: E402
from app.main import create_app  # noqa: E402


@pytest.fixture()
def test_client(tmp_path):
    app = create_app()
    storage = tmp_path / "todos.json"
    repository = JsonTodoRepository(storage)
    service = TodoService(repository)

    app.dependency_overrides[get_repository] = lambda: repository
    app.dependency_overrides[get_todo_service] = lambda: service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_get_todos_empty(test_client):
    response = test_client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_todo(test_client):
    create_response = test_client.post(
        "/todos",
        json={"title": "Read book", "description": "Read DDD chapter"},
    )
    assert create_response.status_code == 201
    body = create_response.json()
    assert body["title"] == "Read book"
    assert body["completed"] is False
    assert "id" in body
    assert datetime.fromisoformat(body["created_at"])  # raises if invalid

    todo_id = body["id"]
    fetch_response = test_client.get(f"/todos/{todo_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["id"] == todo_id


def test_update_todo_via_put(test_client):
    todo = test_client.post(
        "/todos",
        json={"title": "Write tests", "description": "Cover services"},
    ).json()

    response = test_client.put(
        f"/todos/{todo['id']}",
        json={"title": "Write more tests", "description": "Add edge cases"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Write more tests"
    assert data["description"] == "Add edge cases"


def test_patch_todo_completion(test_client):
    todo = test_client.post(
        "/todos",
        json={"title": "Ship feature", "description": "Demo REST API"},
    ).json()

    response = test_client.patch(
        f"/todos/{todo['id']}",
        json={"completed": True},
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_patch_requires_changes(test_client):
    todo = test_client.post(
        "/todos",
        json={"title": "Plan sprint", "description": "Discuss backlog"},
    ).json()

    response = test_client.patch(f"/todos/{todo['id']}", json={})
    assert response.status_code == 400


def test_delete_todo(test_client):
    todo = test_client.post(
        "/todos",
        json={"title": "Archive", "description": "Clean board"},
    ).json()

    delete_response = test_client.delete(f"/todos/{todo['id']}")
    assert delete_response.status_code == 204

    get_response = test_client.get(f"/todos/{todo['id']}")
    assert get_response.status_code == 404

