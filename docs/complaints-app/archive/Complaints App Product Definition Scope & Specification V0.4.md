

# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.4 — 9 November 2026
Status: Minimum release defined and internally consistent. Regulatory rules remain
unverified pending the source register in Section 5.

## 1. Purpose

An internal web application for a small Irish regulated insurance intermediary. It
manages complaints from receipt through investigation, independent approval,
correspondence and closure, replacing a spreadsheet and disconnected email process
with a controlled case record, visible deadlines and an auditable history.

The application supports complaint handling under the Central Bank of Ireland
complaints-handling requirements. It is a coursework prototype, not a certified
compliance product. Legal obligations, chosen internal controls and prototype
limitations are distinguished throughout.

The essential product is accurate deadline tracking, independent approval,
correspondence sent through the application, and an audit trail.

## 2. Intended users and operating context

- One small Irish insurance intermediary.
- Single organisation; no multi-tenancy.
- Handlers investigate their assigned cases.
- Compliance reviewers independently decide outcomes and final responses.
- Accounts are provisioned by a documented command-line procedure performed by an
  operator with repository and hosting access. That operator privilege sits outside
  the application's permission model.
- Complainants have no account and no public portal.
- All records are synthetic. Real email is sent only to controlled test addresses.
- Desktop-first, responsive on smaller screens.

The application cannot prevent a person holding database or hosting credentials from
reading complaint data outside the application. No role or document statement claims
otherwise.

## 3. Scope boundary

One table defines what is committed, deferred and excluded. Sections elsewhere refer
to it rather than restating it.

| Capability | Status |
|---|---|
| Intake with actual receipt date and channel | Committed |
| Verified working-day deadline calculation | Committed |
| Milestone history with per-milestone due and completion dates | Committed |
| Countdown display with exact dates and text urgency | Committed |
| Investigation, outcome and redress recording | Committed |
| Independent approval and return with mandatory comment | Committed |
| Approval invalidation before any post-approval change | Committed |
| Four controlled correspondence types sent through the app | Committed |
| Outbox record, allowlist, failure and uncertainty handling | Committed |
| Repeated progress updates before and after the 40-working-day point | Committed |
| Scheduled deadline check with idempotent staff digest | Committed |
| Audit trail covering decisions, denials, sends and provisioning | Committed |
| Responsive main journey at 375 CSS pixels | Committed |
| Docker deployment against PostgreSQL | Committed |
| Receipt correction with authorisation and deadline recalculation | Optional |
| Handler reassignment | Optional |
| Browser-based user, role and holiday administration | Optional |
| Case notes as a separate record type | Optional |
| Delivery and bounce webhooks, provider reconciliation | Optional |
| Background queue and automated retry scheduling | Optional |
| Advanced reporting, charts and exports | Optional |
| Editable correspondence templates | Optional |
| Extended browser and device test coverage | Optional |
| Separate expedited early-resolution workflow | Optional |
| Public intake, complainant accounts, self-service portal | Out of scope |
| Inbound email ingestion and mailbox integration | Out of scope |
| Attachments and document uploads | Out of scope |
| AI classification, summarisation or automated decisions | Out of scope |
| Redress payment and finance or policy-system integration | Out of scope |
| Multi-organisation operation | Out of scope |
| Configurable workflow designer | Out of scope |
| Automated retention deletion | Out of scope |
| Native mobile applications, offline use, push notifications | Out of scope |
| Case reopening after closure | Out of scope |
| Regulatory certification or guaranteed compliance | Out of scope |

### Goals

1. Capture the actual receipt of a complaint accurately.
2. Calculate and display deadlines using verified rules.
3. Guide the handler through investigation and outcome preparation.
4. Prevent self-approval and premature closure.
5. Send case correspondence from the app and log it automatically.
6. Continue tracking and sending updates while a difficult complaint remains open.
7. Preserve evidence of what was decided, approved, sent and changed.
8. Deliver a reproducible, tested, deployed application with documented limitations.

## 4. Technical foundation

| Area | Baseline |
|---|---|
| Language | Python |
| Framework | Flask |
| Development database | SQLite |
| Integration and deployment database | PostgreSQL |
| Containerisation | Docker and Docker Compose |
| Version control | Git |
| Interface | Server-rendered pages; no separate frontend application |

Selected supporting components for the minimum release: Jinja templates,
Flask-SQLAlchemy, Alembic migrations, Flask-Login, Flask-WTF, pytest with a small
browser-test suite, Gunicorn. Justification belongs in the write-up.

Use a Flask application factory with separate modules for complaints, deadlines,
approvals, correspondence, audit and scheduling. Business rules must be testable
without rendering a page.

Schema migrations run from the first commit. The deployed application uses
PostgreSQL from the first deployment; SQLite is a local convenience only.

Scheduled work runs through a documented Flask CLI command invoked by an external
scheduler. Hosting provider, scheduler, CSS approach and email provider remain open
decisions.

