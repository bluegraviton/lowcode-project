# Complaints App — Core Spec V1.0

**Version:** 1.0 — 11 November 2026
**Status:** Active. Replaces Specification V0.8 and Build Addendum A1.1, which are archived. V0.8 is kept only as a design reference for the stretch items in Section 12.
**Companion document:** Build Plan V1.0.

## 0. How to read this document

- **Section 1 is the one-page scope** (problem, users, MVP, success criteria, plan) and is the version to send to the lecturer. The success criteria in Section 1 are fixed from the date of this document.
- Sections 2 to 11 hold the rules and design the builder implements.
- Section 12 lists pre-registered stretch items that may be added if the build goes faster than planned.
- Rule IDs (R-…) reuse V0.8 names where the meaning is the same. **The definitions in this document win.** V0.8 text does not apply to the core build.
- If anything is ambiguous or conflicts, the builder stops and asks the project owner.

---

## 1. One-page scope

### 1.1 Problem

A small Irish regulated insurance intermediary tracks consumer complaints in a spreadsheet and keeps evidence in an inbox. Under the Consumer Protection Code 2025 it must acknowledge, update, investigate and answer complaints within working-day deadlines, and it must keep a complaint log. Errors in counting working days, a missing independent check on the outcome, and the lack of an audit trail are the real risks. The application is an internal web app that replaces the spreadsheet with a controlled case record, calculated deadlines, an independent approval step for the final response, an outbox of correspondence and an audit trail.

It is a coursework prototype, not a certified compliance product. All data is synthetic. No stakeholder validation has yet taken place (see the limitations register in the Build Plan).

### 1.2 Users

- **Handler:** logs and investigates assigned complaints, drafts and sends correspondence. The only role that creates complaints.
- **Compliance reviewer:** reads all cases, approves or returns the final response, cannot handle cases.
- Complainants have no account and no portal.

### 1.3 MVP ("Must" list)

1. Login with two roles, enforced on the data.
2. Intake with an actual receipt date, locked after intake.
3. Deadline engine: working days, holidays, milestones, countdown display.
4. Investigation record: findings, root cause, outcome, rationale, redress.
5. Independent approval of the final response: snapshot, return with comment, resubmission.
6. Append-only audit trail.
7. Outbox: four message types logged, with an allowlist and fixed templates.
8. Closure gates and the day-40 outcome.
9. Three automations: scheduled deadline check with staff digest, event-triggered intake, human approval step.
10. Docker and PostgreSQL deployment, tests, security scan and evidence pack.

### 1.4 Success criteria (fixed)

| ID | Criterion |
|---|---|
| SC-01 | **Complete journey.** With separate handler and reviewer accounts, complete intake → investigation → submission → independent approval → final response sent → closure. Each unmet closure gate is named in the refusal. |
| SC-02 | **Deadline engine.** Independently checked examples pass: weekends, the October public holiday, Good Friday, Easter Monday, a year boundary, a complaint received late on a Friday, and the day-40 boundary. Every seeded year contains Good Friday and Easter Monday. Completed milestones keep their due and completion dates. Later routine updates are created so updates beyond day 80 exist. |
| SC-03 | **Locked receipt date.** The actual receipt date and channel are captured separately from creation time, future dates are rejected, and the date cannot be edited after intake. |
| SC-04 | **Independent approval.** The reviewer decides an exact snapshot of the package. A return needs a comment. The decision is final. Approved content is immutable and any change needs an audited return. Self-approval is impossible. The final response cannot be sent, and the case cannot close, without valid approval. |
| SC-05 | **Outbox.** All four message types are logged with the template version. One send produces one record. An unresolved notification is refused once a final response has been sent. Real sending, if built, is restricted to allowlisted addresses. "Sent" is never described as "delivered". |
| SC-06 | **Audit trail.** The listed events (Section 10.2) are recorded. A test proves the application's database role cannot UPDATE or DELETE audit entries. |
| SC-07 | **Role-based access on the data.** Handlers reach assigned cases only and reviewers read all cases, enforced in services and scoped queries and proven by direct-request tests. A role table states create, read, update and delete for every entity and names the enforcement point. |
| SC-08 | **Three automations.** A scheduled deadline check with an idempotent digest, an event-triggered intake, and a human approval step, each with a screenshot and a successful test run. |
| SC-09 | **Model and diagrams.** An ERD generated from the implemented models; a level-1 DFD with trust boundaries; a STRIDE table covering every boundary-crossing flow, with a mitigation for each threat. Tests that implement a code mitigation carry the threat ID. |
| SC-10 | **Data protection.** A short GDPR write-up covering lawful basis, minimisation, retention period and who can see personal data. |
| SC-11 | **Delivery.** A deployed app reachable by the marker with persistent data; redeployable from documentation; tests pass against PostgreSQL; a security scan run with each finding's response recorded; incremental commit history; governance policy; honest accessibility review; AI log and declaration; the technical write-up. |

