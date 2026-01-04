from fastapi import status


def test_update_assignment_status(client):
    assignment = client.post("/api/assignments", json={
        "staff_id": 1,
        "task_id": 1
    }).json()

    response = client.put(
        f"/api/assignments/{assignment['assignment_id']}",
        json={"status": "completed"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "completed"


def test_delete_assignment_success(client):
    assignment = client.post("/api/assignments", json={
        "staff_id": 1,
        "task_id": 1
    }).json()

    response = client.delete(f"/api/assignments/{assignment['assignment_id']}")
    assert response.status_code == status.HTTP_200_OK


def test_delete_completed_assignment_blocked(client):
    assignment = client.post("/api/assignments", json={
        "staff_id": 1,
        "task_id": 1
    }).json()

    client.put(
        f"/api/assignments/{assignment['assignment_id']}",
        json={"status": "completed"}
    )

    response = client.delete(f"/api/assignments/{assignment['assignment_id']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
