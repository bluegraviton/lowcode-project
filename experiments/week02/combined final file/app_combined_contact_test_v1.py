import os
import re
from html import escape

from flask import Flask, redirect, request, url_for

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
    form label { display: block; margin-top: 1rem; font-weight: bold; }
    form input, form textarea { width: 100%; box-sizing: border-box; padding: 0.5rem; font: inherit; }
    form button { margin-top: 1rem; padding: 0.5rem 1rem; font: inherit; cursor: pointer; }
    .errors { border: 1px solid #c0392b; background: #fdecea; color: #922b21; padding: 0.5rem 1rem; margin-bottom: 1rem; }
    .errors ul { margin: 0; padding-left: 1.2rem; }
    .field-error { color: #922b21; font-size: 0.9rem; margin: 0.25rem 0 0; }
    input.invalid, textarea.invalid { border: 2px solid #c0392b; }
</style>"""

MAX_NAME_LENGTH = 100
MAX_MESSAGE_LENGTH = 2000

# Practical ASCII email syntax validation; this does not verify deliverability.
MAX_EMAIL_LENGTH = 254
MAX_LOCAL_LENGTH = 64
MAX_DOMAIN_LENGTH = 253
_LOCAL_PART = re.compile(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+")
_DOMAIN_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")


def h(value):
    """Escape a value for safe inclusion in HTML text or attributes."""
    return escape(value, quote=True)


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


def is_valid_email(value):
    """Accept common unquoted email addresses with a dotted domain."""
    if len(value) > MAX_EMAIL_LENGTH or value.count("@") != 1:
        return False
    local, domain = value.split("@")
    if (not local or len(local) > MAX_LOCAL_LENGTH
            or not _LOCAL_PART.fullmatch(local)
            or local.startswith(".") or local.endswith(".") or ".." in local):
        return False
    labels = domain.split(".")
    return (len(labels) >= 2 and len(domain) <= MAX_DOMAIN_LENGTH
            and all(_DOMAIN_LABEL.fullmatch(label) for label in labels)
            and not labels[-1].isdigit())


def validate_contact(name, email, message):
    """Return a dict of field -> error message (empty dict means valid)."""
    errors = {}
    if not name:
        errors["name"] = "Please enter your name."
    elif len(name) > MAX_NAME_LENGTH:
        errors["name"] = f"Name must be {MAX_NAME_LENGTH} characters or fewer."
    if not email:
        errors["email"] = "Please enter your email address."
    elif not is_valid_email(email):
        errors["email"] = "Please enter a valid email address (e.g. you@example.com)."
    if not message:
        errors["message"] = "Please enter a message."
    elif len(message) > MAX_MESSAGE_LENGTH:
        errors["message"] = f"Message must be {MAX_MESSAGE_LENGTH} characters or fewer."
    return errors


def contact_form(values=None, errors=None):
    """Render the contact page, optionally with submitted values and errors."""
    values = values or {}
    errors = errors or {}

    def val(field):
        return h(values.get(field, ""))

    def field_error(field):
        if field in errors:
            return f'<p class="field-error" id="{field}-error">{h(errors[field])}</p>'
        return ""

    def cls(field):
        return ' class="invalid"' if field in errors else ""

    def aria(field):
        if field in errors:
            return f' aria-invalid="true" aria-describedby="{field}-error"'
        return ""

    summary = ""
    if errors:
        items = "".join(f"<li>{h(msg)}</li>" for msg in errors.values())
        summary = f'<div class="errors" role="alert"><strong>Please fix the following:</strong><ul>{items}</ul></div>'

    return page("Contact", f"""<h1>Contact</h1>
    {summary}
    <form method="post" action="/contact" novalidate>
        <label for="name">Name</label>
        <input type="text" id="name" name="name" value="{val('name')}"{cls('name')}{aria('name')}>
        {field_error('name')}

        <label for="email">Email</label>
        <input type="email" id="email" name="email" value="{val('email')}"{cls('email')}{aria('email')}>
        {field_error('email')}

        <label for="message">Message</label>
        <textarea id="message" name="message" rows="6"{cls('message')}{aria('message')}>{val('message')}</textarea>
        {field_error('message')}

        <button type="submit">Send message</button>
    </form>""")


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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return contact_form()

    values = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "message": request.form.get("message", "").strip(),
    }
    errors = validate_contact(**values)
    if errors:
        # 400 signals the submission was rejected; the form is re-shown with
        # the visitor's input preserved and the errors displayed.
        return contact_form(values, errors), 400

    # Submitted data is never persisted, logged, emailed, or put in the
    # URL/session. If saving or sending is ever added, CSRF protection
    # (e.g. Flask-WTF) is required first.
    return redirect(url_for("contact_confirmation"), code=303)


@app.route("/contact/confirmation")
def contact_confirmation():
    return page("Contact confirmation", """<h1>Confirmation</h1>
    <p>Thank you. Your contact form passed validation. No information has been stored or sent.</p>
    <p><a href="/">Return to the home page</a></p>""")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")