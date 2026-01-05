from fastapi import status


def test_create_module_section(client):
    module = client.post("/api/modules", json={
        "name": "Algorithms",
        "code": "CS202",
        "program_id": 1,
        "semester": 2,
        "credits": 3
    }).json()

    payload = {
        "module_id": module["module_id"],
        "section_code": "A",
        "student_count": 50
    }

    response = client.post("/api/module-sections", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["section_code"] == "A"


def test_delete_module_section_blocked_if_tasks_exist(client):
    section = client.post("/api/module-sections", json={
        "module_id": 1,
        "section_code": "B",
        "student_count": 60
    }).json()

    client.post("/api/tasks", json={
        "title": "Lecture Section B",
        "module_section_id": section["section_id"],
        "category": "Teaching",
        "tariff_hours": 3,
        "required_qualification": "BSc"
    })

    response = client.delete(f"/api/module-sections/{section['section_id']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
