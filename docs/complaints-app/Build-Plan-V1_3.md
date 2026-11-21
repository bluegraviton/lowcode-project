# Complaints App — Build Plan V1.3

**Version:** 1.3 — 11 November 2026
**Applies to:** Core Spec V1.3.
**Precedence:** The Core Spec defines what to build. This plan defines how, in what order, and how to keep records as you go. If they conflict, the Core Spec wins and the owner is asked.

## 0. Using this plan

- Give the AI builder **the current Core Spec and this plan** every session. Give it only the V0.8 sections named in a stretch item, never the whole of V0.8.
- Work one slice at a time (Section 3). A slice is finished only when its checklist (Section 3.2) is ticked.
- The builder stops and asks if the documents conflict or anything is ambiguous.
- Spec changes go in the change log at the end of the Core Spec. Nothing gets rewritten in place.

## 1. Constraints and assumptions

| Item | Assumption |
|---|---|
| Deadline | End of week 11, 11:59 pm, which you place in the first week of January 2027. Confirm the exact date on the timetable. Live demonstration in week 12 |
| Late penalty | 10% of the mark for up to 5 calendar days late, then 0. Treat this as a safety net only |
| Time | 10 hours a week, separate from class sessions. Week 5 is partial (about 6 hours). Total about 66 hours |
| Split | About 38 hours build and test, about 28 hours documents and evidence |
| Database | Three stages: in-memory sample data (S0), SQLite (S1 to S2b), PostgreSQL from step M1 in week 8. See Section 3.3 and Core Spec Section 9.1 |
| Hosting | Local development first. The host is researched in S0 and its claims verified in the provider's documentation by the end of week 7. The skeleton is deployed in step D1, straight after M1 |
| Freeze | End of week 10. Week 11 is documents and submission only |
| Christmas | Assumed to fall between week 10 and week 11. If your break hits earlier, tell me and the weeks move |

Class practicals run the same project (data model in session 5, interface 6, tests 7, scan 8, Dockerfile 9, deployment 10, governance 11). Use them to review the matching item, but do not wait for them. This plan runs ahead of them.

## 2. Marks and where the hours go

The Core Spec maps rubric to criteria. The takeaway for time: about 60 of 100 marks come from repository evidence, responsible development and communication, which do not need complex rules. A smaller app that works, is deployed, is tested and is well evidenced beats a larger one that is not.

**Protected core (never cut):** the approval step with snapshot, the audit trail with database revocation, the move to PostgreSQL (M1) that makes that revocation possible, the deadline engine and its tests, role enforcement on the data, the three automations, deployment, tests, the scan response and the documents.

## 3. Build slices

### 3.1 Slices

