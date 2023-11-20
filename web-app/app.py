from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(), unique=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@login_required
def index():


    return render_template('homePage.html')

@app.route('/anime', methods=['GET', 'POST'])
def anime():
    # handle POST request.
    pass

# Route for handling the login page logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user = Users(
            username=request.form.get('username'),
            password=request.form.get('password')
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('hami yaha chau')
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("index"))
        else:
            print('user not found')
            return redirect(url_for("signup"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