## 5. Regulatory requirements register

Before implementing deadline rules, record for each row the exact official source,
the interpretation adopted, the expected test examples and the verification status.

| Rule area | Intended behaviour | Verification requirement |
|---|---|---|
| Receipt | Capture actual receipt date and channel separately from record creation | Confirm receipt conventions and treatment of non-working-day receipt |
| Acknowledgement | Track the five-working-day acknowledgement point | Confirm counting convention and exceptions |
| Progress updates | Track updates at intervals no greater than 20 working days | Confirm provision and timing anchor |
| Unresolved complaint | Track the 40-working-day point and required notification content | Confirm trigger, content and referral-rights wording |
| Final response | Track notification within five working days of investigation completion | Confirm the provision and what constitutes completion |
| Referral rights | Ensure unresolved and final-response templates state the complainant's right to refer the complaint onward | Confirm the required wording and authority |
| Early resolution | Apply the same log and record keeping when a complaint is resolved quickly | Confirm the shortened-procedure exception |
| Working day | Exclude days according to the applicable legal definition | Confirm the statutory term, holiday calendar and counting rule |
| Retention | Apply a defined record-retention policy | Confirm requirements before setting a period |

The 40-working-day point is a resolution target and communication point, not an
automatic closure deadline. A complaint can remain open afterwards.

Independent approval of every final outcome is a chosen internal control. It must not
be described as an express statutory requirement without supporting text.

Do not invent a late-Friday cut-off or treat an office closure as a statutory
non-working day. Do not substitute calendar days for working days.

Where the source uses a different term from "working day", adopt the source's term in
code, tests and user-facing text.

The newsletter cited in Section 21 is regulatory guidance, not a statutory instrument.
Contributions from guidance, statute and internal control must be distinguishable in
the write-up.

## 6. Roles, access and permissions

The minimum release has two roles: handler and compliance. Users hold exactly one
role.

### Permission matrix

| Action | Handler | Compliance reviewer | Record scope |
|---|---|---|---|
| Create complaint | Yes | Yes | Handler records themselves as handler; a reviewer must select a handler |
| Read complaint | Yes | Yes | Handler: assigned cases only. Reviewer: all cases |
| Edit investigation | Yes | No | Assigned cases |
| Prepare and confirm non-final correspondence | Yes | No | Assigned cases |
| Submit outcome for approval | Yes | No | Assigned cases |
| Approve or return | No | Yes | Any case the reviewer did not handle |
| Invalidate approval and reopen investigation | Yes | Yes | Own cases (handler); any case (reviewer) |
| Close complaint | Yes | Yes | Assigned cases (handler); any case (reviewer) |
| Provision users | No | No | Requires hosting or repository access outside the app |

### Enforced constraints

- `Complaint.handler_id` is required and must reference a user whose role is handler.
- `Approval.reviewer_id` is null until a decision is recorded, and when set must
  reference a user whose role is compliance.
- `Approval.reviewer_id` must differ from the handler of that complaint.
- Permissions are checked on every route, service call and data query, not only in
  templates. Direct requests receive the same checks.
- Approval validity is rechecked inside the closing transaction.
- Unauthorised access attempts are audited.
- Database row-level security is optional defence in depth, not a substitute for
  application authorisation.

Terminology: a handler **confirms** non-final messages; a compliance reviewer
**approves** a final-response package. "Authorise" is not used as a synonym for
either.

## 7. Receipt capture

Required intake information:

- Complainant name and controlled contact address.
- Actual received date; time where the verified rule requires it.
- Channel: phone, email, letter, in person or other.
- Receipt evidence or reference note, without attachments.
- Product, complaint category and description.
- Assigned handler.
- System-generated reference and creation timestamp.

The actual receipt date drives deadlines and must never default silently to the entry
date. Reject future receipt dates. Validate required fields and contact details
server-side.

After creation the receipt date is read-only. No correction route exists in the
minimum release; an audited correction workflow is listed as optional in Section 3.

## 8. Case lifecycle

### States

Logged → Investigating → Pending Approval → Approved → Closed.

A reviewer may return a proposal to Investigating with a mandatory comment. The
returned decision remains in the history and a resubmission creates a new Approval
record at a new investigation revision.

Acknowledgement and progress updates are correspondence milestones, not states.
Deadline status is tracked independently of case state.

### Post-approval changes

Approved content is never edited. Any change after approval requires the case to be
returned to Investigating first, which invalidates the current approval and is
audited with the actor, time and reason.

There is no category of edit that leaves an approval valid. The handler or a reviewer
may perform the reopening; only a fresh approval permits release.

Closed case content is read-only. Reopening after closure is out of scope.

### Closure gates

A case may close only when every gate is satisfied. This list is the single definition.

1. Findings, root-cause category, outcome, outcome rationale and redress amount are
   recorded for the current investigation revision.
