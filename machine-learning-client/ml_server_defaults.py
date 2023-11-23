"""
This file contains the default values for the machine learning client.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent

MODELS_DIR = ROOT_DIR / "models"

IMAGES_DIR = ROOT_DIR.parent / "images"
USER_IMAGES = IMAGES_DIR / "user_images"
SKETCH_IMAGES = IMAGES_DIR / "sketch_images"
