import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure user is not signed up
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code in (200, 404)  # 404 if not present

    # Sign up user
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    # Print participants after signup
    activities_resp = client.get("/activities")
    print("Participants after signup:", activities_resp.json()[activity]["participants"])

    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

    # Print participants before unregister
    activities_resp = client.get("/activities")
    print("Participants before unregister:", activities_resp.json()[activity]["participants"])

    # Unregister user
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    print("Unregister response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    # Unregister again (should fail)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404
