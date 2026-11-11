# Complaints App — Build Plan V1.0

**Version:** 1.0 — 11 November 2026
**Applies to:** Core Spec V1.0.
**Precedence:** The Core Spec defines what to build. This plan defines how, in what order, and how to keep records as you go. If they conflict, the Core Spec wins and the owner is asked.

## 0. Using this plan

- Give the AI builder **Core Spec V1.0 and this plan** every session. Give it only the V0.8 sections named in a stretch item, never the whole of V0.8.
- Work one slice at a time (Section 3). A slice is finished only when its checklist (Section 3.2) is ticked.
- The builder stops and asks if the documents conflict or anything is ambiguous.
- Spec changes go in the change log at the end of the Core Spec. Nothing gets rewritten in place.

## 1. Constraints and assumptions

| Item | Assumption |
|---|---|
| Deadline | End of week 11, 11:59 pm, which you place in the first week of January 2027. Confirm the exact date on the timetable. Live demonstration in week 12 |
| Late penalty | 10% of the mark for up to 5 calendar days late, then 0. Treat this as a safety net only |
| Time | 10 hours a week, separate from class sessions. Week 5 is partial (about 6 hours). Total about 66 hours |
| Split | About 36 hours build and test, about 30 hours documents and evidence |
| Freeze | End of week 10. Week 11 is documents and submission only |
| Christmas | Assumed to fall between week 10 and week 11. If your break hits earlier, tell me and the weeks move |

Class practicals run the same project (data model in session 5, interface 6, tests 7, scan 8, Dockerfile 9, deployment 10, governance 11). Use them to review the matching item, but do not wait for them. This plan runs ahead of them.

## 2. Marks and where the hours go

The Core Spec maps rubric to criteria. The takeaway for time: about 60 of 100 marks come from repository evidence, responsible development and communication, which do not need complex rules. A smaller app that works, is deployed, is tested and is well evidenced beats a larger one that is not.

**Protected core (never cut):** the approval step with snapshot, the audit trail with database revocation, the deadline engine and its tests, role enforcement on the data, the three automations, deployment, tests, the scan response and the documents.

## 3. Build slices

### 3.1 Slices

| Slice | Content | Hours |
|---|---|---|
| **S0 Baseline** | Repository; Flask application factory; one configuration module; Docker Compose with PostgreSQL owner and application roles; Alembic; pytest; hosting decision (needs a scheduled CLI job, two database roles and a monitoring tool); `/health`; **deploy the skeleton**; first scan run | 4 |
| **S1 Foundations** | User model; login, logout, CSRF, secure cookies, idle expiry; role checks in services; audit service; revocation of UPDATE and DELETE on the audit table with its test; `provision-user` CLI; wrong-role direct-request tests | 5 |
| **S2a Deadline engine** | **Tests first.** Holiday dataset with the Good Friday and Easter Monday test; pure working-day module; the two worked examples; weekends, October holiday, year boundary, late-Friday receipt, day-40 boundary | 3 |
| **S2b Intake and milestones** | Complaint, Milestone and Correspondence (draft) models; intake form and route; milestones and acknowledgement draft created in one transaction (automation A-2); complaint list and detail; countdown display with text status | 6 |
| **S3 Investigation and approval** | Investigation save; final-response draft; `submit-outcome` with snapshot, hash and first-submission rules; approval queue and decision (automation A-3); return and invalidation; state machine; immutability and self-approval tests | 6 |
| **S4 Outbox** | Templates with mandatory content; composer and preview; `send()` with the log-only transport; allowlist; send service transaction; milestone completion; ordering rule R-ORDER-01 | 5 |
| **S5 Closure and scheduled check** | Closure gates, day-40 outcome, waivers; routine milestone generation; `deadline-check` CLI with `ScheduledRun` and digest (automation A-1); simple dashboard | 7 |

Total about 36 hours.

### 3.2 "Done" checklist for every slice