| Slice | Content | Hours |
|---|---|---|
| **S0 Baseline** | Repository; Python virtual environment with `requirements.txt` and a README giving the run steps; Flask application factory with ONE explicit FEATURES list; one configuration module; **a repository layer over in-memory synthetic sample data** (`app/sample_data.py`), no database; `/health`; a simple read-only home page listing the sample complaints, to prove the chain route → service → repository → template; pytest; create the evidence folders; first scan run; **hosting options researched and written up (no deployment in S0)**. The host must support a scheduled CLI job, two database roles and a monitoring tool. **No Docker, SQLite, PostgreSQL or Alembic in S0** | 3 |
| **S1 Foundations** | **SQLite introduced.** Flask-SQLAlchemy and Alembic (batch mode); `DATABASE_URL` from the environment; User and AuditEvent models; the user and audit repositories reimplemented on SQLite behind the same functions; login, logout, CSRF, secure cookies, idle expiry; role checks in services; audit service, append-only by convention with a test that the audit repository has no update or delete function; `provision-user` CLI; wrong-role direct-request tests. The S0 home page moves behind login. Complaints stay on sample data until S2b. **Audit revocation is not built here; it moves to M1** | 4 |
| **S2a Deadline engine** | **Tests first.** Holiday dataset with the Good Friday and Easter Monday test; pure working-day module; the two worked examples; weekends, October holiday, year boundary, late-Friday receipt, day-40 boundary | 3 |
| **S2b Intake and milestones** | Complaint, Milestone and Correspondence (draft) models, with their repositories switched from sample data to SQLite; the documented seed command that loads the synthetic sample records into the database; intake form and route; milestones and acknowledgement draft created in one transaction (automation A-2); complaint list and detail; countdown display with text status | 6 |
| **M1 Move to PostgreSQL** (not a feature slice) | Docker Compose with PostgreSQL; owner and application roles, with two connection settings in the environment (owner for migrations, application role for the app); run all migrations on empty PostgreSQL and fix portability problems; **audit-table revocation migration and its test (SC-06, R-SEC-03)**; DDL test (the application role cannot change the schema); the whole existing suite passes unchanged on PostgreSQL; remove SQLite-only settings; re-run the seed command; update the README | 3 |
| **D1 Deploy skeleton** (not a feature slice) | Deploy the app as it stands after M1 to the chosen host; run the migrations as the owner role; confirm the DDL test and the audit-revocation test pass against the **hosted** database; record the URL; write the redeploy and rollback note. **Done by the end of week 8** | 1 |
| **S3 Investigation and approval** | Investigation save; final-response draft; `submit-outcome` with snapshot, hash and first-submission rules; approval queue and decision (automation A-3); return of a pending approval; **write the state-transition test table first, before UI code**; immutability and self-approval tests. `return-to-investigation` after approval is added only at the end of S5, once submit → approve → send → close passes | 6 |
| **S4 Outbox** | Short, generic placeholder templates with the mandatory content (wording is not marked; the workflow is); composer and preview; `send()` with the log-only transport; allowlist; send service transaction; milestone completion; ordering rule R-ORDER-01 | 5 |
| **S5 Closure and scheduled check** | Closure gates, day-40 outcome, waivers; routine milestone generation; `deadline-check` CLI with `ScheduledRun` and digest (automation A-1); simple dashboard | 7 |

Total about 38 hours.

**S0 is done only when:** a clean clone runs locally using the README steps (create a virtual environment, `pip install -r requirements.txt`, `flask --app app run --debug`); the home page at `http://127.0.0.1:5000/` shows the sample complaints; `/health` responds; `pytest` passes; the sample data is synthetic and reached only through the repository module; the first scan output is saved; and `evidence/deployment/hosting-options.md` lists the options and the claims still to verify in each provider's own documentation.

**S1 is done only when:** the checklist in Section 3.2 is ticked; a clean clone creates the SQLite database with the migration command and seeds a user with `provision-user`; that user can log in and the home page requires login; the wrong-role tests pass; and no service imports sample data, the database session or a model.

**M1 is done only when:** `docker compose up` starts the app against PostgreSQL from a clean clone; migrations run as the owner role on an empty PostgreSQL database; the audit-revocation test and the DDL test pass; the whole suite passes on PostgreSQL with no test weakened or deleted; SQLite-specific code is removed; and L-18 is deleted.

**D1 is done only when:** the deployed URL responds; a synthetic test user can log in; the DDL and audit-revocation tests pass against the hosted database; and `evidence/deployment/redeploy-and-rollback.md` exists with the URL recorded. If the chosen host cannot support two database roles or a scheduled job, stop and choose another host before building S3.

**Evidence folders (created in S0):** `evidence/automations/`, `evidence/security/` (scans and accessibility review), `evidence/diagrams/`, `evidence/deployment/`, `evidence/ai/`. Save every screenshot, scan output and test run when it happens, with the date and a one-line caption.

### 3.2 "Done" checklist for every slice

- [ ] Tests for the slice pass: on the current database stage before M1 (in-memory, then SQLite) and on PostgreSQL from M1.
- [ ] Each rule ID touched has a test that names it.
- [ ] State changes, denials and sends write audit events.
- [ ] New boundary-crossing flows have STRIDE rows.
- [ ] Limitations register and decision log updated (Section 7).
- [ ] AI log updated: prompts verbatim, what was accepted, modified or rejected.
- [ ] Small commits made, AI-assisted code flagged in the message.
- [ ] App starts from a clean checkout: `flask run` before M1, Docker Compose from M1.

### 3.3 Database stages and the repository layer

Core Spec Section 9.1 holds the rules. In practice:

