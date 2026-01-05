from fastapi import status


def test_create_domain(client):
    payload = {
        "name": "Teaching",
        "description": "Teaching related workload"
    }

    response = client.post("/api/domains", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Teaching"


def test_get_domains(client):
    response = client.get("/api/domains")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