- [ ] Tests for the slice pass against PostgreSQL.
- [ ] Each rule ID touched has a test that names it.
- [ ] State changes, denials and sends write audit events.
- [ ] New boundary-crossing flows have STRIDE rows.
- [ ] Limitations register and decision log updated (Section 7).
- [ ] AI log updated: prompts verbatim, what was accepted, modified or rejected.
- [ ] Small commits made, AI-assisted code flagged in the message.
- [ ] App starts from a clean checkout with Docker Compose.

## 4. Weekly plan

| Week | Build (hours) | Documents and evidence (hours) | Exit check |
|---|---|---|---|
| **5** (part) | S0 (4) | Send Core Spec page 1 to the lecturer; start the regulation table (Core Spec Section 11); start the AI log (2) | Skeleton deployed; first scan recorded |
| **6** | S1 (5), S2a (2) | DFD draft; STRIDE skeleton listing F-1 to F-8; **finish regulation table before S2a closes** (3) | Auth, audit revocation and deadline tests pass |
| **7** | S2b (6), plus 1 buffer | Role/CRUD table draft; GDPR draft (3) | Intake works. **Pace test** (Section 5) |
| **8** | S3 (6), S4 start (1) | Governance policy draft; limitations entries (3) | Approval loop works end to end |
| **9** | S4 finish (4), S5 start (3) | STRIDE rows completed for built flows (3) | Outbox works; **Must list demonstrable by end of week 10 at the latest** |
| **10** | S5 finish (4). **Stretch only if ahead** | ERD generated; DFD final; STRIDE final; scan re-run with responses; accessibility review and 375 px check (6). **Feature freeze at end of week** | Tests and scans green on PostgreSQL |
| **11** | None | Write-up; GDPR final; governance policy; runbook; AI declaration; cover page; clean-checkout redeploy check; submission pack (10) | Submitted |

Weeks 6 to 9 are 7 build hours plus 3 document hours. If a slice runs over, do not extend the week: use the pace test.

## 5. Pace test and cut ladder

**Pace tests.** End of week 7: is S2b done? End of week 9: is S5 at least half done? If not, apply the ladder below immediately, in order, until the plan fits. Record each cut in the decision log and limitations register.

| Rung | Cut | Effect on criteria |
|---|---|---|
| C-1 | Dashboard reduced to the complaint list with an overdue filter | None |
| C-2 | Later routine updates not generated; the scheduled check still flags overdue items | SC-02 partly met; disclose |
| C-3 | Correspondence reduced to acknowledgement and final response; no progress updates or unresolved notification; day-40 outcome records answered or breached only | SC-05 partly met; disclose. Follows the lecturer's advice to cut correspondence before approval or audit |

Nothing in the protected core is cut. If C-3 is not enough, speak to the lecturer; do not cut the approval step.

## 6. Adding stretch features

1. Check start conditions (Core Spec Section 12): Must list works end to end, tests green on PostgreSQL, deployed, documents on plan.
2. Pick the next item in order. Read only the V0.8 sections named for it.
3. Follow the add-a-feature checklist (Section 8.6).
4. Report it in the write-up as an extra, and remove or amend its limitations entry.
5. Add a line to the Core Spec change log.

Time for stretch exists only if slices finish under estimate or you trade week-10 evidence time; never trade week 11. Expect one or two items at most.

## 7. Keeping the limitations register and decision log as you go

### 7.1 Routine (two minutes at the end of each slice)

1. Did I skip, simplify or defer anything from the Core Spec? If yes, add a register entry.
2. Did I make a decision a marker would ask about? If yes, add a decision-log line.
3. Is any open entry now wrong because I built the thing? If yes, amend or delete it.

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

If the cut ladder is used, add the matching entry (C-1 to C-3) at once.

## 8. Rules for the AI builder

### 8.1 Principle