1. **S0.** `app/sample_data.py` holds synthetic users and complaints as plain Python lists and dicts. Each feature has a `repository.py` with functions such as `list_complaints()` and `get_complaint(id)` that read the sample data. Services call only repository functions.
2. **S1.** Add the database setup in `core/` and the User and AuditEvent models. Rewrite only `repository.py` for those two features so the same functions read from SQLite. Services and templates do not change. Complaints still use sample data.
3. **S2b.** Add the Complaint, Milestone and Correspondence models and rewrite their repositories the same way. The seed command now loads `sample_data.py` into the database.
4. **M1.** Change `DATABASE_URL` to PostgreSQL. No repository, service or route should need editing; fix anything that does as a portability bug.

SQLite points to watch until M1: switch foreign keys on (`PRAGMA foreign_keys=ON`) in one place; use Alembic batch mode; do not rely on `with_for_update()` (SQLite ignores it); return timestamps as UTC-aware values through one helper; use the SQLAlchemy `Numeric` and `JSON` types, not raw column types; keep any SQLite-only behaviour out of the code.

## 4. Weekly plan

| Week | Build (hours) | Documents and evidence (hours) | Exit check |
|---|---|---|---|
| **5** (part) | S0 (3) | Send Core Spec page 1 to the lecturer; start the regulation table (Core Spec Section 11); start the AI log (3) | Clean clone runs locally with `flask run`; sample home page and `/health` work; hosting options written up; first scan recorded |
| **6** | S1 (4), S2a (3) | DFD draft; STRIDE skeleton listing F-1 to F-8; **finish regulation table before S2a starts** (3) | Auth and audit-service tests pass on SQLite; deadline tests pass |
| **7** | S2b (6), M1 start (1) | Role/CRUD table draft; GDPR draft (3). Verify hosting claims in the provider's documentation | S2b done; M1 started. **Pace test** (Section 5) |
| **8** | M1 finish (2), D1 deploy (1), S3 start (4) | Governance policy draft; limitations entries; second scan after M1; accessibility and 375 px check on the first case page (3) | Tests pass on PostgreSQL; hosted audit-revocation test passes; skeleton deployed; second scan recorded |
| **9** | S3 finish (2), S4 (5) | STRIDE rows completed for built flows (3) | Approval loop works end to end; outbox works. **Pace test.** Must list demonstrable by end of week 10 at the latest |
| **10** | S5 (7), including `return-to-investigation` after approval. **Stretch only if ahead and the minimum viable demo has been rehearsed** | ERD generated; DFD and STRIDE final; final scan with responses; accessibility re-check on the final UI (3). **Feature freeze at end of week** | Tests and scans green on PostgreSQL |
| **11** | None | Write-up; GDPR final; governance policy; runbook; AI declaration; cover page; clean-checkout redeploy check; submission pack (10) | Submitted |

Weeks 6 to 10 are 7 build hours plus 3 document hours. The plan has no planned slack. M1 (3 hours) is new work, paid for by lighter S0 and S1 (no Docker, database roles or revocation in them) and by one fewer document hour. Week 10 document time is 3 hours, down from 5, so the DFD, STRIDE and role tables must be nearly final by the end of week 9. If a slice runs over, do not extend the week: use the overrun trigger and pace test.

## 5. Pace test and cut ladder

**Overrun trigger.** If any slice passes 125% of its estimate, run the pace test at once; do not wait for week 7 or 9.

**Pace tests.** End of week 7: are S2a and S2b done and M1 started? End of week 9: is S4 done? (S5 is a full 7 hours in week 10, so any S5 time already spent is a bonus.) If not, apply the ladder below immediately, in order, until the plan fits. Record each cut in the decision log and limitations register.

| Rung | Cut | Effect on criteria |
|---|---|---|
| C-1 | Dashboard reduced to the complaint list with an overdue filter | None |
| C-2 | Later routine updates not generated; the scheduled check still flags overdue items | SC-02 partly met; disclose |
| C-3 | Correspondence reduced to acknowledgement and final response; no progress updates or unresolved notification; day-40 outcome records answered or breached only | SC-05 partly met; disclose. Follows the lecturer's advice to cut correspondence before approval or audit |

