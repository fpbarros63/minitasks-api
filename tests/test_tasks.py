import pytest


def create_task(client, title="Task A", description="Desc A"):
    payload = {"title": title, "description": description}
    res = client.post("/tasks", json=payload)
    assert res.status_code == 201
    return res.json()


def test_create_task_success(client):
    task = create_task(client, "Study ML", "Twice a week")
    assert task["id"] == 1
    assert task["title"] == "Study ML"
    assert task["description"] == "Twice a week"
    assert task["done"] is False


def test_create_task_validation_error_empty_title(client):
    res = client.post("/tasks", json={"title": "", "description": "x"})
    assert res.status_code == 422


def test_get_task_by_id_success(client):
    created = create_task(client, "Task One", "First")
    task_id = created["id"]

    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == task_id
    assert body["title"] == "Task One"


def test_get_task_by_id_not_found(client):
    res = client.get("/tasks/9999")
    assert res.status_code == 404


def test_patch_task_done_success(client):
    created = create_task(client, "Task Patch", "Patch desc")
    task_id = created["id"]

    res = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    body = res.json()
    assert body["done"] is True


def test_patch_task_not_found(client):
    res = client.patch("/tasks/9999", json={"done": True})
    assert res.status_code == 404


def test_delete_task_success(client):
    created = create_task(client, "Task Del", "Del desc")
    task_id = created["id"]

    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 204

    # não existe mais
    res2 = client.get(f"/tasks/{task_id}")
    assert res2.status_code == 404


def test_list_tasks_pagination_limit_offset(client):
    create_task(client, "T1", "D1")
    create_task(client, "T2", "D2")
    create_task(client, "T3", "D3")

    res = client.get("/tasks?limit=2&offset=0")
    assert res.status_code == 200
    body = res.json()

    assert body["total"] == 3
    assert body["limit"] == 2
    assert body["offset"] == 0
    assert len(body["items"]) == 2
    assert body["items"][0]["title"] == "T1"
    assert body["items"][1]["title"] == "T2"

    res2 = client.get("/tasks?limit=2&offset=2")
    assert res2.status_code == 200
    body2 = res2.json()

    assert body2["total"] == 3
    assert len(body2["items"]) == 1
    assert body2["items"][0]["title"] == "T3"


def test_list_tasks_filter_done(client):
    t1 = create_task(client, "Done 1", "x")
    create_task(client, "Pending 1", "y")
    create_task(client, "Pending 2", "z")

    # marca um como done
    res = client.patch(f"/tasks/{t1['id']}", json={"done": True})
    assert res.status_code == 200

    # filtra done=true
    res_done = client.get("/tasks?done=true&limit=50&offset=0")
    assert res_done.status_code == 200
    b_done = res_done.json()

    assert b_done["total"] == 1
    assert len(b_done["items"]) == 1
    assert b_done["items"][0]["title"] == "Done 1"

    # filtra done=false
    res_pending = client.get("/tasks?done=false&limit=50&offset=0")
    assert res_pending.status_code == 200
    b_pending = res_pending.json()

    assert b_pending["total"] == 2
    assert len(b_pending["items"]) == 2
    titles = [x["title"] for x in b_pending["items"]]
    assert "Pending 1" in titles
    assert "Pending 2" in titles
