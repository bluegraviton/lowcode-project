from flask import Flask, request
import re

app = Flask(__name__)

NAV = """<nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>"""

STYLE = """<style>
    body { font-family: sans-serif; max-width: 700px; margin: 0 auto; padding: 1rem; }
    nav { padding-bottom: 0.5rem; border-bottom: 1px solid #ccc; margin-bottom: 1rem; }
    nav a { margin-right: 1rem; text-decoration: none; }
    .error { color: red; margin-bottom: 1rem; }
    .form-group { margin-bottom: 1rem; }
    .form-group label { display: block; margin-bottom: 0.5rem; }
    .form-group input, .form-group textarea { width: 100%; padding: 0.5rem; box-sizing: border-box; }
    button { padding: 0.5rem 1rem; cursor: pointer; }
</style>"""


def page(title, content):
    """Wrap page content in the shared HTML layout, including the navigation."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    {STYLE}
</head>
<body>
    {NAV}
    {content}
</body>
</html>"""


@app.route("/")
def home():
    return page("Hello", "<h1>Hello from Claude</h1>")


@app.route("/about")
def about():
    return page("About", """<h1>What would I build in an evening?</h1>
    <p>Actually, I don't know! I have a few very loose ideas on what I'd do but for now, I'm just putting a lorem ipsum idea here.</p>

    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>

    <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>""")


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    error = None
    name = ""
    email = ""
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            error = "All fields (name, email, and message) are required."
        elif not EMAIL_REGEX.match(email):
            error = "Please enter a valid email address."
        else:
            confirmation_content = f"""<h1>Thank You!</h1>
            <p>Thank you, <strong>{name}</strong>. Your message has been received.</p>
            <p><a href="/">Return to Home</a></p>"""
            return page("Contact - Thank You", confirmation_content)

    error_html = f'<div class="error">{error}</div>' if error else ""
    
    form_content = f"""<h1>Contact Us</h1>
    {error_html}
    <form method="post" action="/contact">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{name}">
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" value="{email}">
        </div>
        <div class="form-group">
            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="5">{message}</textarea>
        </div>
        <button type="submit">Send Message</button>
    </form>"""

    return page("Contact", form_content)


if __name__ == "__main__":
    app.run(debug=True)
