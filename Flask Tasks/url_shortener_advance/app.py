from flask import Flask, render_template, request, redirect, url_for
from models import db, User, URL
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random, string, validators

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 5 or len(username) > 9:
            error = "Username must be between 5 to 9 characters long"
        elif User.query.filter_by(username=username).first():
            error = "This username already exists..."
        else:
            user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("signup.html", error=error)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form["url"]

        if not validators.url(original_url):
            error = "Invalid URL"
        else:
            code = generate_short_code()
            new_url = URL(
                original_url=original_url,
                short_code=code,
                user_id=current_user.id
            )
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + code

    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html",
                           short_url=short_url,
                           urls=urls,
                           error=error)

# ---------------- REDIRECT ----------------
@app.route("/<code>")
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first_or_404()
    return redirect(url.original_url)

# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
