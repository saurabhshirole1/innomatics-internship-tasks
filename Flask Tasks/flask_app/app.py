from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name")

    if not name:
        return "<h2>Please pass your name like ?name=YourName</h2>"

    upper_name = name.upper()
    reverse_name = name[::-1]
    name_length = len(name)

    return f"""
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1 style="color: green;">WELCOME, {upper_name} 🫡</h1>
            <p><b>Original Name:</b> {name}</p>
            <p><b>Upper Case:</b> {upper_name}</p>
            <p><b>Reversed Name:</b> {reverse_name}</p>
            <p><b>Name Length:</b> {name_length} characters</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
