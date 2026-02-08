import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity}" in data["message"]
    # Check participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_unregister_from_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Unregistered {email} from {activity}" in data["message"]
    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
