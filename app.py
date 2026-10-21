from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
    <h1>Hello from Claude</h1>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True)