If a criterion is only partly met at the end, the write-up says so. Criteria are never edited to match what was built.

### 1.5 Plan summary

The build is about 36 hours in six slices (S0 to S5) alongside about 30 hours of documents, over weeks 5 to 11 at 10 hours a week. Features are frozen at the end of week 10. Week 11 is the write-up and submission. The week-by-week plan is in the Build Plan.

### 1.6 Out of scope

Public intake or portal, inbound email, AI classification or automated decisions, redress payments, multi-organisation use, case reopening after closure, automated retention deletion, the six-monthly pattern analysis (Regulation 107), native mobile apps.

---

## 2. Brief minimums and marking map

| Brief minimum | Where met |
|---|---|
| Data model, 3+ related tables, ERD | Section 7; SC-09 |
| Automations: scheduled, event, human approval | Section 8; SC-08 |
| Role-based access on the data, with role table | Section 3; SC-07 |
| Level-1 DFD | Section 10.4; SC-09 |
| STRIDE on every boundary-crossing flow | Section 10.4; SC-09 |
| GDPR write-up | Section 10.3; SC-10 |

| Rubric criterion | Marks | Mainly served by |
|---|---|---|
| Problem and tooling | 15 | Section 1.1; success criteria set now; platform justification in the write-up (draft in V0.8 Appendix A, "Platform choice") |
| Build quality | 25 | SC-01 to SC-05, SC-07, SC-08 |
| Repository, testing, scanning | 20 | SC-02, SC-06, SC-11 |
| Responsible development | 20 | SC-06, SC-07, SC-09, SC-10, SC-11 |
| Stakeholder communication | 20 | Write-up; non-technical live demo; defended next step (Build Plan, Section 9) |

---

## 3. Roles and permissions

Each user holds exactly one role. This structurally prevents self-approval. Accounts are created by CLI only. Permissions are enforced in services and scoped queries, never only by hiding screens. Denials are audited.

### 3.1 CRUD by entity

| Entity | Handler | Compliance reviewer | Writes performed by | Enforced in |
|---|---|---|---|---|
| Complaint | Create; read assigned; update investigation fields on assigned while `logged` or `investigating`; no delete | Read all; no direct update; no create; no delete | Complaint, investigation, approval and closure services | Scoped queries, service checks |
| Milestone | Read assigned; no direct write | Read all; no direct write | Complaint, correspondence, approval, closure and scheduled-check services | Service checks |
| Approval | Read assigned; creates by submitting | Read all; decide pending approvals | Approval service | Service and revision checks |
| Correspondence | Create and edit drafts on assigned; send on assigned; read assigned | Read all; no create, edit or send | Correspondence and approval services | Scoped queries, immutability rules |
| AuditEvent | Read assigned; no write, update or delete | Read all; no write, update or delete | Audit service and CLI append only | Scope plus database privilege revocation |
| User | Read own profile | Read own profile | CLI | CLI only |
| PublicHoliday | Read | Read | CLI loader | Read-only access |
| ScheduledRun | None | None | Scheduled CLI job | Operator access |

No role deletes any record. There is no delete route.

### 3.2 Routes

