def test_get_activities(client):
    # Arrange: nothing to set up

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_success(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/unregister", params={"email": email})  # Ensure clean state

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})


def test_signup_duplicate(client):
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})  # Ensure user is signed up

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Cleanup
    client.delete(f"/activities/{activity}/unregister", params={"email": email})


def test_signup_activity_not_found(client):
    # Arrange: nothing to set up

    # Act
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", params={"email": email})  # Ensure user is signed up

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_unregister_not_found(client):
    # Arrange: nothing to set up

    # Act
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_not_found(client):
    # Arrange: nothing to set up

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": "notfound@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_root_redirect(client):
    # Arrange: nothing to set up

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    # Optionally, check for expected HTML content
    assert b"Mergington High School" in response.content
