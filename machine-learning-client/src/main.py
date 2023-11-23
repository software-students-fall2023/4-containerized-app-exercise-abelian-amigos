"""
This module contains code for a machine learning client that creates sketch from an image.
"""
import os
from datetime import datetime

import cv2

from flask import Flask, request
from werkzeug.utils import secure_filename
from src.defaults import TEMPLATES_DIR, INPUT_DIR, OUTPUT_DIR
from src.model import Model


def make_directories():
    """
    A function to ensure all the directories needed for the application to run are present.
    """
    for directory in [TEMPLATES_DIR, INPUT_DIR, OUTPUT_DIR]:
        if not os.path.exists(directory):
            os.mkdir(directory)


def init_app():
    """
    A function to initialize the application and instantiate the model used for sketching
    """
    make_directories()
    app_ = Flask(__name__)
    model_ = Model()

    return app_, model_


app, model = init_app()


def save_image():
    """
    A function to save the uploaded images from the requests into a predetermined directory.
    """
    image = request.files["photo"]
    timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M-%S.%f")
    image_name = f"{timestamp}_{secure_filename(image.filename)}"
    image.save(INPUT_DIR / image_name)
    return image_name


@app.route("/sketch", methods=["POST"])
def sketch():
    """
    A function to run the sketch model on the image.
    """
    image_name = save_image()
    image = cv2.imread(str(INPUT_DIR / image_name))

    try:
        output = model.run(image)
        cv2.imwrite(str(OUTPUT_DIR / image_name), output)
        return {"image_name": image_name}
    except ValueError:
        return {"error": "No face detected in the image."}


if __name__ == "__main__":
    app.run(debug=True, port=8002)
