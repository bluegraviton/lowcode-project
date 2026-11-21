\# S0 Security Scan Review — 2026-11-18



\## Dependency audit



Command: `pip-audit -r requirements.txt`



Result: No known vulnerabilities found.



Scope: Dependencies audited from requirements.txt. This result does not

cover every aspect of application security or guarantee future results.



\## Bandit



Command: `bandit -r app`



Result: 31 Low findings, 0 Medium, 0 High. No files skipped.



\### B101 — 28 findings



All reported occurrences are assertions in automated test files.

Reviewed as expected test assertions, not production security checks.

Disposition: retain assertions; no code change.



\### B105 — 3 findings



Locations: app/sample\_data.py, lines 53, 62 and 71.



Each reported value is `"password\_hash": None`.

These are absent password hashes in synthetic sample records, not

embedded passwords.

Disposition: false positives for these specific lines; no code change.

Revisit credential handling when authentication is implemented.



\## Evidence capture note



Windows PowerShell formatted native diagnostic output as

NativeCommandError records during output redirection. The reports

nevertheless contain the audit result and complete Bandit summary.



\## Limitations



These scans are supporting evidence, not proof that the application is

secure. S0 remains a local, unauthenticated sample-data prototype.

