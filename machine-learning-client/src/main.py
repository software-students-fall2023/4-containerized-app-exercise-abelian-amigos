"""
This module contains code for a machine learning client that creates sketch from an image.
"""
import os
from datetime import datetime

import cv2
from flask import Flask, request
from werkzeug.utils import secure_filename

from src.ml_defaults import USER_IMAGES, SKETCH_IMAGES
from src.ml_db import db
from src.model import Model


def make_directories(user_images, sketch_images):
    """
    A function to ensure all the directories needed for the application to run are present.
    """
    for directory in [user_images, sketch_images]:
        if not os.path.exists(directory):
            os.makedirs(directory)


def init_app():
    """
    A function to initialize the application and instantiate the model used for sketching
    """
    make_directories(USER_IMAGES, SKETCH_IMAGES)
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
    image.save(USER_IMAGES / image_name)
    return image_name


@app.route("/sketch", methods=["POST"])
def sketch():
    """
    A function to run the sketch model on the image.
    """
    image_name = save_image()
    image = cv2.imread(str(USER_IMAGES / image_name))

    try:
        start = datetime.now()
        output = model.run(image)
        end = datetime.now()
        duration = (end - start).total_seconds()
        db.inferences.insert_one(
            {
                "image": image_name,
                "start_time": start,
                "end_time": end,
                "inference_time": duration,
            }
        )
        cv2.imwrite(str(SKETCH_IMAGES / image_name), output)
        return {"success": True, "image_name": image_name}
    except ValueError:
        return {"success": False, "error": "No face detected in the image. Try again."}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
