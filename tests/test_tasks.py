import os
import pytest
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

os.environ["DATABASE_URL"] = "sqlite:///./test_minitasks.db"

from app.main import app  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    # Apaga o arquivo do banco de testes
    db_file = "test_minitasks.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    # Roda migrations no banco de testes
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield



def test_create_task_ok():
    resp = client.post("/tasks/", json={
        "title": "Teste",
        "description": "Criar task"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Teste"
    assert data["description"] == "Criar task"
    assert data["done"] is False
    assert "created_at" in data


def test_list_tasks_pagination():
    # cria 2
    client.post("/tasks/", json={"title": "A", "description": None})
    client.post("/tasks/", json={"title": "B", "description": None})

    resp = client.get("/tasks/?limit=1&offset=0")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "A"

    resp2 = client.get("/tasks/?limit=1&offset=1")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert len(data2) == 1
    assert data2[0]["title"] == "B"


def test_get_task_by_id_ok():
    created = client.post("/tasks/", json={"title": "X", "description": "Y"}).json()
    task_id = created["id"]

    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == task_id
    assert data["title"] == "X"


def test_update_task_done_ok():
    created = client.post("/tasks/", json={"title": "X", "description": None}).json()
    task_id = created["id"]

    resp = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["done"] is True


def test_delete_task_ok():
    created = client.post("/tasks/", json={"title": "X", "description": None}).json()
    task_id = created["id"]

    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204

    # agora não existe mais -> 404 padronizado
    resp2 = client.get(f"/tasks/{task_id}")
    assert resp2.status_code == 404
    body = resp2.json()
    assert "error" in body
    assert body["error"]["type"] == "not_found"


def test_extra_fields_forbidden_on_create():
    resp = client.post("/tasks/", json={
        "title": "Teste",
        "description": "ok",
        "foo": "bar"
    })
    assert resp.status_code == 422


def test_not_found_uses_standard_error_shape():
    resp = client.get("/tasks/999999")
    assert resp.status_code == 404
    data = resp.json()
    assert "error" in data
    assert data["error"]["type"] == "not_found"
    assert "path" in data["error"]