2. A reviewer other than the handler has approved the current investigation revision
   and the exact final-response content now held, and that approval is not invalidated.
3. That approved final response has reached provider-accepted status.
4. Either the complaint was approved and its final response sent before the
   40-working-day point, or an unresolved-at-40-days notification has reached
   provider-accepted status before closure.
5. Closure is recorded as an audited transition by a user permitted by Section 6.

Gate 4 requires a notification only where approval and final-response sending did not
both occur before the 40-working-day point. Where they did, gate 4 is satisfied
without a notification.

Gate 4 does not excuse late notification. A notification sent after day 40 satisfies
the gate while leaving the overdue milestone and its escalation visible.

The minimum release models no discretionary closure exception. An exception field
would permit closure without evidence of a required notification and could not be
validated against a verified rule. If a verified rule later permits an alternative, it
must be added here and to Section 16.1 criterion 5 together.

Consequently a case requiring an alternative handling path cannot be closed in the
minimum release. This is a disclosed prototype limitation, not a gap to be worked
around with free text.

A failed final-response send leaves the case Approved and awaiting sending. Provider
acceptance is evidence of submission to the email service, not proof of delivery.

## 9. Deadline engine and milestones

### Milestone records

Each obligation is a stored milestone: complaint, type, sequence, due date, whether
it is open or completed, the completing correspondence and the completion timestamp.
Milestones are never overwritten, so the history of due dates survives repeated
updates. Current deadlines are derived from open milestones; the complaint record
holds no duplicate due-date columns.

Milestone types: acknowledgement, progress update, unresolved notification, final
response.

### Calculation

Use verified rules with explicit date conventions and the applicable holiday
calendar. Store timestamps consistently and display them in Europe/Dublin local time.
A rolling 24-hour approximation is not acceptable.

### Display

Every countdown shows the milestone label, exact due date, working days remaining or
overdue, completion status and the next permitted action.

- "Acknowledgement due in 2 working days — 14 November 2026".
- "Progress update due today".
- "Acknowledgement overdue by 1 working day".
- "40-working-day point passed — unresolved notification required".
- "Acknowledged 12 November 2026 — within deadline".

Completed milestones retain their due date and completion timestamp. Multiple clocks
display simultaneously when obligations overlap. Text or icons accompany colour.
Countdown accuracy must not depend on the scheduler having run.

### Continued updates

The unresolved-at-40-days notification neither closes the case nor ends update
obligations.

Acknowledgement → progress updates → unresolved notification → further progress
updates → approved final response → closure.

There is no maximum number of updates. Each is its own logged message and its own
milestone. Sending any message leaves the receipt date, the 40-working-day target and
the final-response deadline unchanged. Where a verified combined message satisfies two
obligations, both milestones are completed by that message and the combination is
recorded.

## 10. Correspondence

### Message types

1. Acknowledgement.
2. Progress update — repeatable before and after the 40-working-day point.
3. Unresolved-at-40-days notification.
4. Final response.

Any substantive outgoing message to the complainant is sent as one of these four
types, so no outgoing case communication escapes the log. A request for further
information from the complainant is sent as a progress update. Inbound telephone or
email contacts are recorded in the investigation record; no separate case-note type
exists in the minimum release.

### Templates

Templates are fixed and version-controlled. Each message carries its template version
so later changes cannot rewrite what was sent. Unresolved and final-response templates
must state the complainant's referral rights; the exact wording is a verification task
in Section 5 and an acceptance criterion in Section 16.1.

Staff-facing digests contain references and links, not narratives. Complainant
messages necessarily contain substantive detail, which is minimised.

### Flow

Prepare → preview → confirm or approve → persist → attempt send → record result.

The outbox record is written before the provider is called. Stored content includes
the recipient, subject and body as released, template version, the confirming or
approving user, the approval reference where applicable, timestamps, status, provider
reference and any error summary.

### Editability

A correspondence row is editable only while its status is draft and no live approval
refers to it. Editing after a return is an in-place edit of that draft, because a
returned approval is no longer live and the reviewed content is preserved in the
approval snapshot.

Authorisation freezes content. A frozen message may be retried with unchanged content
but never edited. Changing it means withdrawing approval and resubmitting a new final
response.

### Statuses

draft, sending, provider_accepted, failed, acceptance_unknown.

`acceptance_unknown` means the provider's acceptance of the message is unknown. It is
never used to describe delivery, and provider acceptance is never described as
delivery or reading.

### Failure and uncertainty

Failed and uncertain messages remain visible in the case and in the operational queue,
and never complete a milestone.

Definite failures may be retried with unchanged content, reusing the same authorised
record and recorded as a new attempt.

An uncertain outcome requires a recorded resolution by a compliance reviewer: either
confirm acceptance with supporting evidence, or authorise a replacement send. Both are
audited. The scheduled check flags any message still in sending beyond a configured
age as acceptance_unknown; it never resends automatically.

