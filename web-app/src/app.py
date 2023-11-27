"""
Flask application for the web-app.
"""

import requests
from bson.objectid import ObjectId
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash

from src.web_app_defaults import (
    SECRET_KEY,
    ML_SERVER_URL,
    USER_IMAGES_DIR,
    SKETCH_IMAGES_DIR,
)

from src.web_app_db import db

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)


# User class
class User(UserMixin):
    """
    User class for flask-login
    """

    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]


@login_manager.user_loader
def load_user(user_id):
    """
    Load the user from the database
    """
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return None
    return User(user_data)


# Routes
@app.route("/")
def index():
    """
    Handle the HomePage route
    """
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect(url_for("login"))


@app.route("/sketchify", methods=["POST"])
def sketch():
    """
    Handle the Post request for photo upload.
    """
    # prepare the image for upload
    image = request.files["photo"]
    files = [("photo", (image.filename, image.stream, image.content_type))]

    # send the image to the machine learning server for generating the sketch
    response = requests.post(
        f"{ML_SERVER_URL}/sketch", files=files, timeout=10000
    ).json()

    if response["success"]:
        # save the image name in the database
        db.images.insert_one(
            {
                "image_name": response["image_name"],
                "user_id": current_user.id,
            }
        )
        return render_template("render.html", image_name=response["image_name"])

    return render_template("index.html", error=response["error"])


@app.route("/previous", methods=["GET", "POST"])
@login_required
def previous():
    """
    Retrieve and render all past sketches made by user.
    """

    user_renders = db.images.find({"user_id": current_user.id})
    return render_template("previous.html", user_renders=user_renders)


# Route for handling the login page logic
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle the register page logic.
    """
    if request.method == "POST":

        if db.users.find_one({"username": request.form.get("username")}):
            return render_template("register.html", error="Username already exists.")
        
        else:
            hashed_password = generate_password_hash(
                request.form.get("password"), method="pbkdf2:sha256"
            )

            db.users.insert_one(
                {"username": request.form.get("username"), "password": hashed_password}
            )

            user_data = db.users.find_one({"username": request.form.get("username")})
            user = User(user_data)
            login_user(user)
            return redirect(url_for("index"))
        
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle the login page logic.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = db.users.find_one({"username": username})

        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("index"))

        # Return to login page with an error message
        return render_template("login.html", error="Invalid username or password")

    # GET request: just show the login form
    return render_template("login.html")


@app.route("/images/<image_type>/<image_name>")
def serve_images(image_type, image_name):
    """
    A function to serve the images from the server.
    """
    directory = SKETCH_IMAGES_DIR if image_type == "sketch_image" else USER_IMAGES_DIR
    return send_from_directory(directory, image_name)


@app.route("/logout")
@login_required
def logout():
    """
    Handle the logout logic.
    """
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8001)
