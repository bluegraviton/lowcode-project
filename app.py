from flask import Flask

app = Flask(__name__)

NAV = """<nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
</nav>"""

STYLE = """<style>
    body { font-family: sans-serif; max-width: 700px; margin: 0 auto; padding: 1rem; }
    nav { padding-bottom: 0.5rem; border-bottom: 1px solid #ccc; margin-bottom: 1rem; }
    nav a { margin-right: 1rem; text-decoration: none; }
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


if __name__ == "__main__":
    app.run(debug=True)