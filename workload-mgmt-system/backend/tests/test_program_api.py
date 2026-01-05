from fastapi import status


def test_create_program(client):
    domain = client.post("/api/domains", json={
        "name": "Teaching",
        "description": "Teaching workload"
    })

    domain_id = domain.json()["domain_id"]

    payload = {
        "name": "BSc Computer Science",
        "code": "CS101",
        "domain_id": domain_id
    }

    response = client.post("/api/programs", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["code"] == "CS101"


def test_get_programs(client):
    response = client.get("/api/programs")
    assert response.status_code == status.HTTP_200_OK