Build so that a feature can be added, changed or removed by touching **one folder and one registration line**. Use plain structure, not frameworks: no plugin registry, no dependency-injection container, no event bus, no configuration-driven workflow, and no abstraction before two call sites.

### 8.2 Structure

```
app/
  __init__.py        # application factory; ONE explicit FEATURES list
  config.py          # all enumerations, status values, tunables
  core/              # database setup, auth helpers, audit service, clock, errors
  deadlines/         # pure functions only; no database access
  transport/         # send(message): log-only now; email later
  features/
    auth/  complaints/  investigation/  approvals/
    correspondence/  milestones/  closure/  automations/
  cli.py             # provision-user, deactivate-user, load-holidays, deadline-check
migrations/
tests/               # cross-cutting tests only (security, PostgreSQL, negative access)
```

Each feature folder has `routes.py`, `services.py`, `models.py`, `templates/`, `tests/` and `register(app)`. **Removing a feature means deleting its folder and its line in FEATURES.**

### 8.3 Dependency rules

1. Dependencies run routes → services → models. No rule logic in routes or templates.
2. A feature calls another feature only through that feature's public `services` module, never its models or internals. Shared code lives in `core/`. No circular imports.
3. `deadlines/` takes dates and returns dates. No database, no clock.
4. Routes never write an entity directly; the named service writes inside a transaction.
5. **No GET request writes data.**
6. A later slice adds new folders and edits earlier code only at join points: `config.py`, the FEATURES list, new migrations, and public service calls. It never restructures an earlier slice. If it seems to need to, stop and ask.
7. No string literals for statuses, types or roles in logic.

### 8.4 Schema and data

1. Every schema change goes through an Alembic migration, generated then reviewed by hand. No manual DDL.
2. Models and migrations are the single source of truth. Generate the ERD and a data dictionary from the models and regenerate after each migration. Do not draw them by hand.
3. Enumerations are validated text columns, validated in services; CHECK constraints are welcome.
4. Foreign keys, uniqueness and NOT NULL rules are in the database, not only in code.
5. Seed data is synthetic and loaded by a documented command: about eight complaints across all states, including one near day 40 and one overdue.
6. The audit revocation is applied through the owner role and has a test.

### 8.5 Code quality

- Small functions, type hints on public functions, short docstrings that cite the rule ID, for example `# R-ORDER-01`.
- One `now()` function in `core/` used everywhere, so tests can set the date.
- Services own the transaction boundary.
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
- The full suite runs against PostgreSQL.
- Small commits; one slice per branch; messages say what changed and flag "AI-assisted".
- Never weaken or delete a test to make a build pass; raise it.

### 8.9 Prompt header (paste at the start of every session)

> You are building the Complaints App. Read **Core Spec V1.0** and **Build Plan V1.0**; the Core Spec defines what to build. Work only on the current slice: **[slice]**. Follow Build Plan Section 8: one folder per feature, routes → services → models, pure deadline functions, all enumerations in `config.py`, a migration for every schema change, no GET writes, tests alongside, rule IDs in tests and comments. Use synthetic data only. Do not add features outside the Core Spec. If anything is ambiguous or the documents conflict, stop and ask me. At the end, list what you built, what you skipped or simplified, and any limitation or decision I should record.

## 9. Documents, evidence and demo

### 9.1 Submission pack (Moodle)

A link to the deployed app; a link to the GitHub repository; one PDF or Word write-up of about 2,500 words with the cover page and the AI Fluency declaration appendix; lecturer test accounts for each role.

**Repository must contain:** source, Dockerfile, passing tests, scan output with recorded responses, deployment documentation sufficient to redeploy, governance policy, ERD, DFD, STRIDE table, role table, GDPR write-up, limitations register, accessibility review, AI log, decision log with the hindsight decision, screenshots and test runs for the three automations.

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

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 11 November 2026 | Initial build plan for Core Spec V1.0. Replaces Build Addendum A1.1. |
