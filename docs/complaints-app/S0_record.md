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




Had ChatGPT review the code. It found the following:


| #   | Priority             | Location                                                                                                                                                                                                 | Finding                                                                                                                                                                                                                                                                                                                                        |
| --- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Medium · Security    | [complaints/routes.py (line 10)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/routes.py:10)                                                                   | Anyone who can reach `/` can view every complaint row, including complainant names. This is intentional for S0’s synthetic data. Connecting the route to real records as written would expose them without authentication or authorization.                                                                                                    |
| 2   | Medium · Correctness | [complaints/services.py (line 33)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/services.py:33)                                                               | A single unrecognized product, category, or status raises `KeyError` and causes the entire complaints page to return HTTP 500. The checked-in fixtures contain valid values. The failure becomes relevant when the repository starts reading persisted records.                                                                                |
| 3   | Low · Usability      | [base.html (line 7)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/templates/base.html:7)                                                                                          | The locally served app depends on jsDelivr for all styling. When the CDN is blocked or unreachable, the page loses its styling and the table loses its narrow-screen scrolling behavior. The integrity hash matches the Bootstrap 5.3.8 stylesheet. [Bootstrap CDN documentation](https://getbootstrap.com/docs/5.3/getting-started/download/) |
| 4   | Low · Security       | [README.md (line 13)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/README.md:13), [README.md (line 41)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/README.md:41) | Both run commands enable Flask’s interactive debugger. The Windows instructions point to loopback. Reusing either command on a network-facing server would make the debugger reachable from outside the machine.                                                                                                                               |
| 5   | Low · Structure      | [test_complaints_services.py (line 11)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/tests/test_complaints_services.py:11)                                    | The test checks that each label belongs to the right set of labels. It would still pass if the service displayed “Closed” for every complaint. It never checks the label against the corresponding record.                                                                                                                                     |
| 6   | Low · Test coverage  | [test_no_get_writes.py (line 9)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/tests/test_no_get_writes.py:9)                                                                          | The no-write test silently skips every GET route with a path parameter. It covers the current complaint index and health check, but a future route such as `/complaints/<id>` could mutate data without failing this test.                                                                                                                     |


## What I fixed, and why

- **#4 — Debug mode.** I added a README note that says `--debug` is for local use only. This makes clear that the run command is for development, since exposing Flask’s interactive debugger on a network-facing server is a security risk.
- **#5 — Complaint labels.** I updated the test to check the product, category, and status labels against each complaint’s record. The old test could pass even if every complaint was shown as “Closed,” because “Closed” is a valid label.
- **#6 — GET route coverage.** I added a test that fails if a GET route with a path parameter is added without updating the no-write check. This makes the coverage gap visible when a route like `/complaints/<id>` is added.

## What I am knowingly leaving, and why

- **#1 — Public complaints list.** S0 uses made-up complaints, so the public list exposes no real complaint data. Login is planned for S1.
- **#2 — Unknown labels.** All S0 sample records use valid product, category, and status values. I’ll revisit how to handle unknown values when the app starts reading stored records.
- **#3 — CDN dependency.** The S0 brief calls for a pinned Bootstrap CDN URL. If the CDN is unavailable, the complaint data still shows, but the page loses its styling and the table may overflow on small screens. That trade-off is acceptable for S0.

SEE week03-review.md for additional.




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