| Route | Handler | Reviewer | Service |
|---|---|---|---|
| `GET/POST /login`, `POST /logout` | Anonymous / yes | Anonymous / yes | Authentication |
| `GET /` dashboard | Assigned | All | Dashboard query |
| `GET /complaints` | Assigned | All | Scoped query |
| `GET /complaints/new`, `POST /complaints` | Yes | No | Complaint service (creates milestones and acknowledgement draft) |
| `GET /complaints/<id>` | Assigned | All | Case query |
| `POST /complaints/<id>/investigation` | Assigned | No | Investigation service |
| `POST /complaints/<id>/correspondence` | Assigned | No | Correspondence service (create draft) |
| `POST /correspondence/<id>/edit` | Assigned | No | Correspondence service |
| `GET /correspondence/<id>/preview` | Assigned | All | Preview renderer |
| `POST /correspondence/<id>/send` | Assigned | No | Send service |
| `POST /complaints/<id>/submit-outcome` | Assigned | No | Approval service |
| `GET /approvals` | No | Yes | Queue query |
| `POST /approvals/<id>/decision` | No | Yes | Approval service |
| `POST /complaints/<id>/return-to-investigation` | Assigned | Any | Approval service |
| `POST /complaints/<id>/close` | Assigned | Any | Closure service |
| `GET /health` | Public | Public | Minimal status, no data |
| CLI | | | `provision-user`, `deactivate-user`, `load-holidays`, `deadline-check` |

The CLI runs with operator credentials outside the application permission model. Each user change and scheduled run is audited. `deactivate-user` refuses to remove the last active reviewer or a handler with open cases. Only `/login` and `/health` are reachable without authentication.

---

## 4. Lifecycle and rules

States: **logged → investigating → pending_approval → approved → closed.** The first save of the investigation moves `logged` to `investigating`. A return moves the case back to `investigating`. Closed cases are read-only and cannot be reopened.

**R-APPROVAL-01 (Independent approval).** The final response needs approval by a reviewer of the exact package. This is a chosen internal control, not a statutory requirement, and the write-up must say so. Validity is checked at the decision, again when the final response is sent and again at closure.

**Submission.** `submit-outcome` is allowed from `investigating` when findings, root cause, outcome, rationale and redress are recorded and a complainant-addressed final-response draft exists. It creates an Approval row holding a snapshot of the investigation fields and the final-response recipient, subject and body, plus a SHA-256 hash, and moves the case to `pending_approval`. **The first submission** sets `completed_at` (the adopted proxy for investigation completion) and creates the final-response milestone. Later submissions never change either.

**Decision.** A reviewer approves or returns. A return needs a comment (**R-RETURN-01**). The decision is final: no appeal, no conditional approval. Any compliance user may decide a resubmission, including the reviewer who returned it (limitation). On approval the final response is authorised (`authorised_by`, `authorised_at`) and the case moves to `approved`.

**Return and invalidation.** A reviewer return sets `decision = returned` **and `invalidated_at`**, moves the case to `investigating` and increments `revision`. A handler or reviewer may also call `return-to-investigation` after approval, with a reason; this invalidates the approval. A *live* approval is pending or approved with `invalidated_at` null. **R-RETURN-02:** return-to-investigation is refused once the final response has been sent. Return never changes `completed_at`, the final-response milestone or its due date, so the final-response clock keeps running through rework.

**R-APPROVAL-02 (Approved content is immutable).** Investigation fields are editable only while `logged` or `investigating`. A final-response draft is editable only while it is a draft, has never been authorised and is not referenced by a live approval. An authorised final response is never edited. If the outcome must change after approval, the handler returns the case and composes a **new** final-response record; the old one remains as history. A stale submission or decision (revision mismatch) is rejected.

**R-ORDER-01 (Notification precedes final response).** Once any final response for the case has status `sent`, an unresolved notification cannot be sent.

**R-CLOSE-01 (Closure gates).** A case closes only when all hold, and a refusal names the failed gate:
1. Findings, root cause, outcome, rationale and redress are recorded for the current revision.
2. A reviewer approved the current revision, the approval is live, and the hash of the current final response matches the snapshot.
3. The final response has status `sent`.

**R-CLOSE-02 (Day-40 outcome).** At closure the service records one outcome, using the Europe/Dublin date of each timestamp:
- (a) `answered_in_time`: the final response was sent on or before the unresolved-notification due date (day 40);
- (b) `notified_before_outcome`: otherwise, the unresolved notification was sent (and so before the final response);
- (c) `breached`: otherwise.

