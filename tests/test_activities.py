def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 9
    assert "Chess Club" in data
    assert set(data["Chess Club"]) == expected_fields


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == expected_location
