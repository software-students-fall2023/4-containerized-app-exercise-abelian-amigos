"""
This file contains the default values for the web-app.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ML_SERVER_URL = os.getenv("ML_SERVER_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

MONGO_DB_HOST = os.getenv("MONGO_DB_HOST")
MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT"))
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
DATABASE_NAME = os.getenv("MONGO_DB_NAME")

IMAGES_DIR = Path(__file__).parent.parent / "images"
USER_IMAGES_DIR = IMAGES_DIR / "user_images"
SKETCH_IMAGES_DIR = IMAGES_DIR / "sketch_images"