Reading (a) is deliberately conservative: the final-response milestone due date can fall after day 40, so the countdown shows both dates and states "day-40 notification still required unless the final response is sent by day 40" where that applies. Outcome (b) is an ordering outcome and does not mean the notification was on time; the case page shows a derived "notification late" indicator when its completion date is after its due date. This is a recorded limitation.

**R-CLOSE-03 (Waivers).** At closure every still-open milestone is waived with a reason: `not_applicable` if its due date is on or after the date the final response was sent, otherwise `missed`. The service records the waiver with actor and time.

**Early resolution.** The prototype uses the normal journey for early-resolved complaints and records the receipt, outcome, response and closure dates. It does not model an expedited path.

---

## 5. Deadlines and milestones

**R-DATE-01 (Working day).** A working day is not a Saturday, a Sunday, Good Friday or a public holiday under the Organisation of Working Time Act 1997. Easter Monday is a public holiday and is excluded. Weekends are excluded by definition, so no "roll to Monday" logic exists.

**R-DATE-02 (Dates).** Timestamps are stored in UTC. Comparisons with a due date use the Europe/Dublin local date. The count starts on the **next working day after the day of receipt** (adopted, unverified), so a complaint received late on a Friday has day 1 on Monday (or the next working day if Monday is a holiday). The calculation is a pure function taking dates and a holiday set and returning a date. If a date falls beyond the loaded holiday range it raises an error rather than assuming a working day.

**Holiday data.** A version-controlled dataset covers the current and following year. A test asserts that every seeded year contains Good Friday and Easter Monday.

**Worked examples (fixtures).** Received Thursday 22 October 2026 with Monday 26 October a public holiday: five working days is Friday 30 October 2026. Received Wednesday 24 March 2027 with Good Friday 26 March and Easter Monday 29 March: five working days is Friday 2 April 2027.

### 5.1 Milestones

| Type | Due | Created |
|---|---|---|
| acknowledgement | receipt + 5 WD | At intake |
| progress_update, sequence n | receipt + 20n WD | n = 1 at intake; later ones as below |
| unresolved_notification | receipt + 40 WD | At intake |
| final_response | `completed_at` + 5 WD | Once, at first submission |

- **Later routine updates.** The next routine milestone is created when the previous one is completed, or by the scheduled check when the previous due date passes. None is created once a final response has been sent (**R-MILESTONE-03**). No page view writes data.
- **Completion (R-MILESTONE-01, -02).** Sending a complainant-addressed message completes one milestone. An acknowledgement, notification or final response completes the open milestone of its type. A progress update completes the open routine milestone with the highest sequence whose due date is on or before today, or the lowest sequence if none is due. If none is open, the message completes nothing. Due and completion dates both stay visible; a late completion does not erase lateness.
- **Display.** Every countdown shows label, exact due date, working days remaining or overdue, status and next action. Status uses text as well as colour. Examples: "Acknowledgement due in 2 working days — 13 November 2026"; "Acknowledged 12 November 2026 — within deadline". A return or resubmission never resets the final-response countdown.
- Milestones are never overwritten. Receipt correction (stretch ST-1) will supersede rather than overwrite.

---

## 6. Correspondence and outbox

**Types.** Acknowledgement, progress update, unresolved notification, final response. Any substantive outgoing message uses one of these, so none escapes the log. A request for further information is sent as a progress update. In the core build all messages are addressed to the complainant.

**Templates.** Fixed files in version control, selected by message type, with the template version stored on each message. Contact details for the Financial Services and Pensions Ombudsman are stored with the template version. Mandatory content:

| Type | Must contain |
|---|---|
| Acknowledgement | Reference and date received; complaint as understood; procedure and expected timeframe; named contact; referral right and contact details |
| Progress update | Reference; what has been done; what remains; next expected update; named contact |
| Unresolved notification | Reference; not yet resolved; anticipated timeframe; referral right and contact details |
| Final response | Reference; decision and reasons; offer, redress or settlement terms; referral right and contact details; referral time limit where applicable |

**Flow.** The acknowledgement draft is created at intake. The handler creates other drafts, previews and sends them. Statuses are `draft` and `sent`. The `send` action is the confirmation.