Nothing in the protected core is cut. M1 in particular cannot be cut or pushed past S3, because the audit revocation and the send service's row lock need PostgreSQL. If C-3 is not enough, speak to the lecturer; do not cut the approval step.

## 6. Adding stretch features

1. Check start conditions (Core Spec Section 12): Must list works end to end, tests green on PostgreSQL, deployed, documents on plan, and the minimum viable demo (Section 9.2, steps 1 to 5) rehearsed cleanly.
2. Pick the next item in order. Read only the V0.8 sections named for it.
3. Follow the add-a-feature checklist (Section 8.6).
4. Report it in the write-up as an extra, and remove or amend its limitations entry.
5. Add a line to the Core Spec change log.

Time for stretch exists only if slices finish under estimate or you trade week-10 evidence time; never trade week 11. Expect one or two items at most. Receipt correction (ST-1) is the riskiest: start it only with about 8 clear spare hours and build only the minimum in the Core Spec.

## 7. Keeping the limitations register and decision log as you go

### 7.1 Routine (about five minutes at the end of each slice)

1. Did I skip, simplify or defer anything from the Core Spec? If yes, add a register entry.
2. Did I make a decision a marker would ask about? If yes, add a decision-log line.
3. Is any open entry now wrong because I built the thing? If yes, amend or delete it.
4. Write 2–3 bullet notes for your own analysis: what I simplified and why, what a marker might question, what risk remains. Convert them to prose in week 11.

### 7.2 Formats

Register: `L-nn | what is missing or simplified | why | effect on the user or compliance position | source`
Decision log: `date | decision | reason | consequence`

Entries are **factual**. The analysis of limitations in the write-up is your own work and is not written by AI.

### 7.3 Entries to add now

| ID | Entry |
|---|---|
| L-01 | No stakeholder validation has taken place (replace with the real review if one happens) |
| L-02 | Day-of-receipt exclusion and first-submission completion proxy are adopted, unverified conventions |
| L-03 | Only log-only transport unless ST-4 is built: "sent" means recorded in the outbox, not emailed |
| L-04 | Receipt date cannot be corrected in the application unless ST-1 is built |
| L-05 | Reviewer-shopping: any compliance user may decide a resubmission |
| L-06 | No reviewer cover; single-value roles |
| L-07 | Handler absence leaves no cover unless ST-7 is built |
| L-08 | Inbound correspondence is not captured |
| L-09 | Ombudsman referral status is not modelled |
| L-10 | Regulation 107 analysis is out of scope |
| L-11 | Retention period unverified; no deletion feature |
| L-12 | Correction and erasure conflict with immutable messages, approval hashes and the audit table |
| L-13 | Day-40 outcome (a) is stricter than the final-response milestone due date; outcome (b) is an ordering outcome and lateness is a derived indicator |
| L-14 | No password reset or MFA; login throttling only if ST-2 is built |
| L-15 | Anyone with database or hosting credentials can read data outside the application |
| L-16 | Closed cases cannot be reopened and no discretionary closure exists |
| L-17 | Template wording is short placeholder text and has not had legal or compliance review |
| L-18 | Until M1, audit entries are protected by application code only; database-level revocation exists from M1. Not a limitation of the delivered build: delete this entry when M1 is done (Core Spec 9.1) |

Decision-log lines to add now: database staged as sample data, then SQLite, then PostgreSQL at M1, following the lecturer's SQLite instruction; repository layer chosen so each switch changes one file per feature; PostgreSQL required because SQLite has no roles or privilege revocation; deployment deferred from S0 to D1 and D1 moved after M1.

If the cut ladder is used, add the matching entry (C-1 to C-3) at once.

## 8. Rules for the AI builder

### 8.1 Principle

Build so that a feature can be added, changed or removed by touching **one folder and one registration line**. Use plain structure, not frameworks: no plugin registry, no dependency-injection container, no event bus, no configuration-driven workflow, and no abstraction before two call sites.

### 8.2 Structure

