from fastapi import status


def test_create_program_section(client):
    program = client.post("/api/programs", json={
        "name": "Computer Science",
        "code": "CS",
        "domain_id": 1
    }).json()

    payload = {
        "program_id": program["program_id"],
        "section_code": "A",
        "student_count": 120,
        "academic_year": "2024/2025"
    }

    response = client.post("/api/program-sections", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["section_code"] == "A"


def test_delete_program_section_blocked_if_modules_exist(client):
    section = client.post("/api/program-sections", json={
        "program_id": 1,
        "section_code": "B",
        "student_count": 100,
        "academic_year": "2024/2025"
    }).json()

    client.post("/api/modules", json={
        "name": "Operating Systems",
        "code": "CS303",
        "program_id": 1,
        "semester": 3,
        "credits": 3,
        "program_section_id": section["section_id"]
    })

    response = client.delete(f"/api/program-sections/{section['section_id']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
