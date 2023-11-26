"""
Test the ML server model.
"""
import cv2
import pytest
from src.ml_defaults import USER_IMAGES
from src.model import Model


def test_model():
    """
    Test the model.
    """
    model = Model()
    assert model is not None
    assert model.device == "cpu"

    # image with face
    image_path = USER_IMAGES / "test1.jpg"
    assert image_path.exists()

    image = cv2.imread(str(image_path))
    assert image is not None
    assert model.run(image) is not None

    # image without face
    image_path = USER_IMAGES / "test2.jpg"
    assert image_path.exists()

    image = cv2.imread(str(image_path))
    assert image is not None
    with pytest.raises(ValueError):
        model.run(image)
