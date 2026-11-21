# Complaints App

Coursework prototype of an internal complaints-handling web app. All data is synthetic. This is **slice S0 (Baseline)**: a Flask app showing sample complaints, with no database, no login and no deployment. See Core Spec V1.3 and Build Plan V1.3.

## Run it on Windows (PowerShell, from VS Code)

Tested with Python 3.12; Python 3.10 or later is expected to work. Open the project folder in VS Code, then open a terminal (Terminal > New Terminal).

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
flask --app app run --debug
```

Open http://127.0.0.1:5000/ for the sample complaints and http://127.0.0.1:5000/health for the status check. Stop the server with Ctrl+C.

If activation is blocked ("running scripts is disabled"), allow scripts for this terminal session only, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\.venv\\Scripts\\Activate.ps1
```

Run the tests:

```powershell
pytest
```

\--debug is for local use only. Never use it on a network-facing server.



### Select the interpreter in VS Code

Press Ctrl+Shift+P, choose **Python: Select Interpreter**, then pick the one under `.venv` (it shows `.\\.venv\\Scripts\\python.exe`). Open a new terminal afterwards; it should show `(.venv)` at the start of the prompt.

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app app run --debug
pytest
```

## Security scan

With the virtual environment active, from the project root:

```powershell
pip-audit -r requirements.txt
bandit -r app
```

Save each output under `evidence/security/` with the date and a one-line caption.

## Folder layout

```
app/
  \_\_init\_\_.py       create\_app() and the ONE FEATURES list
  config.py         all enumerations and tunables; Config and TestConfig
  sample\_data.py    synthetic users and complaints (repository files only)
  templates/        shared layout (base.html)
  features/
    health/         GET /health
    complaints/     routes.py, services.py, repository.py, templates/, tests/
tests/              cross-cutting tests only
conftest.py         app and client fixtures shared by all tests
evidence/           automations, security, diagrams, deployment, ai
docs/               limitations register, decision log
```

Request chain: route, then service, then repository, then sample data. Routes only render. Services hold logic and call only their own repository. Only `repository.py` files import `app.sample\_data`; a test enforces this.

## Add a feature

1. Create `app/features/<name>/` with `\_\_init\_\_.py` (containing `register(app)`), `routes.py`, `services.py`, `repository.py`, `templates/<name>/` and `tests/`. Use the Blueprint name `<name>`; test file names must be unique across the project (prefix with the feature name).
2. Add one line to `FEATURES` in `app/\_\_init\_\_.py`, with its import.
3. Put any new enumerations in `app/config.py`.

A test fails if a feature folder exists but is missing from `FEATURES`. Full checklist: Build Plan Section 8.6.

## Where SQLite plugs in

Only `repository.py` files change. In S1 and S2b each feature's `repository.py` is rewritten to read from SQLite instead of `app.sample\_data`. Function names, arguments and returned field names stay the same (the field names already match the Core Spec Section 7 tables), so services, routes and templates do not change. PostgreSQL arrives at step M1 with no repository edits expected.

