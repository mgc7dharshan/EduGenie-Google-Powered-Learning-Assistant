from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["service"] == "EduGenie"


def test_empty_question():

    response = client.post(
        "/qa",
        json={
            "input": ""
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "Please enter a question"
        in data["result"]
    )