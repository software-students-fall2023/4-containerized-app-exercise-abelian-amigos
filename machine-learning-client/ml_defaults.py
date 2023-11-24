"""
This file contains the default values for the machine learning client.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent

MODELS_DIR = ROOT_DIR / "models"

IMAGES_DIR = ROOT_DIR.parent / "images"
USER_IMAGES = IMAGES_DIR / "user_images"
SKETCH_IMAGES = IMAGES_DIR / "sketch_images"

MONGO_HOST = os.getenv("MONGO_DB_HOST")
MONGO_PORT = int(os.getenv("MONGO_DB_PORT"))
MONGO_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
