from fastapi import status


def test_run_optimization(client):
    response = client.post("/api/optimization/run", json={
        "semester": "2024_S1",
        "department": "CS"
    })

    assert response.status_code == status.HTTP_200_OK
    assert "assignments" in response.json()
    assert "summary" in response.json()