### Controlled live sending

Only allowlisted recipients receive real mail, enforced in the send service rather
than the interface. Addresses are checked after final resolution. Unrestricted CC and
BCC are not supported. Content is synthetic with a demonstration notice. Credentials
stay outside Git and AI tools. Automated tests use a fake transport; a separate
controlled test demonstrates real delivery to a test address.

## 11. Investigation, outcome and approval

Investigation records: findings, root-cause category, outcome, outcome rationale,
redress amount and completion timestamp. No guided root-cause framework is required.

Root-cause category, product and complaint category are closed enumerations defined in
version-controlled configuration, not free text. The initial lists will be recorded in
the source register appendix of the write-up; adding a value is a code change.

Outcomes: Upheld, Partially upheld, Not upheld. Redress is recorded, including zero,
and is not paid by the application.

`Investigation.completed_at` is set when the handler submits the package for approval.
A return clears it, so the final-response clock stops until resubmission, which sets a
new value and recalculates the deadline. Whether a return should restart the
statutory clock is an interpretation question recorded in Section 5, not an
assumption.

On submission the system stores an immutable snapshot of the reviewed package — the
investigation fields for that revision plus the exact final-response subject, body and
recipient — on the Approval record. Reviewers decide against the snapshot, and the
snapshot is evidence after later edits.

Approval and return require a comment. Approval validity is checked when the decision
is made and again inside the send and close transactions. A revision check rejects a
stale submission rather than overwriting a newer decision.

## 12. Logical data model

| Entity | Purpose |
|---|---|
| User | Identity, single role, activation |
| Complainant | Contact details, held separately from case narrative |
| Complaint | Receipt details, handler, classification, lifecycle |
| Investigation | Findings, root cause, outcome, redress, revision, completion |
| Approval | Submission snapshot, revision reference, decision, invalidation |
| Correspondence | Outbound message content, type, milestone link, status |
| SendAttempt | Attempt result, provider reference, error, uncertainty resolution |
| Milestone | Obligation type, sequence, due date, completing message, completion |
| ScheduledRun | Job name, period key, status, timestamps, error |
| AuditEvent | Actor, time, action, change details |
| PublicHoliday | Date, name, calendar |

This is a logical model, not a table-count target. Separating complainant details
supports permission design but is not anonymisation; message bodies and findings may
also contain personal data.

A separate case-note entity and any investigation-revision table are deferred; the
approval snapshot provides the evidence the revision table would otherwise hold.

## 13. Logical screens

Dashboard: open cases, acknowledgements due, updates due, day-40 cases, responses due,
pending approvals, failed and uncertain sends. Urgent actions precede any totals.

Complaint list: reference, state, handler, received date, next milestone and next
action. Filters for state, handler, date range, category and overdue status. Only
authorised records affect results and counts.

Intake: required fields, explicit receipt date, contact validation, handler selection,
confirmation of calculated milestones.

Complaint detail: header with reference, state, handler and milestone panel; sections
for summary, investigation, outcome and approval, correspondence, audit history.
Role-appropriate actions are shown and independently enforced.

Correspondence composer: type, template, required fields, preview, allowlisted
recipient, approval status, confirmation, and clear send outcome.

Approval queue: pending packages, read-only snapshot, approve or return, mandatory
comment, self-approval prevention.

No configuration screens exist in the minimum release.

Detailed visual design is left to the UI specification.

### Responsive and mobile behaviour

One responsive website, not a separate mobile application. The following rows are
committed for the minimum-release screens listed above.

| Area | Mobile behaviour |
|---|---|
| Navigation | Collapsible, keyboard-accessible menu with a labelled control |
| Dashboard | Stacked cards and milestone panels, urgent items first |
| Complaint list | Compact rows with reference, state, next milestone and action |
| Complaint detail | Stacked sections, reference and next milestone near the top |
| Forms | Single column, adjacent validation messages, entered values preserved |
| Correspondence | Prepare, preview and send without page-level horizontal scrolling |
| Approval | Snapshot, outcome, redress and response preview visible before deciding |
| Action controls | Comfortable touch spacing; sticky controls must not obscure content or focus |
| Countdowns | Milestone label, exact date and text urgency, never colour alone |

Native applications, offline operation and push notifications are out of scope.

## 14. Automations

| Type | Behaviour |
|---|---|
| Scheduled | Daily deadline and stuck-send check, plus staff digest |
| Event-triggered | Intake creates milestones and an acknowledgement draft; a completed message completes its milestone; submission opens an approval |
| Human | Approval blocks release until decided; uncertain sends require recorded resolution |

Nothing substantive to a complainant is sent because a timer fired. Monitoring prompts
a human to act.

