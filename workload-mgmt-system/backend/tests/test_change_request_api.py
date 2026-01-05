from fastapi import status


def test_create_change_request(client):
    payload = {
        "assignment_id": 1,
        "requested_by_staff_id": 1,
        "reason": "Overloaded during exam week"
    }

    response = client.post("/api/change-requests", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "PENDING"


def test_admin_approves_change_request(client):
    request = client.post("/api/change-requests", json={
        "assignment_id": 1,
        "requested_by_staff_id": 1,
        "reason": "Specialty mismatch"
    }).json()

    response = client.put(
        f"/api/change-requests/{request['request_id']}/approve",
        json={"admin_comment": "Approved"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "APPROVED"