```
app/
  __init__.py        # application factory; ONE explicit FEATURES list
  config.py          # all enumerations, status values, tunables, DATABASE_URL
  sample_data.py     # synthetic records for S0; loaded by the seed command from S2b
  core/              # database setup (from S1), auth helpers, audit service, clock, errors
  deadlines/         # pure functions only; no database access
  transport/         # send(message): log-only now; email later
  features/
    auth/  complaints/  investigation/  approvals/
    correspondence/  milestones/  closure/  automations/
  cli.py             # provision-user, deactivate-user, load-holidays, deadline-check, seed
migrations/          # from S1
tests/               # cross-cutting tests only (security, PostgreSQL, negative access)
```

Each feature folder has `routes.py`, `services.py`, `repository.py`, `templates/`, `tests/` and `register(app)`, plus `models.py` from the slice that introduces its tables. **Removing a feature means deleting its folder and its line in FEATURES.**

### 8.3 Dependency rules

1. Dependencies run routes → services → repositories (→ models, from S1). No rule logic in routes, templates or repositories.
2. A feature calls another feature only through that feature's public `services` module, never its models or internals. Shared code lives in `core/`. No circular imports.
3. `deadlines/` takes dates and returns dates. No database, no clock.
4. Routes never write an entity directly; the named service writes inside a transaction, and repositories never commit.
5. **No GET request writes data.**
6. A later slice adds new folders and edits earlier code only at join points: `config.py`, the FEATURES list, new migrations, and public service calls. It never restructures an earlier slice. If it seems to need to, stop and ask.
7. No string literals for statuses, types or roles in logic.
8. Services never import `sample_data`, the database session or models; only repositories do. Repository functions keep the same names, arguments and returned field names in every database stage (Section 3.3).

### 8.4 Schema and data

1. From S1, every schema change goes through an Alembic migration, generated then reviewed by hand. No manual DDL. Migrations use batch mode on SQLite and must run on both SQLite and PostgreSQL until M1; after M1 only PostgreSQL is supported.
2. Models and migrations are the single source of truth. Generate the ERD and a data dictionary from the models and regenerate after each migration. Do not draw them by hand.
3. Enumerations are validated text columns, validated in services; CHECK constraints are welcome.
4. Foreign keys, uniqueness and NOT NULL rules are in the database, not only in code.
5. Seed data is synthetic: about eight complaints across all states, including one near day 40 and one overdue. In S0 it is `app/sample_data.py`; from S2b a documented seed command loads the same records into the database.
6. The audit revocation is applied through the owner role at M1 and has a test.

### 8.5 Code quality

- Small functions, type hints on public functions, short docstrings that cite the rule ID, for example `# R-ORDER-01`.
- One `now()` function in `core/` used everywhere, so tests can set the date.
- Services own the transaction boundary. Before S1 the in-memory store has no transactions; the one-transaction rules (A-2, send service) are first built on a database from S2b.
- Specific errors; no silent `except`. A denial raises a typed error that the route maps to a response **and** writes an audit event.
- No secrets in code, logs, tests or prompts. **No real personal data in any AI prompt.**
- No dead code and no speculative hooks. Delete rather than comment out.
- Add a dependency only if it removes more code than it adds.

### 8.6 Checklist: adding a feature

1. Confirm it is in scope (Must or a listed stretch item).
2. Create `features/<name>/` with routes, services, models, templates, tests.
3. Add its migration; regenerate the ERD and data dictionary.
4. Add its rows to the role table and enforce them in the service.
5. Add its audit events.
6. Add STRIDE rows and refresh the DFD for any new boundary-crossing flow.
7. Add tests naming the rule IDs.
8. Add its single line to FEATURES.
9. Update the limitations register, decision log, AI log and Core Spec change log.

### 8.7 Checklist: removing a feature

1. Delete the folder and its FEATURES line.
2. Add a migration only if data or columns must go.
3. Remove its tests, role-table rows, STRIDE rows and screens.
4. Add a limitations entry and a decision-log line.
5. Run the full suite.

### 8.8 Testing and Git

- Write tests alongside each slice. Deadline tests come first. A fake transport in automated tests; the log-only transport is the default.
- Before M1 the suite runs on the current stage (in-memory, then SQLite). From M1 the full suite runs against PostgreSQL, and a test that passed before M1 must pass unchanged after it.
- Small commits; one slice per branch; messages say what changed and flag "AI-assisted".
- Never weaken or delete a test to make a build pass; raise it.