Each scheduled run records its job name and period key, so a rerun cannot duplicate a
digest for the same period. Failures and the last successful run are recorded. Digest
recipients are allowlisted like any other recipient.

## 15. Security, privacy and operations

- Authentication, password hashing, CSRF protection, secure session configuration and
  server-side validation.
- Authorisation on every protected request and record access.
- Audit of approvals, returns, approvals invalidated, denials, correspondence
  attempts, uncertainty resolutions, account provisioning through the CLI and
  relevant configuration changes.
- Operational logs kept separate from business audit evidence, without secrets or
  unnecessary narrative.
- Append-only audit behaviour through the application, with the limitation of
  database-owner access documented.
- Synthetic data only; production legal basis and retention described separately.
- Retention: a documented policy is delivered. No deletion feature is implemented and
  that is stated as a limitation.
- Backup and restore, access review, incident response, change control and ownership
  documented in the governance policy.
- Monitoring of health, errors, scheduled-run failures and send failures.
- Accessible labels, keyboard navigation, visible focus, contrast, clear errors and
  non-colour status indicators, with real failures reported honestly.
- Persistent database storage and a documented recovery route.

## 16. Success criteria and release priorities

### 16.1 Minimum release — committed scope

These are established before implementation and must be evidenced by tests,
demonstration or documented procedure.

**Complete journey**

1. Using separate handler and compliance accounts, complete intake → investigation →
   submission → independent approval → final-response sending → closure.
2. Record the actual receipt date and channel separately from the creation timestamp,
   reject future dates, and keep the receipt date read-only after creation.
3. Record findings, root-cause category, outcome, outcome rationale and redress, with
   closed enumerations, and reject submission while any is missing.
4. Allow a reviewer to approve or return with a mandatory comment; a return makes the
   package editable again and remains in history.
5. Refuse closure unless every gate in Section 8 is satisfied, returning a specific
   reason for each unmet gate.

**Identity, permissions, integrity**

6. Provide working authentication and server-side permissions. One handler must not
   read or modify another's complaint through any route.
7. Prevent self-approval, prevent any user changing their own role, and enforce the
   handler and reviewer constraints in Section 6 at the data layer.
8. Keep correspondence editable only in draft with no live approval, freeze content on
   authorisation, and require invalidation of approval before any approved content
   changes.
9. Audit approvals, returns, invalidations, denials, sends, uncertainty resolutions and
   CLI provisioning, with entries not editable through the application.

**Deadlines**

10. Calculate every milestone from verified rules and pass independently checked
    examples covering ordinary dates, weekends, applicable holidays and a year
    boundary.
11. Display each milestone with exact due date and text status, and retain the due date
    and completion timestamp of completed milestones after later updates.
12. Support repeated progress updates before and after the 40-working-day notification
    without changing the receipt date or resolution target, demonstrated on a synthetic
    case with at least two post-notification updates.

**Correspondence**

13. Send all four message types through the app using version-controlled templates,
    and confirm that unresolved and final-response templates state referral rights.
14. Restrict real sends to server-side allowlisted addresses, persist content before
    sending, and log recipient, content, actor, timestamps and result.
15. Distinguish provider acceptance, definite failure and unknown acceptance; never
    describe acceptance as delivery, and keep unresolved messages visible without
    completing milestones.
16. Permit retry of definite failures with unchanged content and require a recorded,
    audited resolution of uncertain outcomes before any replacement send.

**Interface and automation**

17. Provide dashboard, complaint list, intake, complaint detail and approval queue with
    basic counts rather than advanced reporting.
18. Support keyboard operation and a 375 CSS pixel viewport for the committed journey
    without horizontal scrolling or hidden essential controls, with identical
    permissions and approval rules across sizes.
19. Produce an idempotent staff digest from the scheduled check, recording each run and
    its failures.

**Delivery and evidence**

20. Preserve data across restarts, run the deployed application on PostgreSQL, and
    rebuild it from a clean checkout using the documented Docker procedure.
21. Pass the test suite in Section 17, including stale-revision rejection and digest
    idempotency, against PostgreSQL.
22. Retain security-scan results and the recorded response to each finding, with no
    secrets in the repository or AI tools.
23. Provide the repository, deployment instructions, governance policy, monitoring
    evidence, privacy and accessibility review, AI-use log and declaration, technical
    write-up and live demonstration.

### 16.2 Optional enhancements

Only after Section 16.1 is evidenced and remaining assessment work is reserved:
receipt correction with authorisation and recalculation, handler reassignment,
browser-based user and holiday administration with an administrator role, case notes,
delivery webhooks and reconciliation, background queue, advanced reporting, editable
templates, extended device coverage, and an expedited early-resolution path.

Optional status removes no security requirement. Anything implemented must carry its
permissions, validation, audit and tests.

### 16.3 Implementation choices for the minimum release

- Users are created by a documented CLI command.
- The holiday calendar is loaded from a verified dataset covering the test period and
  the following year.