**Send service (one transaction).** Lock the complaint row, then check: permission (assigned handler); case not closed; for a final response, the live approval and matching hash (**R-APPROVAL-01**); R-ORDER-01; allowlist when real sending is on (**R-SEND-07**). Then call the transport, set `sent` with `sent_at`, record the transport, complete the eligible milestone and write the audit event. Any failed check is refused and audited. Authorisation freezes content (**R-SEND-02**): a sent message is never edited.

**Transport.** One `send(message)` function with a swappable implementation. The core build ships the **log-only** transport: the message is recorded in the outbox and nothing is emailed, and the record says so (`transport = log`). "Sent" means recorded by the transport. It never means delivered or read (**R-SEND-08**). Real email is stretch ST-4 and must be built with the failure handling described there.

**Allowlist.** Only allowlisted addresses may receive real email. No unrestricted CC or BCC. Content carries a demonstration notice. Credentials are kept in the environment, never in Git, logs or AI prompts.

---

## 7. Data model

Logical model of eight tables. Enumerations are validated text columns defined in one configuration module. The ERD and a data dictionary are generated from the models.

- **User:** id (PK), name, email (unique), password_hash, role (`handler`/`compliance`), active, created_at.
- **Complaint:** id (PK), reference (unique, generated), handler_id (FK User), complainant_name, complainant_email, complainant_phone (optional), received_date, received_channel (`email`/`phone`/`letter`/`in_person`/`other`), receipt_note, product, category (validated enumerations), description, status, findings, root_cause_category, outcome (`upheld`/`partially_upheld`/`not_upheld`), outcome_rationale, redress_amount (decimal ≥ 0, default 0), revision (default 1), completed_at, day40_outcome, closed_at, created_at, updated_at. `received_date` has no update path in the core build.
- **Milestone:** id (PK), complaint_id (FK), type, sequence, due_date, completed_at, completed_correspondence_id (FK Correspondence, optional), waived_at, waived_reason (`not_applicable`/`missed`), created_at. Unique on (complaint_id, type, sequence).
- **Approval:** id (PK), complaint_id (FK), final_response_id (FK Correspondence; the only approval link), revision, reviewer_id (FK User, null until decided), decision (`pending`/`approved`/`returned`), comment (write-once after decision), submission_note (write-once after decision), package_snapshot (JSON), content_hash, submitted_at, decided_at, invalidated_at, created_at.
- **Correspondence:** id (PK), complaint_id (FK), message_type, recipient_type (`complainant`), recipient_email, subject, body, template_version, status, authorised_by_id (FK User), authorised_at, sent_by_id (FK User), sent_at, transport (`log`/`email`), created_at. Holds no milestone or approval reference.
- **AuditEvent:** id (PK), complaint_id (FK, optional), actor_id (FK, optional for system and CLI), action, change_details (JSON), created_at. Append-only.
- **PublicHoliday:** id (PK), date, name, calendar. Unique on (date, calendar).
- **ScheduledRun:** id (PK), job_name, period_key, status (`started`/`succeeded`/`failed`), started_at, finished_at, item_count, error_summary. Unique on (job_name, period_key).

Each link is stored once: approval to final response on `Approval.final_response_id`, milestone completion on `Milestone.completed_correspondence_id`. Merging complainant and investigation fields into Complaint is a deliberate simplification, recorded in the decision log. Message bodies and findings also hold personal data.

---

## 8. Automations

| ID | Automation | Behaviour | Evidence |
|---|---|---|---|
| A-1 | **Scheduled** deadline check (`deadline-check` CLI, daily) | Creates routine milestones that have become due, flags overdue items, writes a `ScheduledRun` row keyed by job and period (a repeat for the same period creates no duplicate), and sends a staff digest of references and counts, with no narrative, to one allowlisted address. A failed period can be re-run and updates the existing row. | Screenshot of the run, the `ScheduledRun` row, the digest; test |
| A-2 | **Event-triggered** intake | `POST /complaints` creates the complaint, the acknowledgement, first progress-update and unresolved-notification milestones, and the acknowledgement draft in one transaction. | Screenshot of the case and milestone panel; test |
| A-3 | **Human approval** | Submission places the package in the reviewer queue and blocks release of the final response until a reviewer decides. | Screenshot of queue, decision and audit entries; test |

