import copy

from fastapi.testclient import TestClient

from src.app import activities, app, normalize_email

client = TestClient(app)
BASE_ACTIVITIES = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(BASE_ACTIVITIES))


def test_get_activities_returns_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_adds_participant_with_normalized_email():
    # Arrange
    reset_activities()
    email = "  New.Student@Mergington.edu  "

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    normalized = normalize_email(email)
    assert normalized in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Signed up {normalized} for Chess Club"


def test_signup_rejects_duplicate_email_case_insensitive():
    # Arrange
    reset_activities()
    email = "ALEGICAL@gmail.com"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_missing_activity():
    # Arrange
    reset_activities()

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_when_activity_is_full():
    # Arrange
    reset_activities()
    activity = activities["Chess Club"]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "another@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is already full"


def test_unregister_removes_participant_case_insensitive():
    # Arrange
    reset_activities()
    email = "  ALEGICAL@GMAIL.COM  "

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    normalized = normalize_email(email)
    assert normalized not in {
        normalize_email(participant) for participant in activities["Chess Club"]["participants"]
    }
    assert response.json()["message"] == f"Removed {normalized} from Chess Club"


def test_unregister_rejects_missing_participant():
    # Arrange
    reset_activities()

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "missing@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