- Templates are files in version control.
- One email provider is called inline; there is no queue or worker.
- Early-resolved complaints follow the normal journey.
- No receipt-correction, reassignment or administrative routes exist.
- Erroneous synthetic cases are corrected by creating a new case, not by rewriting
  history.

### 16.4 Baseline and change control

Commit this baseline before implementation and retain earlier versions in Git. Record
each later change with its reason and impact. Do not redefine success to match
whatever was built.

## 17. Test strategy

- Unit: working-day arithmetic, milestone generation and re-generation, state
  transitions, approval invalidation, stale-revision rejection.
- Integration: persistence, permissions, transactional approve and close, correspondence
  logging, approval snapshot retention.
- Closure gates: one negative test per unmet gate in Section 8, including missing
  findings, missing or invalidated approval, missing final-response send, unauthorised
  closure, and a missing-notification case where approval and sending did not both
  occur before the 40-working-day point.
- Closure success: one closure after all gates pass, and one case approved and closed
  before the 40-working-day point with no notification sent.
- Negative: self-approval, cross-handler access, role self-change, non-allowlisted
  recipient, editing a frozen message, closing with an invalidated approval.
- Correspondence: success, definite failure, unknown acceptance and its resolution,
  retry without duplication, stale sending flagged by the scheduled check.
- Scheduling: idempotent digest for a repeated period key, recorded failure.
- Browser: one main end-to-end journey and key blocked actions.
- PostgreSQL: run the full suite against the deployment database before submission.
- Security: appropriate scanners for source, dependencies, container and deployed
  application, with triage and remediation or acceptance recorded.
- Accessibility: automated checks plus manual keyboard review.

Prioritise control tests over coverage percentages.

## 18. Repository and assessment deliverables

- Source with meaningful incremental history.
- Migrations and synthetic seed data.
- Working Dockerfile and deployment documentation.
- Example environment file with placeholders only.
- Automated tests and documented commands.
- Security-scan output and remediation evidence.
- Deployed application with role-specific accounts supplied securely.
- Governance policy and operational runbook.
- Architecture, data model and DFD/STRIDE evidence.
- Approximately 2,500-word technical write-up with Harvard references and cover page.
- AI-usage log and AI Fluency declaration appendix.
- Live demonstration in Week 12 with a recommendation supported by observed results.

The assessment prohibits AI authorship of the design-decision analysis, security
findings discussion, accessibility review and limitations section. Those remain the
student's own work.

## 19. Delivery approach

1. Commit scope, rule register and success criteria.
2. Establish repository, Flask skeleton, authentication, Docker and PostgreSQL.
3. Implement and test receipt and deadline logic.
4. Deliver one persistent case journey with approval, audit and closure gates.
5. Add correspondence, fake transport and milestone handling.
6. Integrate allowlisted real sending and test failure and uncertainty.
7. Complete tests, scans, accessibility and monitoring.
8. Complete governance evidence and the deployed demonstration.
9. Write the technical report and reserve contingency.

Submission is at the end of Week 11 with the demonstration in Week 12. Confirm actual
dates against the timetable.

Available hours remain unconfirmed; plan conservatively around work and family
commitments. Re-estimate after the first working slice.

## 20. Open decisions

- Verified provisions, counting conventions and referral wording.
- Hosting provider and persistent PostgreSQL service.
- Email provider, test recipients and uncertainty handling thresholds.
- CSS approach and visual design.
- Account recovery and optional MFA.
- Holiday calendar source and update procedure.
- Interpretation of the final-response clock after a return.
- Confirmed timetable and sustainable weekly effort.

## 21. Reference and evidence register

Primary coursework source: MCLCD_Oct26_CA2_LowCodeNoCodeAIDev.docx, read 9 November
2026. It specifies repository, testing, Docker, deployment, governance, accessibility,
AI declaration and demonstration requirements.

Additional supplied source: Low-Code-No-Code-Project-Brief.pdf. Its status alongside
CA2 must be confirmed; earlier ERD, automation, access-control, DFD, STRIDE and data
protection planning should be preserved where applicable.

Sources to verify and cite by provision:

- Central Bank of Ireland, Consumer Protection Code 2025 (statutory instrument or
  code — status to be confirmed).
- Central Bank of Ireland, General Consumer Protection Requirements (confirm whether
  this is a separate instrument from the Code).
- Central Bank of Ireland, Investment Firm and Intermediary Newsletter, June 2026
  (guidance, not law).

## 22. Revision history

| Version | Change |
|---|---|
| 0.2 | Initial product definition and specification. |
| 0.3 | Minimum release introduced; committed and optional scope separated; closure gates consolidated. |
| 0.4 | Contradictions resolved: no post-approval editing, approval snapshots, milestone records, acceptance uncertainty, permission matrix, scheduled-run records, single scope table, single test list, consolidated terminology. |

