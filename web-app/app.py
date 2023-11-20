"""
    Flask application for the web-app.
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# Initialize the app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/anime"
app.config["SECRET_KEY"] = "secret_key"

# Initialize Pymongo
mongo = PyMongo(app)

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
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        return None
    return User(user_data)


# Routes
@app.route("/")
@login_required
def index():
    """
        Handle the HomePage route
    """
    return render_template("homePage.html")


@app.route("/anime", methods=["GET", "POST"])
def anime():
    """
        Handle the Post request for photo upload.
    """
    # handle POST request.
    print('request.method', request.method)
# Route for handling the login page logic
@app.route("/register", methods=["GET", "POST"])
def register():
    """
        Handle the register page logic.
    """
    if request.method == "POST":
        # Hash the password before storing it
        hashed_password = generate_password_hash(request.form.get("password"))
        mongo.db.users.insert_one(
            {"username": request.form.get("username"), "password": hashed_password}
        )
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
        Handle the login page logic.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = mongo.db.users.find_one({"username": username})

        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data)  # Assuming User is a class that you've defined
            login_user(user)
            return redirect(url_for("index"))

        print("Invalid username or password")
        # Return to login page with an error message
        return render_template("login.html", error="Invalid username or password")

    # GET request: just show the login form
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
