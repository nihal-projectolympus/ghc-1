from src.app import activities


def test_unregister_existing_student_returns_success_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}


def test_unregister_existing_student_removes_from_activities(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.get("/activities")

    # Assert
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.signed.up@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_after_signup_restores_original_participants(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original = list(activities[activity_name]["participants"])
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert activities[activity_name]["participants"] == original