Superseded statements, retained only as record:

- An earlier draft implied a late-Friday cut-off; no such rule is modelled.
- An earlier draft treated 8 January as a submission date; the timetable governs.
- An earlier draft described features as belonging to "the original concept"; scope
  status in Section 3 governs.
- An earlier draft used a precedence rule that Section 16 overrides other sections;
  v0.4 resolves the contradictions instead.
- Earlier drafts used "MVP", "minimum assessed release" and "minimum implementation";
  v0.4 uses "minimum release".

---

# Appendix A — Specification

## Purpose

An internal complaints-management application for handlers and compliance reviewers
in a small Irish insurance intermediary. It replaces spreadsheets and disconnected
email with deadline tracking, independent approval, logged correspondence and an
auditable history.

## Entities

### User
- id (integer, primary key)
- name (text, required)
- email (text, required, unique)
- password_hash (text, required)
- role (one of: handler, compliance)
- active (boolean, default true)
- created_at (timestamp)

An administrator role is deferred to Section 16.2 and is not part of this release.

### Complainant
- id (integer, primary key)
- name (text, required)
- email (text, required; controlled test address)
- phone (text, optional)
- created_at (timestamp)

### Complaint
- id (integer, primary key)
- reference (text, required, unique, system-generated)
- complainant_id (foreign key to Complainant, required)
- handler_id (foreign key to User, required; the user must hold the handler role)
- received_date (date, required; read-only after creation)
- received_time (time, optional)
- received_channel (one of: email, phone, letter, in_person, other)
- receipt_note (text, required)
- product (enum, required)
- category (enum, required)
- description (text, required)
- status (one of: logged, investigating, pending_approval, approved, closed;
  default logged)
- closed_at (timestamp, optional)
- created_at (timestamp)
- updated_at (timestamp)

Due dates are not stored here; they are derived from Milestone records.

### Investigation
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required, unique)
- findings (text, optional while drafting)
- root_cause_category (enum, optional while drafting)
- outcome (one of: upheld, partially_upheld, not_upheld; optional while drafting)
- outcome_rationale (text, optional while drafting)
- redress_amount (decimal, non-negative, default 0)
- revision (integer, default 1; incremented on each submission)
- completed_at (timestamp, optional; set on submission, cleared on return)
- updated_at (timestamp)

### Approval
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- investigation_revision (integer, required)
- final_response_id (foreign key to Correspondence, required)
- reviewer_id (foreign key to User, nullable until a decision; must hold the
  compliance role and differ from the handler)
- decision (one of: pending, approved, returned; default pending)
- comment (text, required when a decision is recorded)
- package_snapshot (structured data, required; immutable copy of the reviewed
  investigation fields and final-response recipient, subject and body)
- content_hash (text, required; hash of the snapshot)
- submitted_at (timestamp, required)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)

### Correspondence
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- milestone_id (foreign key to Milestone, optional)
- message_type (one of: acknowledgement, progress_update,
  unresolved_notification, final_response)
- recipient_email (text, required before sending)
- subject (text, required before sending)
- body (text, required before sending)
- template_version (text, required)
- status (one of: draft, sending, provider_accepted, failed, acceptance_unknown;
  default draft)
- authorised_by_id (foreign key to User, optional until confirmed or approved)
- authorised_at (timestamp, optional)
- provider_accepted_at (timestamp, optional)
- created_at (timestamp)
- Editable only while draft and not referenced by a pending or approved,
  non-invalidated Approval. Content is immutable once authorised.

### SendAttempt
- id (integer, primary key)
- correspondence_id (foreign key to Correspondence, required)
- attempted_at (timestamp, required)
- result (one of: provider_accepted, failed, acceptance_unknown)
- provider_reference (text, optional)
- error_code (text, optional)
- error_summary (text, optional; excludes secrets)
- resolved_by_id (foreign key to User, optional)
- resolved_at (timestamp, optional)
- resolution (one of: confirmed_accepted, resend_authorised, optional)
- resolution_note (text, optional)

### Milestone
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- type (one of: acknowledgement, progress_update, unresolved_notification,
  final_response)
- sequence (integer, required; orders repeated updates)
- due_date (date, required)
- completed_correspondence_id (foreign key to Correspondence, optional)
- completed_at (timestamp, optional)
- created_at (timestamp)
- Unique on (complaint_id, type, sequence).

### ScheduledRun
- id (integer, primary key)
- job_name (text, required)
- period_key (text, required)
- status (one of: started, succeeded, failed)
- started_at (timestamp, required)
- finished_at (timestamp, optional)
- item_count (integer, optional)
- recipient (text, optional; allowlisted)
- error_summary (text, optional)
- Unique on (job_name, period_key).

### AuditEvent
- id (integer, primary key)
- complaint_id (foreign key to Complaint, optional)
- actor_id (foreign key to User, optional for system and CLI actions)
- action (text, required)
- change_details (structured data, optional; minimises personal data)
- created_at (timestamp)
- Append-only through the application.

