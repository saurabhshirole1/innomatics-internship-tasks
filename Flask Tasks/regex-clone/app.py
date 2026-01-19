from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    highlighted = ""
    error = None
    pattern = ""
    text = ""

    if request.method == "POST":
        pattern = request.form["pattern"]
        text = request.form["text"]

        try:
            regex = re.compile(pattern)
            matches = regex.findall(text)
            highlighted = regex.sub(r"<mark>\g<0></mark>", text)
        except re.error:
            error = "Invalid Regular Expression"

    return render_template(
        "index.html",
        matches=matches,
        highlighted=highlighted,
        error=error,
        pattern=pattern,
        text=text
    )

if __name__ == "__main__":
    app.run(debug=True)