Nothing substantive is sent to a complainant because a timer fired. The scheduled check prompts a human.

---

## 9. Architecture rules

1. Routes validate input and delegate. Services hold business rules and transactions. Models hold persistence. No rule logic in routes or templates.
2. Deadline rules are pure functions in one module, with no database access.
3. All enumerations, status values and tunables live in one configuration module.
4. One folder per feature, registered explicitly in one place, so a feature can be added or removed by touching one folder and one line.
5. The email transport is one function with swappable implementations (log-only now).

Stack: Python, Flask, PostgreSQL, Docker Compose, Flask-SQLAlchemy, Alembic, Flask-Login, Flask-WTF, pytest, Gunicorn. Server-rendered Jinja templates, one responsive CSS framework, checked once at 375 CSS pixels. Every schema change is a migration. No plugin registry, dependency-injection container or event bus; no abstraction before two call sites. The detailed builder rules are in the Build Plan.

---

## 10. Security, privacy and audit

### 10.1 Security controls

- **R-SEC-01:** password hashing, CSRF on every POST, secure cookie and session settings, idle expiry, server-side validation.
- **R-SEC-02:** authorisation in services and scoped queries, with tests proving a direct request from the wrong user fails.
- **R-SEC-03:** the audit table's UPDATE and DELETE privileges are revoked from the application's database role, with a test. The migration owner role is separate. The hosting choice must support two database roles.
- Secrets come from the environment and never go into Git, logs or AI tools. Operational logs are separate from audit evidence and hold no narrative.

### 10.2 Audit events

Case creation; state transitions; submissions; decisions; returns and invalidations; closure with day-40 outcome and waivers; sends and refusals; permission denials; failed logins; CLI user changes; scheduled-run results.

### 10.3 Privacy

- Synthetic data only. The production lawful basis is described in the GDPR write-up, written by the student from the Central Bank and data protection sources.
- Minimisation: only the fields in Section 7 are collected; narrative is excluded from the digest and from logs.
- Visibility: handlers see personal data on assigned cases, reviewers on all cases, nobody else.
- Retention: six years from closure is proposed and unverified; no deletion feature exists.
- Correction and erasure are manual operator actions and conflict with immutable messages, approval hashes and the append-only audit table. State this.
- Real personal data must not go into AI prompts.

### 10.4 DFD and STRIDE scope

External entities: handler and reviewer browsers, the complainant (recipient), the operator (CLI and scheduler), and the email provider if ST-4 is built. Processes: web application, send service, scheduled job. Data stores: PostgreSQL, template files, environment configuration. Trust boundaries: browser to application, application to database, application to email transport, operator to host and database. Boundary-crossing flows for STRIDE (add rows if stretch items add flows):

| Flow | Description |
|---|---|
| F-1 | Login credentials, browser to application |
| F-2 | Case data entry and display, browser and application |
| F-3 | Approval decisions, reviewer browser to application |
| F-4 | Application to database, reads and writes |
| F-5 | Outbound message to the complainant through the transport |
| F-6 | Staff digest through the transport |
| F-7 | Operator CLI to database (provisioning, scheduled check) |
| F-8 | Environment secrets to application |

---

## 11. Regulation verification table

A lecturer note says the AI-drafted regulatory summary must be confirmed against the source. **Nothing below is treated as verified until the status box is ticked with a paragraph reference.** Sources: S.I. No. 81 of 2025 and the Central Bank's published Consumer Protection Code 2025 pages, as listed in V0.8 Appendix B.9. Expect about an hour. These rows become the basis of the success criteria, so confirm them before slice S2.