### PublicHoliday
- id (integer, primary key)
- date (date, required)
- name (text, required)
- calendar (text, required)
- Unique on (date, calendar).

A case-note entity is deferred to Section 16.2.

## Routes

| Method | Path | Does |
|---|---|---|
| GET | /login | Show login form |
| POST | /login | Authenticate and start session |
| POST | /logout | End session |
| GET | / | Role-appropriate dashboard with milestones and urgent actions |
| GET | /complaints | List and filter authorised complaints |
| GET | /complaints/new | Show intake form |
| POST | /complaints | Create complaint and generate milestones |
| GET | /complaints/<id> | Show authorised case, milestones, correspondence and audit |
| POST | /complaints/<id>/investigation | Save investigation draft |
| POST | /complaints/<id>/correspondence | Create a controlled draft |
| POST | /correspondence/<id>/edit | Edit a draft that is not under live approval |
| GET | /correspondence/<id>/preview | Preview recipient, subject, body and approval status |
| POST | /complaints/<id>/submit-outcome | Snapshot the package and open approval |
| GET | /approvals | Show compliance review queue |
| POST | /approvals/<id>/decision | Approve or return the snapshotted package |
| POST | /complaints/<id>/return-to-investigation | Invalidate approval and reopen investigation |
| POST | /correspondence/<id>/send | Confirm or approve, persist, then attempt send |
| POST | /correspondence/<id>/retry | Retry a definite failure with unchanged content |
| POST | /correspondence/<id>/resolve-uncertainty | Record acceptance evidence or authorise a resend |
| POST | /complaints/<id>/close | Enforce every closure gate in Section 8, then close and audit |
| GET | /health | Minimal health status without sensitive information |

### Optional routes

Deferred to Section 16.2; not part of this release.

| Method | Path | Does |
|---|---|---|
| POST | /complaints/<id>/receipt-correction | Compliance-authorised correction with reason and recalculation |
| POST | /complaints/<id>/assign | Reassign the handler with audit |
| POST | /complaints/<id>/notes | Add a case note |
| GET | /admin/users | Account-management screen |
| POST | /admin/users/<id>/update | Change role or activation with audit |
| GET | /admin/holidays | Holiday configuration |
| POST | /admin/holidays | Add a verified holiday entry with audit |

## Technical constraints

- Python and Flask with versions pinned in the repository.
- SQLite locally; PostgreSQL for integration testing and deployment.
- Flask-SQLAlchemy for persistence and Alembic for migrations.
- Application factory with business rules in separate modules.
- Jinja templates; no separate JavaScript frontend framework.
- Responsive interface supporting the committed journey at 375 CSS pixels.
- Authentication, password hashing, CSRF protection and server-side validation.
- Reject future receipt dates and validate required intake fields server-side.
- Permissions enforced on every request, service call and query, including direct
  requests that bypass the interface.
- Handlers reach assigned cases only; reviewers reach all cases but never decide a
  case they handled.
- Handler, reviewer and single-role constraints enforced in the data layer.
- Correspondence editable only in draft and only outside a live approval; frozen on
  authorisation.
- Approved content never edited; change requires invalidation and resubmission.
- Closure requires every gate in Section 8, including recorded findings and, where the
  complaint remained unresolved at the 40-working-day point, an unresolved notification
  with provider-accepted status.
- Provider acceptance is never described as delivery.
- All four message types are sent through the app and logged automatically.
- Progress updates are repeatable before and after the 40-working-day point and never
  reset the receipt date or resolution target.
- Milestones are stored per obligation; current deadlines derive from open milestones.
- Deadline calculation uses verified rules and the applicable working-day calendar.
- Countdowns show label, exact date and text urgency.
- Outbound content is persisted before any send attempt.
- Real sending is restricted server-side to allowlisted addresses; no unrestricted
  CC or BCC.
- Failed and uncertain sends remain visible and never complete milestones.
- Unknown acceptance requires a recorded, audited resolution before any replacement
  send; the scheduled check flags stale sending records.
- Scheduled runs are idempotent per job and period and record failures.
- Synthetic data only; credentials from environment configuration, never in Git or AI
  tools.
- Scheduled work runs through a documented CLI command, not a web route.
- Users are provisioned by CLI; holidays are loaded from a verified dataset; templates
  are version-controlled.
- Retention is a documented policy only; no deletion feature is implemented.
- Dockerfile, deployment documentation, persistent database, automated tests, scan
  evidence and meaningful Git history are required.
- Exact regulatory interpretations, hosting provider and email provider must be
  verified or selected before implementation.

## Out of scope

Excluded capabilities are listed in the single scope table in Section 3. Items marked
Optional there are deferred, not excluded; items marked Out of scope are not delivered
in this release.