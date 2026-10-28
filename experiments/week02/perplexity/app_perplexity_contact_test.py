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
    label { display: block; margin-bottom: 0.3rem; }
    input, textarea { box-sizing: border-box; width: 100%; padding: 0.5rem; font: inherit; }
    .error { display: block; color: #a00000; margin-top: 0.3rem; }
    [aria-invalid="true"] { border: 2px solid #a00000; }
    button { padding: 0.5rem 1rem; font: inherit; }
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



# Practical ASCII email syntax validation; this does not verify deliverability.
_LOCAL_PART = re.compile(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+")
_DOMAIN_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")


def valid_email(value):
    """Accept common unquoted email addresses with a dotted domain."""
    if len(value) > 254 or value.count("@") != 1:
        return False
    local, domain = value.split("@")
    if (not local or len(local) > 64 or not _LOCAL_PART.fullmatch(local)
            or local.startswith(".") or local.endswith(".") or ".." in local):
        return False
    labels = domain.split(".")
    return (len(labels) >= 2 and len(domain) <= 253
            and all(_DOMAIN_LABEL.fullmatch(label) for label in labels)
            and not labels[-1].isdigit())


def contact_form(values, errors):
    """Escape submitted text before redisplaying it in HTML."""
    fields = []
    for key, label in (("name", "Name"), ("email", "Email"), ("message", "Message")):
        value = escape(values.get(key, ""), quote=True)
        error = errors.get(key)
        attributes = ' required'
        if error:
            attributes += f' aria-invalid="true" aria-describedby="{key}-error"'
        if key == "message":
            control = f'<textarea id="{key}" name="{key}" rows="6"{attributes}>{value}</textarea>'
        else:
            kind = "email" if key == "email" else "text"
            control = f'<input type="{kind}" id="{key}" name="{key}" value="{value}"{attributes}>'
        error_html = (f'<span class="error" id="{key}-error">{escape(error)}</span>'
                      if error else "")
        fields.append(f'<p><label for="{key}">{label}</label>{control}{error_html}</p>')
    summary = ('<p class="error" role="alert">Please correct the errors below.</p>'
               if errors else "")
    return page("Contact", '<h1>Contact</h1>' + summary
                + '<form method="post" action="/contact" novalidate>'
                + "".join(fields) + '<button type="submit">Submit</button></form>')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    values = {key: "" for key in ("name", "email", "message")}
    errors = {}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        for key, label in (("name", "Name"), ("email", "Email"), ("message", "Message")):
            if not values[key]:
                errors[key] = f"{label} is required."
        if values["email"] and not valid_email(values["email"]):
            errors["email"] = "Enter a well-formed email address, such as name@example.com."
        if not errors:
            # Do not persist, log, email, or put submitted data in the URL/session.
            return redirect(url_for("contact_confirmation"), code=303)
    return contact_form(values, errors), 400 if errors else 200


@app.route("/contact/confirmation")
def contact_confirmation():
    return page("Contact confirmation", """<h1>Thank you</h1>
    <p>Your contact form passed validation. No information has been stored or sent.</p>
    <p><a href="/">Return to home</a></p>""")


if __name__ == "__main__":
    app.run(debug=True)