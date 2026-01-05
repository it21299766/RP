from fastapi import status


def test_create_tariff(client):
    payload = {
        "task_type": "LECTURE",
        "category": "TEACHING",
        "hours": 2,
        "per_unit": "PER_SECTION"
    }

    response = client.post("/api/tariffs", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["hours"] == 2


def test_update_tariff(client):
    tariff = client.post("/api/tariffs", json={
        "task_type": "LAB",
        "category": "TEACHING",
        "hours": 3,
        "per_unit": "PER_SECTION"
    }).json()

    response = client.put(
        f"/api/tariffs/{tariff['tariff_id']}",
        json={"hours": 4}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["hours"] == 4


def test_delete_tariff(client):
    tariff = client.post("/api/tariffs", json={
        "task_type": "MARKING",
        "category": "ASSESSMENT",
        "hours": 5,
        "per_unit": "PER_50_STUDENTS"
    }).json()

    response = client.delete(f"/api/tariffs/{tariff['tariff_id']}")
    assert response.status_code == status.HTTP_200_OK
