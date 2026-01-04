import pytest
from fastapi import status


def test_create_staff_success(client):
    payload = {
        "name": "Dr. Alice",
        "qualification": "PhD",
        "specialty": "Computer Science",
        "department": "CS",
        "role": "ACADEMIC",
        "max_hours": 12,
        "skills": ["Python", "AI"],
        "experience": 5
    }

    response = client.post("/api/staff", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Dr. Alice"
    assert data["qualification"] == "PhD"


def test_create_staff_invalid_qualification(client):
    payload = {
        "name": "Bob",
        "qualification": "Diploma",
        "specialty": "IT",
        "department": "IT",
        "role": "ACADEMIC",
        "max_hours": 10
    }

    response = client.post("/api/staff", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_staff_list(client):
    response = client.get("/api/staff")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_update_staff(client):
    create = client.post("/api/staff", json={
        "name": "Temp",
        "qualification": "MSc",
        "specialty": "SE",
        "department": "SE",
        "role": "ACADEMIC",
        "max_hours": 8
    })

    staff_id = create.json()["staff_id"]

    update = client.put(f"/api/staff/{staff_id}", json={
        "max_hours": 10,
        "available": False
    })

    assert update.status_code == status.HTTP_200_OK
    assert update.json()["available"] is False


def test_delete_staff(client):
    create = client.post("/api/staff", json={
        "name": "Delete Me",
        "qualification": "BSc",
        "specialty": "IT",
        "department": "IT",
        "role": "ACADEMIC",
        "max_hours": 6
    })

    staff_id = create.json()["staff_id"]
    delete = client.delete(f"/api/staff/{staff_id}")
    assert delete.status_code == status.HTTP_200_OK