### 8.9 Prompt header (paste at the start of every session)

> You are building the Complaints App. Read the current **Core Spec** and **Build Plan**; the Core Spec defines what to build. Work only on the current slice: **[slice]**. Current database stage: **[sample data / SQLite / PostgreSQL]**. Follow Build Plan Sections 3.3 and 8: one folder per feature, routes → services → repositories → models, pure deadline functions, all enumerations in `config.py`, a migration for every schema change, no GET writes, tests alongside, rule IDs in tests and comments. Use synthetic data only. Do not add features outside the Core Spec. If anything is ambiguous or the documents conflict, stop and ask me. At the end, list what you built, what you skipped or simplified, and any limitation or decision I should record.

## 9. Documents, evidence and demo

### 9.1 Submission pack (Moodle)

A link to the deployed app; a link to the GitHub repository; one PDF or Word write-up of about 2,500 words with the cover page and the AI Fluency declaration appendix; lecturer test accounts for each role.

**Repository must contain:** source, README with local run steps, Dockerfile, passing tests, scan output with recorded responses, deployment documentation sufficient to redeploy, governance policy, ERD, DFD, STRIDE table, role table, GDPR write-up, limitations register, accessibility review, AI log, decision log with the hindsight decision, screenshots and test runs for the three automations.

**You write yourself (AI may not write these):** design-decision analysis, security findings discussion, accessibility review, limitations discussion. The defended next step is also yours.

### 9.2 Non-technical live demo (about 8 minutes)

Tell it as a story, not a feature tour. Avoid rule IDs and internal terms.

1. A complaint arrives; the handler logs it with the real receipt date; the deadlines appear.
2. Show a countdown near day 40 and what the system says to do.
3. The handler investigates and submits the outcome; the reviewer sees exactly what was submitted, returns it with a comment, then approves the resubmission.
4. The final response goes out (recorded in the outbox); the case closes.
5. Show the audit trail and prove a handler cannot see or approve another case.
6. (If ST-1 is built) correct a mistyped receipt date and show the deadlines move.
7. State the recommended next step (invest, iterate, hand to developers, or shelve) and defend it with what you found: what works, what is missing, and what the unverified conventions mean.

A recorded backup of the demo is worthwhile as a fallback but not required.

### 9.3 Early actions that cost little

- Send the one-page scope (Core Spec Section 1) to the lecturer this week, and ask whether extras beyond the criteria are acceptable.
- Arrange one real conversation with a complaints handler or similar, even 20 minutes with screenshots, so L-01 can be replaced.
- Verify the regulation table (Core Spec Section 11) before slice S2a.
- Verify the hosting claims in the provider's own documentation (two database roles, scheduled jobs, monitoring) before M1 (by the end of week 7), so the host is known to support PostgreSQL with two roles before you rely on it. Record in the decision log: the deferral of deployment from S0 to D1, D1 moving to after M1, and the staged database.

## 10. Change log

| Version | Date             | Change                                                                                                                                                                                                                                                                                                      |
| ------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 11 November 2026 | Initial build plan for Core Spec V1.0. Replaces Build Addendum A1.1.                                                                                                                                                                                                                                        |
| 1.1     | 11 November 2026 | Added overrun trigger; S0 definition of done and evidence folders; state-transition test table first and return-after-approval last in S3; short generic templates; second scan and early accessibility check in week 8; minimum viable demo gate; ST-1 caution; analysis notes in the slice routine; L-17. |
| 1.2     | 11 November 2026 | Local-first development: deployment moved from S0 to a separate step D1 (end of week 6); hosting research added to S0; weekly plan re-timed (week-7 buffer used); pace tests adjusted; hours now about 37 build and 29 documents.                                                                           |
| 1.3     | 11 November 2026 | Staged database: S0 on in-memory sample data behind per-feature repository modules, S1 to S2b on SQLite, PostgreSQL from new step M1 (week 8, before S3) because SQLite has no roles or privilege revocation. S0 simplified (virtual environment and `flask run`, no Docker or Alembic); S1 loses audit revocation; D1 moves to week 8; new Section 3.3; rules 8.2 to 8.9 updated; L-18 added; weekly plan re-timed with no slack; hours now about 38 build and 28 documents. |
