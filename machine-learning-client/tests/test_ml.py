"""
Test ML Client API
"""
import os
import pytest

# Import the functions and objects from the module you want to test
from src.main import app
from src.ml_defaults import USER_IMAGES, SKETCH_IMAGES
from src.ml_db import db


@pytest.fixture(name="client")
def fixture_client():
    """
    Fixture for setting up a test client with app configured for testing.

    Returns:
        Flask test client: The configured Flask test client.
    """
    app.config["TESTING"] = True
    client_ = app.test_client()
    yield client_


@pytest.fixture(name="valid_test_image")
def fixture_valid_test_image():
    """
    Fixture for providing a valid test image file.

    Returns:
        Binary file: The valid test image file.
    """
    return open(USER_IMAGES / "test1.jpg", "rb")


@pytest.fixture(name="invalid_test_image")
def fixture_invalid_test_image():
    """
    Fixture for providing an invalid test image file.

    Returns:
        Binary file: The invalid test image file.
    """
    return open(USER_IMAGES / "test2.jpg", "rb")


def test_make_directories():
    """
    Test case for when directories don't exist.
    """
    for directory in [USER_IMAGES, SKETCH_IMAGES]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    assert os.path.exists(USER_IMAGES)
    assert os.path.exists(SKETCH_IMAGES)


def test_valid_sketch(client, valid_test_image):
    """
    Test case for submitting a valid sketch request.

    Args:
        client: The test client to use.
        valid_test_image: The valid test image file to use.
    """
    data = {"photo": (valid_test_image, "test_image_1.jpg")}
    response = client.post("/sketch", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert response.json["success"]

    image_name = response.json["image_name"]

    assert os.path.exists(os.path.join(USER_IMAGES, image_name))
    assert db.inferences.find_one({"image": image_name})


def test_invalid_sketch(client, invalid_test_image):
    """
    Test case for submitting an invalid sketch request.

    Args:
        client: The test client to use.
        valid_test_image: The invalid test image file to use.
    """
    data = {"photo": (invalid_test_image, "test_image_2.jpg")}
    response = client.post("/sketch", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    assert not response.json["success"]

    assert response.json["error"]
    assert response.json["error"] == "No face detected in the image. Try again."
