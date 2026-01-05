from fastapi import status


def test_create_task_success(client):
    payload = {
        "title": "CS101 Lecture",
        "category": "Teaching",
        "department": "CS",
        "required_specialty": "Computer Science",
        "required_qualification": "MSc",
        "tariff_hours": 3,
        "required_skills": ["Python"],
        "required_experience": 1
    }

    response = client.post("/api/tasks", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "CS101 Lecture"


def test_create_task_invalid_category(client):
    payload = {
        "title": "Invalid",
        "category": "Sports",
        "required_qualification": "BSc",
        "tariff_hours": 1
    }

    response = client.post("/api/tasks", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_all_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_update_task(client):
    create = client.post("/api/tasks", json={
        "title": "Lab",
        "category": "Teaching",
        "department": "IT",
        "required_specialty": "IT",
        "required_qualification": "BSc",
        "tariff_hours": 2
    })

    task_id = create.json()["task_id"]

    update = client.put(f"/api/tasks/{task_id}", json={
        "tariff_hours": 3
    })

    assert update.status_code == status.HTTP_200_OK
    assert update.json()["tariff_hours"] == 3


def test_delete_task(client):
    create = client.post("/api/tasks", json={
        "title": "Delete Me",
        "category": "Admin",
        "required_qualification": "BSc",
        "tariff_hours": 1
    })

    task_id = create.json()["task_id"]
    delete = client.delete(f"/api/tasks/{task_id}")
    assert delete.status_code == status.HTTP_200_OK
