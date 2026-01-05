from fastapi import status


def test_create_module_success(client):
    program = client.post("/api/programs", json={
        "name": "Computer Science",
        "code": "CS",
        "domain_id": 1
    }).json()

    payload = {
        "name": "Data Structures",
        "code": "CS201",
        "program_id": program["program_id"],
        "semester": 2,
        "credits": 3
    }

    response = client.post("/api/modules", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Data Structures"


def test_get_modules(client):
    response = client.get("/api/modules")
    assert response.status_code == status.HTTP_200_OK


def test_delete_module_blocked_when_tasks_exist(client):
    module = client.post("/api/modules", json={
        "name": "DB Systems",
        "code": "CS301",
        "program_id": 1,
        "semester": 3,
        "credits": 3
    }).json()

    client.post("/api/tasks", json={
        "title": "DB Lecture",
        "module_id": module["module_id"],
        "category": "Teaching",
        "required_qualification": "BSc",
        "tariff_hours": 3
    })

    response = client.delete(f"/api/modules/{module['module_id']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
