\# Complaints App S0 — Setup, Testing and Security Review



Date: 18 November 2026



\## Local Setup



I downloaded and extracted the Claude-generated Complaints App S0 prototype and opened it in VS Code. I created a Python virtual environment, installed the project dependencies and resolved a PowerShell script-execution restriction during initial setup.



\## Functional Testing



\- Ran the automated test suite: all 34 tests passed.

\- Started the Flask application locally and confirmed that the complaints page displayed:

&#x20; - The prototype warning banner.

&#x20; - Eight sample complaints, ordered newest first.

&#x20; - All five complaint statuses.

\- Confirmed that the `/health` endpoint returned `{"status":"ok"}`.

\- Tested the layout at a viewport width of 375 px. The table scrolled horizontally within its container without causing the whole page to scroll sideways.



\## Security Scanning and Review



\- Ran `pip-audit` against `requirements.txt`: no known vulnerabilities were reported.

\- Ran Bandit against `app/`: 31 Low findings were reported, with no Medium or High findings.

\- Reviewed the reported code:

&#x20; - 28 B101 findings concerned assertions in test files. These were recorded as expected test assertions and retained.

&#x20; - Three B105 findings concerned `"password\_hash": None` in synthetic sample records. These were recorded as false positives for hard-coded passwords.

\- Saved the scan reports and a written review in `evidence/security/`.



\## Outcome and Limitations



The S0 prototype runs successfully locally, and the functional checks and security scan review are complete.



It remains a read-only, unauthenticated prototype using synthetic data. The tests and scans provide evidence of basic operation and security review, not proof of complete security.







----------------


To run again:
Go to the application folder:

powershell
cd "C:\Users\blueg\lowcode-project\complaints-app-S0\complaints-app"
Run the automated tests whenever you want to check them:

powershell
.\.venv\Scripts\python.exe -m pytest
Start the app:

powershell
.\.venv\Scripts\python.exe -m flask --app app run --debug
Open these addresses in your browser:

text
http://127.0.0.1:5000/
http://127.0.0.1:5000/health
Stop the app in the terminal:

text
Ctrl + C
