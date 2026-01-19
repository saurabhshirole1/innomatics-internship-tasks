from flask import Flask, render_template, request, redirect, url_for
from models import db, URL
import random, string
import validators

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    error = None

    if request.method == "POST":
        original_url = request.form.get("url")

        if not validators.url(original_url):
            error = "Invalid URL. Please enter a valid URL."
        else:
            short_code = generate_short_code()
            new_url = URL(original_url=original_url, short_code=short_code)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + short_code

    return render_template("home.html", short_url=short_url, error=error)

@app.route("/history")
def history():
    urls = URL.query.all()
    return render_template("history.html", urls=urls)

@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

if __name__ == "__main__":
    app.run(debug=True)
