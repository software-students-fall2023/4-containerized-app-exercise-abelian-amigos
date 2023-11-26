"""
Tests for the webapp.
"""

import pytest
from src.app import app
from src.web_app_defaults import USER_IMAGES_DIR


@pytest.fixture(name="client")
def fixture_client():
    """
    Create a test client for the Flask app.
    """
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection in tests
    client = app.test_client()

    yield client


def test_index(client):
    """
    Test the index route.
    """
    response = client.get("/")
    assert response.status_code == 302  # Redirect to login page when not authenticated


def test_register(client):
    """
    Test the registration route.
    """
    response = client.post(
        "/register", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 302  # Redirect to login page after registration
    assert response.headers["Location"] == "/login"


def test_login(client):
    """
    Test the login route.
    """
    response = client.post(
        "/login", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 302  # Redirect to index page after successful login
    assert response.headers["Location"] == "/"


def test_anime_route(client, monkeypatch):
    """
    Test the /anime route with a real image file.
    """
    # Specify the path to your test image
    test_image_path = USER_IMAGES_DIR / "test1.jpg"

    # Simulate a logged-in user
    with client:
        client.post("/login", data={"username": "testuser", "password": "testpassword"})

        # Mock the ML server response
        def mock_post(*args, **kwargs):
            _ = args, kwargs

            class MockResponse:
                """
                Mock class for simulating HTTP responses.
                """

                def __init__(self):
                    self.success = None

                def set_success(self, success):
                    """
                    Determine if response sent is a success or failure response
                    """
                    self.success = success

                def json(self):
                    """
                    Simulates the JSON response from an HTTP request.
                    """
                    return {"success": self.success, "image_name": "test_image.jpg"}

            good_response = MockResponse()
            good_response.set_success(True)
            return good_response

        monkeypatch.setattr("requests.post", mock_post)

        # Simulate the file upload
        with open(test_image_path, "rb") as image_file:
            response = client.post(
                "/sketchify", data={"photo": (image_file, "test_image.jpg")}
            )

    assert response.status_code == 200


def test_previous_route(client):
    """
    Test the /previous route.
    """

    with client:
        client.post("/login", data={"username": "testuser", "password": "testpassword"})
        response = client.get("/previous")
        assert response.status_code == 200
        assert b"test_image.jpg" in response.data