| # | Statement the app relies on | Used in | Source reference found | Verified |
|---|---|---|---|---|
| V-01 | Working day excludes Saturday, Sunday, Good Friday and public holidays (Organisation of Working Time Act 1997) | R-DATE-01 | | ☐ |
| V-02 | Acknowledge within 5 working days of receipt, with required content | Milestones, template | | ☐ |
| V-03 | Progress updates at intervals no greater than 20 working days from receipt | Routine milestones | | ☐ |
| V-04 | Investigate and make reasonable efforts to resolve within 40 working days | R-CLOSE-02 | | ☐ |
| V-05 | If unresolved at 40 working days, notify anticipated timeframe, referral right and ombudsman contact | Notification template | | ☐ |
| V-06 | Final response within 5 working days of completion of the investigation, with required content | Final-response milestone, template | | ☐ |
| V-07 | Complaint resolved to satisfaction within 5 working days: procedure need not apply, log still kept | Early-resolution note | | ☐ |
| V-08 | Complaint log fields (Regulation 106) | Complaint record | | ☐ |
| V-09 | Day of receipt is not counted (**adopted convention**) | R-DATE-02 | | ☐ confirm or disclose |
| V-10 | First submission for approval stands in for completion of investigation (**adopted convention**) | Final-response milestone | | ☐ confirm or disclose |
| V-11 | Independent approval is an internal control, not a statutory duty | Write-up | | ☐ |
| V-12 | Retention of six years from closure (**proposed**) | GDPR write-up | | ☐ |
| V-13 | Current ombudsman name and contact details | Templates | | ☐ |

---

## 12. Stretch list and rules for growing the scope

Scope is allowed to grow, but only this way: the success criteria in Section 1.4 are fixed; stretch items are pre-registered here; anything built beyond the criteria is reported in the write-up as an **extra**, never as a criterion met. Confirm with the lecturer that this is acceptable.

**Start a stretch item only when** the Must list works end to end, tests pass on PostgreSQL, the app is deployed, and documents are on plan for that week. Work in this order. Each item follows the add-a-feature checklist in the Build Plan, including permissions, audit events, tests, STRIDE rows, a DFD update and a limitations update.

| ID | Item | Est. hours | Design reference in V0.8 | Notes |
|---|---|---|---|---|
| ST-1 | **Receipt correction** (reviewer-only, preview, reason, supersede and recalculate milestones, carry over completions, audit) | 5 | Sections 5.5, 3.2; Addendum A-09 | Needs a migration for `superseded_at`. Gives the mistyped-date demo. |
| ST-2 | **Login throttling and lockout** | 2 | Sections 10.1, 11.3 | Strengthens the security evidence. |
| ST-3 | **CSV export of the register** (same scope and filters as the list, audited, no contact details) | 3 | Section 8 (S-CSV-EXPORT), Appendix B.5 | Supports the complaint-log obligation. |
| ST-4 | **Real email send with failure handling:** reserve an attempt record before the call, record the result, retry definite failures, flag stale sends | 8 | Sections 6.3, 6.4, 6.7; Addendum A-07 | Needs a SendAttempt table and a `failed` status. The email provider becomes a DFD entity. |
| ST-5 | **Corrective update after a receipt correction** | 3 | Sections 5.5, 4.4 | Requires ST-1. |
| ST-6 | **Insurer (provider) recipient type** | 3 | Sections 6.1, 6.2, 10.3 | Needs DFD, STRIDE and GDPR-disclosure updates. |
| ST-7 | **Handler reassignment and user administration** | 3 | Sections 3.2, 11.3 | Operator CLI first, interface later. |
| ST-8 | **Case notes** | 2 | Section 11.3 | |

Not planned: page-render catch-up (a GET that writes data), internal staff notices, attachments, webhooks, queues, MFA, password reset.

Realistically the plan leaves room for **one or two** items. Choose by value per hour.

---

## 13. Lecturer feedback incorporated

| Feedback | Where |
|---|---|
| Check Consumer Protection Code timelines against the source; they become success criteria | Section 11; SC-02 |
| Working days are the bug area: tests first, including bank holidays and a late-Friday receipt | Section 5; SC-02; Build Plan slice S2 |
| Synthetic data only, including AI prompts | Sections 1.1, 10.3; Build Plan builder rules |
| Log outbound email to a table first; real send last | Section 6; ST-4 |
| If time is tight, cut correspondence history before approval or audit | Build Plan cut ladder; protected core |
| One-page scope with success criteria set now, MVP and weekly plan | Section 1; Build Plan |
| No public unauthenticated surface | Section 3.2 |

---

## 14. Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 11 November 2026 | New core specification extracted from V0.8 and Addendum A1.1, reduced to the brief's minimums, the rubric and the available hours. Adds regulation verification table, stretch list and lecturer feedback mapping. |
