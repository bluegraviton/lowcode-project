# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.5 — 9 November 2026
Status: Minimum release defined, with architecture, approval and security decisions
settled. Regulatory rules remain unverified pending the Section 5 register.

## 1. Purpose

An internal web application for a small Irish regulated insurance intermediary. It
manages complaints from receipt through investigation, independent approval,
correspondence and closure, replacing a spreadsheet and disconnected email process
with a controlled case record, visible deadlines and an auditable history.

The application supports complaint handling under the Central Bank of Ireland
complaints-handling requirements. It is a coursework prototype, not a certified
compliance product. Statutory obligations, chosen internal controls and prototype
limitations are distinguished throughout.

The essential product is accurate deadline tracking, independent approval of
outcomes, correspondence sent through the application, and an audit trail.

## 2. Intended users and operating context

- One small Irish insurance intermediary.
- Single organisation; no multi-tenancy.
- Handlers investigate their assigned cases.
- Compliance reviewers decide outcomes and final responses independently.
- Accounts are provisioned by a documented command-line procedure, performed by an
  operator holding repository and hosting access. That privilege sits outside the
  application's permission model.
- Complainants have no account and no public portal. Some correspondence is addressed
  to the product provider or insurer rather than the complainant.
- All records are synthetic. Real email reaches only controlled test addresses.
- Desktop-first, responsive on smaller screens.

The application cannot prevent a person holding database or hosting credentials from
reading complaint data outside the application. No role description claims otherwise.

## 3. Scope boundary

One table defines what is committed, deferred and excluded. Other sections refer to it.

| Capability | Status |
|---|---|
| Intake with actual receipt date and channel | Committed |
| Authorised receipt correction with recalculation | Committed |
| Verified working-day deadline calculation | Committed |
| Milestone records preserving due and completion dates | Committed |
| Countdown display with exact dates and text urgency | Committed |
| Investigation, outcome and redress recording with fixed categories | Committed |
| Independent approval of the final response only | Committed |
| Approve, return with reasons, resubmit with notes | Committed |
| Approval invalidation before any post-approval change | Committed |
| Four correspondence types, complainant, provider or internal recipient | Committed |
| Outbox record, allowlist, failure and uncertainty handling | Committed |
| Repeated progress updates before and after the 40-working-day point | Committed |
| Scheduled deadline check with idempotent staff digest | Committed |
| CSV export of the authorised register | Committed |
| Audit trail covering decisions, denials, corrections and sends | Committed |
| Baseline authentication hardening | Committed |
| Responsive main journey at 375 CSS pixels | Committed |
| Docker deployment on PostgreSQL | Committed |
| Itemised change requests with per-item handler responses | Optional |
| Handler reassignment | Optional |
| Browser-based user, role and holiday administration | Optional |
| Case notes as a separate record type | Optional |
| Attachments and document uploads | Optional |
| Delivery and bounce webhooks, provider reconciliation | Optional |
| Background queue and automated retry scheduling | Optional |
| Advanced reporting, charts and further exports | Optional |
| Editable correspondence templates | Optional |
| Extended browser and device test coverage | Optional |
| Expedited early-resolution workflow | Optional |
| Password reset by email and multi-factor authentication | Optional |
| Public intake, complainant accounts, self-service portal | Out of scope |
| Inbound email ingestion and mailbox integration | Out of scope |
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
| Database | PostgreSQL for development, integration testing and deployment |
| Containerisation | Docker and Docker Compose |
| Version control | Git |
| Interface | Server-rendered pages; no separate frontend application |

Selected supporting components: Jinja templates, Flask-SQLAlchemy, Alembic migrations,
Flask-Login, Flask-WTF, pytest with a small browser-test suite, Gunicorn. Justification
belongs in the write-up.

PostgreSQL runs in Docker Compose from the first commit, so local work and deployment
share one database engine. There is no second database target. If the brief mandates a
different development database, it becomes a local convenience only and the deployed
system remains PostgreSQL.

### Architecture and modularity

The application must remain straightforward to extend, modify or reduce. This is a
requirement, not a preference.

- Layer routes, services and models. Routes validate input and delegate; services hold
  business rules and transactions; models hold persistence. No rule logic in routes or
  templates.
- Feature packages as Flask blueprints: complaints, investigation, approvals,
  correspondence, deadlines, audit, scheduling. Removing a feature means deleting its
  package and one registration line.
- Deadline rules as pure functions in one module, taking dates and returning dates,
  with no database access. A verified interpretation change then touches one file and
  its tests.
- All enumerations, status values, template names and tunable values live in one
  configuration module. No string literals in logic.
- Templates grouped by feature with one base layout and one shared macros file.
- Migrations for every schema change, additive and nullable-first, with a documented
  step required before any destructive change.
- No stored column duplicates derived data; current deadlines come from milestones.
- Tests mirror the package structure, so a rule change identifies the tests to run.
- A one-page architecture note in the repository states where each kind of change
  belongs. It also serves as write-up evidence.

The intended test of the design is concrete: adding a root-cause category, changing the
acknowledgement interval, or removing CSV export should each touch one or two files and
nothing else.

### Over-engineering guardrail

- No abstraction before two call sites, and no mechanism that exists only for future
  flexibility.
- The seams above are the permitted abstractions. Anything further requires
  justification in the write-up against the specific risk it removes.
- No plugin registry, dependency-injection container, configuration-driven workflow or
  generic event bus.
- Every dependency and helper module must remove more code than it adds, or be required
  by an assessment deliverable.
- Duplication is acceptable; premature generalisation is not.
- A feature added must map to a committed criterion. A feature removed must delete its
  route, template, tests and criterion reference together.

## 5. Regulatory requirements register

Before deadline logic is written, record for each row the exact provision, the
interpretation adopted, the expected test examples and the verification status.

This register is a gate. Deadline-engine code is not merged until each row that drives
code contains a quoted provision, a one-sentence interpretation, two worked examples with
real dates, and a statement of what would change if the interpretation is wrong. Rows
that affect only narrative, such as retention, need a citation but no test examples.

| Rule area | Intended behaviour | Verification requirement |
|---|---|---|
| Receipt | Capture actual receipt date and channel separately from record creation | Confirm receipt conventions and non-working-day receipt |
| Acknowledgement | Track the five-working-day acknowledgement point | Confirm counting convention and exceptions |
| Progress updates | Track updates at intervals no greater than 20 working days | Confirm provision and timing anchor |
| Unresolved complaint | Track the 40-working-day point and required notification content | Confirm trigger, content and referral-rights wording |
| Final response | Track notification within five working days of investigation completion | Confirm the provision and what constitutes completion |
| Referral rights | Ensure unresolved and final-response templates state the right to refer the complaint onward | Confirm required wording and authority |
| Early resolution | Apply the same log and records when a complaint is resolved quickly | Confirm the shortened-procedure exception |
| Working day | Exclude days according to the applicable legal definition | Confirm the statutory term, holiday calendar and counting rule |
| Retention | Apply a defined record-retention policy | Confirm requirements before setting a period |

The 40-working-day point is a resolution target and communication point, not an
automatic closure deadline.

Independent approval of the final response is a chosen internal control. It must not be
described as an express statutory requirement without supporting text.

Do not invent a late-Friday cut-off or treat an office closure as a statutory
non-working day. Do not substitute calendar days for working days. Where the source uses
a different term from "working day", adopt the source's term in code, tests and
user-facing text.

The newsletter cited in Section 21 is guidance, not a statutory instrument. Statute,
code, guidance and internal control must stay distinguishable in the write-up.

## 6. Roles, access and permissions

Two roles: handler and compliance. Each user holds exactly one role.

### Permission matrix

| Action | Handler | Compliance reviewer | Record scope |
|---|---|---|---|
| Create complaint | Yes | Yes | Handler records self as handler; reviewer selects a handler |
| Read complaint | Yes | Yes | Handler: assigned cases. Reviewer: all cases |
| Export register to CSV | Yes | Yes | Handler: assigned cases. Reviewer: all cases |
| Edit investigation | Yes | No | Assigned cases |
| Correct a receipt date | No | Yes | Any case, with reason and audit |
| Prepare and confirm acknowledgement, update or notification | Yes | No | Assigned cases |
| Submit final response for approval | Yes | No | Assigned cases |
| Approve or return the final response | No | Yes | Any case the reviewer did not handle |
| Invalidate approval and reopen investigation | Yes | Yes | Own cases (handler); any case (reviewer) |
| Close complaint | Yes | Yes | Assigned cases (handler); any case (reviewer) |
| Provision or deactivate users | No | No | Requires hosting or repository access |

### Enforced constraints

- `Complaint.handler_id` is required and must reference a user whose role is handler.
- `Approval.reviewer_id` is null until a decision, and when set must reference a user
  whose role is compliance and must differ from the handler.
- A user cannot change their own role or reactivate themselves.
- A user holding open complaints cannot be deactivated; the command fails with the
  blocking references listed.
- Permissions are checked on every route, service call and query, including direct
  requests.
- Approval validity is rechecked inside the sending and closing transactions.
- Denials and failed authorisation attempts are audited.

Terminology: a handler **confirms** a message; a reviewer **approves** a final response.
Approval applies to the final response only, because that is the message that carries an
outcome and a redress position.

## 7. Receipt capture and correction

Required intake information:

- Complainant name and controlled contact address.
- Actual received date; time where the verified rule requires it.
- Channel: phone, email, letter, in person or other.
- Receipt evidence or reference note, without attachments.
- Product, complaint category and description.
- Assigned handler.
- System-generated reference and creation timestamp.

The receipt date drives every deadline and must never default to the entry date. Reject
future dates. Validate required fields and contact details server-side.

The receipt date is read-only to ordinary editing. A compliance reviewer may correct it
through a dedicated action that requires a reason, records the previous and new values
with the actor and time, and recalculates milestones.

Recalculation marks the superseded milestones as superseded rather than deleting them,
and creates replacements. The earlier due dates and their completion state therefore
remain visible as evidence of what was monitored before the correction.

## 8. Case lifecycle

### States

Logged → Investigating → Pending Approval → Approved → Closed.

A return moves the case back to Investigating. The returned decision remains in the
history, and resubmission creates a new Approval row at a new investigation revision.

Acknowledgement and progress updates are correspondence milestones, not states.

### Post-approval changes

Approved content is never edited. Any change after approval requires returning the case
to Investigating, which invalidates the approval and is audited with actor, time and
reason.

There is no category of edit that leaves an approval valid. The handler or a reviewer may
perform the reopening; only a fresh approval permits release.

Closed case content is read-only. Reopening after closure is out of scope.

### Closure gates

A case may close only when every gate is satisfied. This list is the single definition.

1. Findings, root-cause category, outcome, outcome rationale and redress amount are
   recorded for the current investigation revision.
2. A reviewer other than the handler approved the current revision and the exact
   final-response content now held, and that approval is not invalidated.
3. That final response reached provider-accepted status.
4. Either the complaint was approved and its final response sent before the
   40-working-day point, or an unresolved-at-40-days notification reached
   provider-accepted status before closure.
5. Closure is recorded as an audited transition by a user permitted by Section 6.

Gate 4 requires a notification only where approval and final-response sending did not
both occur before the 40-working-day point.

Gate 4 does not excuse late notification. A notification sent after the point satisfies
the gate while leaving the overdue milestone visible.

The minimum release models no discretionary closure exception. An exception field would
permit closure without evidence of a required notification and could not be validated
against a verified rule. If a verified rule later permits an alternative, it must be
added here and to the closure-gate criterion in Section 16.1 together.

Consequently a case requiring an alternative handling path cannot be closed in this
release. This is a disclosed limitation, not a gap to be worked around with free text.

A failed final-response send leaves the case Approved and awaiting sending. Provider
acceptance is not proof of delivery.

## 9. Deadline engine and milestones

### Milestone records

Each obligation is a stored milestone: complaint, type, sequence, due date, open or
completed state, completing correspondence, completion timestamp, and a superseded flag
used only by receipt correction. Milestones are never overwritten, so the history of due
dates survives repeated updates. Current deadlines derive from open, non-superseded
milestones.

Types: acknowledgement, progress update, unresolved notification, final response.

### Calculation

Verified rules, explicit date conventions, the applicable holiday calendar. Timestamps
display in Europe/Dublin local time. A rolling 24-hour approximation is unacceptable.

### Display

Every countdown shows milestone label, exact due date, working days remaining or
overdue, completion status and the next permitted action.

- "Acknowledgement due in 2 working days — 14 November 2026".
- "Progress update due today".
- "Acknowledgement overdue by 1 working day".
- "40-working-day point passed — unresolved notification required".
- "Acknowledged 12 November 2026 — within deadline".

Completed milestones retain due and completion dates. Overlapping obligations display
together. Text or icons accompany colour. Accuracy must not depend on the scheduler
having run.

### Continued updates

The unresolved notification neither closes the case nor ends update obligations.

Acknowledgement → progress updates → unresolved notification → further progress updates
→ approved final response → closure.

There is no maximum number of updates. Each is its own message and milestone. Sending
anything leaves the receipt date, the 40-working-day target and the final-response
deadline unchanged. Where one verified message satisfies two obligations, both milestones
are completed by it and the combination is recorded.

## 10. Correspondence

### Message types and recipients

1. Acknowledgement.
2. Progress update, repeatable before and after the 40-working-day point.
3. Unresolved-at-40-days notification.
4. Final response.

Each message also records a recipient type: complainant, product provider or insurer, or
internal. Internal messages are staff notices containing references and links, never
narrative. Provider correspondence is necessary where the investigation depends on the
insurer, so it travels through the same outbox and log rather than by private email.

Any substantive outgoing message goes through one of these four types, so no case
communication escapes the log. A request for further information is sent as a progress
update. Inbound telephone or email contacts are summarised in the investigation record;
no separate case-note type exists in the minimum release.

### Approval and confirmation

Acknowledgement, progress update and unresolved notification require handler
confirmation only. They carry no outcome or redress determination, and placing a reviewer
in their path would jeopardise the deadlines they exist to meet.

The final response requires independent approval of the exact package. If a notification
ever contained a determination, it would be a final response by definition.

### Templates

Fixed and version-controlled, with the version recorded on every message so later edits
cannot rewrite what was sent. Unresolved and final-response templates must state referral
rights; exact wording is a Section 5 verification task and a Section 16.1 criterion.

### Flow

Prepare → preview → confirm or approve → persist → attempt send → record result.

The outbox record is written before the provider is called. It stores recipient, recipient
type, subject, body, template version, actor, approval reference where applicable,
timestamps, status, provider reference and error summary.

### Editability

A message is editable only while its status is draft and no live approval refers to it.
Editing after a return is an in-place edit of that draft, because the returned approval is
no longer live and the reviewed content is preserved in the approval snapshot.

Authorisation freezes content. A frozen message may be retried with unchanged content but
never edited. Changing it means withdrawing approval and submitting a new final response.

### Statuses

draft, sending, provider_accepted, failed, acceptance_unknown.

`acceptance_unknown` means provider acceptance is unknown. It never describes delivery,
and acceptance is never described as delivery or reading.

### Failure and uncertainty

Failed and uncertain messages stay visible in the case and the operational queue and never
complete a milestone.

Definite failures may be retried with unchanged content on the same authorised record,
recorded as a new attempt.

Unknown acceptance requires a recorded resolution by a compliance reviewer: confirm
acceptance with supporting evidence, or authorise a replacement send. Both are audited. The
scheduled check flags any message left in sending beyond a configured age as
acceptance_unknown and never resends automatically.

### Controlled live sending

Only allowlisted addresses receive real mail, enforced in the send service rather than the
interface, checked after final address resolution. No unrestricted CC or BCC. Content is
synthetic with a demonstration notice. Credentials stay outside Git and AI tools. Automated
tests use a fake transport; a separate controlled test demonstrates real delivery.

## 11. Investigation, outcome and approval

Investigation records: findings, root-cause category, outcome, outcome rationale, redress
amount and completion timestamp. No guided root-cause framework is required.

Root-cause category, product and complaint category are closed enumerations in
version-controlled configuration, not free text. Adding a value is a code change.

Outcomes: Upheld, Partially upheld, Not upheld. Redress is recorded, including zero, and is
not paid by the application.

`Investigation.completed_at` is set on submission for approval and cleared on a return, so
the final-response clock stops until resubmission, which sets a new value and recalculates
the deadline. Whether a return should restart a statutory clock is an interpretation
question recorded in Section 5, not an assumption.

On submission the system stores an immutable snapshot of the reviewed package — the
investigation fields for that revision plus the exact final-response recipient type,
recipient, subject and body — on the Approval record, with a hash of that snapshot.

### Return and resubmission

A return must state a reason in the decision comment, and may include recommendations or
change requests for the handler.

The handler may then edit the package and resubmit, accompanying the resubmission with a
note recording what changed and any disagreement with the recommendations. The note is
optional; the reviewer's decision is not deferred by its absence.

The approver has absolute authority. There is no appeal, no override, no conditional
approval and no closure without a valid approval. Recorded disagreement informs the next
decision but cannot compel it. Itemised change requests with per-item handler responses are
an optional enhancement.

Each round creates a new Approval row, so the sequence of comments, recommendations,
submission notes and decisions is the history.

Approval validity is checked when the decision is made and again inside the send and close
transactions. A revision check rejects a stale submission rather than overwriting a newer
decision.

## 12. Logical data model

| Entity | Purpose |
|---|---|
| User | Identity, single role, activation |
| Complainant | Contact details, separate from case narrative |
| Complaint | Receipt details, handler, classification, lifecycle |
| Investigation | Findings, root cause, outcome, redress, revision, completion |
| Approval | Submission snapshot, revision, decision, recommendations, note |
| Correspondence | Outbound content, type, recipient type, milestone link, status |
| SendAttempt | Attempt result, provider reference, error, uncertainty resolution |
| Milestone | Obligation, sequence, due date, completion, supersession |
| ScheduledRun | Job name, period key, status, timestamps, error |
| AuditEvent | Actor, time, action, change details |
| PublicHoliday | Date, name, calendar |

This is a logical model, not a table-count target. Separating complainant details supports
permission design but is not anonymisation; message bodies and findings also contain personal
data.

A case-note entity and an investigation-revision table are deferred; the approval snapshot
provides the evidence a revision table would otherwise hold.

## 13. Logical screens

Dashboard: open cases, acknowledgements due, updates due, day-40 cases, responses due,
pending approvals with queue age, cases returned more than once, failed and uncertain sends.
Urgent actions precede totals.

Complaint list: reference, state, handler, received date, next milestone, next action.
Filters for state, handler, date range, category and overdue status. A CSV export control
applies the same filters and permissions.

The export contains reference, state, handler, received date, milestone dates, outcome and
closure date. It excludes narrative fields and personal contact details, and every export is
audited.

Intake: required fields, explicit receipt date, contact validation, handler selection,
confirmation of calculated milestones.

Complaint detail: header with reference, state, handler and milestone panel; sections for
summary, investigation, outcome and approval, correspondence, audit history. Role-appropriate
actions are shown and independently enforced.

Correspondence composer: type, recipient type, template, required fields, preview, allowlisted
recipient, approval status, confirmation, clear send outcome.

Approval queue: pending packages with age, read-only snapshot, prior comments and submission
notes, approve or return, mandatory comment.

Receipt correction: reviewer-only form showing current date, new date, reason, and the
milestone changes the correction will cause before confirmation.

No configuration screens exist in the minimum release. Detailed visual design is left to the
UI specification.

### Responsive and mobile behaviour

One responsive website. The following rows are committed for the screens listed above.

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
| Scheduled | Daily deadline check, stuck-send check, staff digest |
| Event-triggered | Intake creates milestones and an acknowledgement draft; a completed message completes its milestone; submission opens an approval |
| Human | Approval blocks release of a final response; unknown acceptance requires recorded resolution |

Nothing substantive to a complainant is sent because a timer fired. Monitoring prompts a
human to act.

Each scheduled run records job name and period key, so a rerun cannot duplicate a digest for
the same period. Failures and the last successful run are recorded. Digest recipients are
allowlisted like any other recipient.

## 15. Security, privacy and operations

- Authentication with password hashing, CSRF protection, secure cookie and session settings,
  and server-side validation.
- Idle session expiry, and throttling of repeated failed logins with the block recorded in
  the audit trail.
- Authenticated users may change their own password. Email-based reset and multi-factor
  authentication are optional enhancements and are disclosed as limitations.
- Authorisation on every protected request and record access.
- Audit of approvals, returns, invalidations, receipt corrections, denials, correspondence
  attempts, uncertainty resolutions, exports and CLI provisioning.
- UPDATE and DELETE on the audit table revoked for the application database role in
  PostgreSQL, so append-only behaviour is enforced by the database rather than by application
  code alone. Database-owner access remains a documented limitation.
- Operational logs kept separate from audit evidence, without secrets or narrative.
- Synthetic data only, with production legal basis described separately.
- A documented procedure for data-subject access, correction and erasure requests, including
  who performs it and how the audit trail is respected. No automated request handling.
- Retention: a documented policy only. No deletion feature exists, and that is stated as a
  limitation.
- Backup and restore, access review, incident response, change control and ownership in the
  governance policy.
- Monitoring of health, errors, scheduled-run failures and send failures.
- Accessible labels, keyboard navigation, visible focus, contrast, clear errors and non-colour
  status indicators, with real failures reported honestly.
- Persistent storage and a documented recovery route.

## 16. Success criteria and release priorities

### 16.1 Minimum release — committed scope

**Complete journey**

1. Using separate handler and compliance accounts, complete intake → investigation →
   submission → independent approval → final-response sending → closure.
2. Record actual receipt date and channel separately from creation time, reject future dates,
   and keep the date read-only to ordinary editing.
3. Support a reviewer-only receipt correction that requires a reason, audits old and new
   values, supersedes rather than deletes prior milestones, and recalculates deadlines.
4. Record findings, root-cause category, outcome, rationale and redress using fixed
   enumerations, and reject submission while any is missing.
5. Enforce the approve-and-return loop: a return requires a comment and may add
   recommendations; resubmission may carry a note of changes and disagreement; the approver's
   decision is final and unappealable.
6. Refuse closure unless every gate in Section 8 is satisfied, naming each unmet gate.

**Identity, permissions, integrity**

7. Provide working authentication and server-side permissions. One handler must not read or
   modify another's complaint or export through any route.
8. Prevent self-approval, prevent role self-change, and enforce the handler, reviewer and
   single-role constraints at the data layer.
9. Refuse deactivation of a user holding open complaints, listing the blocking references.
10. Keep correspondence editable only in draft with no live approval, freeze content on
    authorisation, and require invalidation before approved content changes.
11. Audit approvals, returns, invalidations, corrections, denials, exports, uncertainty
    resolutions and CLI provisioning, with entries not editable through the application.

**Deadlines**

12. Calculate every milestone from verified rules, and pass independently checked examples
    covering ordinary dates, weekends, applicable holidays and a year boundary.
13. Display each milestone with exact due date and text status, retaining due and completion
    dates of completed milestones after later updates and after a receipt correction.
14. Support repeated progress updates before and after the 40-working-day notification without
    changing the receipt date or resolution target, demonstrated with at least two
    post-notification updates.

**Correspondence**

15. Send all four message types with recipient type and version-controlled templates, and
    confirm that unresolved and final-response templates state referral rights.
16. Restrict real sends to server-side allowlisted addresses, persist content before sending,
    and log recipient, recipient type, content, actor, timestamps and result.
17. Distinguish provider acceptance, definite failure and unknown acceptance, never describe
    acceptance as delivery, and keep unresolved messages visible without completing milestones.
18. Permit retry of definite failures with unchanged content, and require a recorded, audited
    resolution of unknown acceptance before any replacement send.
19. Confirm acknowledgement, update and notification messages with the handler alone, and
    approve only the final response.

**Interface and automation**

20. Provide dashboard, complaint list with CSV export, intake, complaint detail, approval queue
    and receipt correction, using basic counts rather than advanced reporting.
21. Support keyboard operation and a 375 CSS pixel viewport for the committed journey without
    horizontal scrolling or hidden essential controls, with identical permissions across sizes.
22. Produce an idempotent staff digest from the scheduled check, recording each run and its
    failures.

**Delivery, security and evidence**

23. Preserve data across restarts, run the deployed application on PostgreSQL, and rebuild it
    from a clean checkout using the documented Docker procedure.
24. Pass the test suite in Section 17, including stale-revision rejection, digest idempotency
    and receipt-correction recalculation, against PostgreSQL.
25. Add password change, idle session expiry, login throttling and database-level protection of
    the audit table, plus a documented data-subject-request procedure.
26. Retain security-scan results and the recorded response to each finding, with no secrets in
    the repository or AI tools.
27. Provide repository, deployment instructions, governance policy, monitoring evidence,
    privacy and accessibility review, AI-use log and declaration, technical write-up and live
    demonstration.

### 16.2 Optional enhancements

Only after Section 16.1 is evidenced and remaining assessment work is reserved: itemised
change requests with per-item handler responses, handler reassignment, browser-based
administration with an administrator role, case notes, attachments, delivery webhooks,
background queue, advanced reporting, editable templates, extended device coverage,
expedited early-resolution path, password reset by email and multi-factor authentication.

Optional status removes no security requirement. Anything implemented carries its permissions,
validation, audit and tests.

### 16.3 Implementation choices

- Users are created and deactivated by a documented CLI command that refuses to remove the
  last compliance reviewer or a handler with open cases.
- The holiday calendar is loaded from a verified dataset covering the test period and the
  following year.
- Templates are files in version control.
- One email provider is called inline; no queue or worker.
- Early-resolved complaints follow the normal journey.
- No reassignment or administrative routes exist.

### 16.4 Delivery checkpoints

Commit this baseline before implementation and retain earlier versions in Git.

- Week 1: Section 5 register complete for every rule that drives code; email sending proven as
  a spike to an allowlisted address.
- Week 5: criteria 1–6 and 12–14 demonstrable end to end.
- Anything unfinished at the week-5 checkpoint becomes a disclosed limitation rather than a
  reason to extend the build.

Do not redefine success to match whatever was built.

## 17. Test strategy

- Unit: working-day arithmetic, milestone generation and regeneration, receipt-correction
  recalculation, state transitions, approval invalidation, stale-revision rejection.
- Integration: persistence, permissions, transactional approve and close, correspondence
  logging, approval snapshot retention, export scoping.
- Approval loop: return without comment rejected, resubmission creating a new revision,
  approver decision final, closure refused with an invalidated approval.
- Closure gates: one negative test per unmet gate, including missing findings, missing or
  invalidated approval, missing final-response send, unauthorised closure, and a
  missing-notification case where approval and sending did not both occur before the
  40-working-day point.
- Closure success: one closure after all gates pass, and one case approved and closed before
  the 40-working-day point with no notification sent.
- Negative: self-approval, cross-handler access, role self-change, deactivating a user with
  open cases, non-allowlisted recipient, editing a frozen message, editing under live approval.
- Correspondence: success, definite failure, unknown acceptance and its resolution, retry
  without duplication, stale sending flagged by the scheduled check.
- Scheduling: idempotent digest for a repeated period key, recorded failure.
- Browser: one main end-to-end journey and key blocked actions.
- PostgreSQL: full suite against the deployment database before submission.
- Security: appropriate scanners for source, dependencies, container and deployed application,
  with triage and remediation or acceptance recorded.
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
- Governance policy, operational runbook and data-subject-request procedure.
- Architecture and modularity note, data model and DFD/STRIDE evidence.
- Approximately 2,500-word technical write-up with Harvard references and cover page.
- AI-usage log and AI Fluency declaration appendix.
- Live demonstration in Week 12 with a recommendation supported by observed results.

The assessment prohibits AI authorship of the design-decision analysis, security findings
discussion, accessibility review and limitations section. Those remain the student's own work.

## 19. Delivery approach

1. Commit scope, rule register and success criteria.
2. Establish repository, Flask skeleton, PostgreSQL in Docker Compose, authentication.
3. Complete the Section 5 register for code-driving rules; prove email sending as a spike.
4. Implement and test receipt, correction and deadline logic.
5. Deliver the case journey with milestones, approval, audit and closure gates.
6. Add correspondence, fake transport and uncertainty handling.
7. Integrate allowlisted real sending and test failure and uncertainty.
8. Complete tests, scans, accessibility, hardening and monitoring.
9. Complete governance evidence, the deployed demonstration and the written report.

Submission is at the end of Week 11 with the demonstration in Week 12. Confirm dates against
the timetable.

Available hours remain unconfirmed; plan conservatively around work and family commitments and
re-estimate after the first working slice.

## 20. Open decisions

- Verified provisions, counting conventions and referral wording.
- Hosting provider.
- Email provider, test recipients and the uncertainty age threshold.
- CSS approach and visual design.
- Interpretation of the final-response clock after a return.
- Any lecturer requirement to use a specific development database.
- Confirmed timetable and sustainable weekly effort.

## 21. Reference and evidence register

Primary coursework source: MCLCD_Oct26_CA2_LowCodeNoCodeAIDev.docx, read 9 November 2026.
It specifies repository, testing, Docker, deployment, governance, accessibility, AI
declaration and demonstration requirements.

Additional supplied source: Low-Code-No-Code-Project-Brief.pdf. Its status alongside CA2 must
be confirmed; earlier ERD, automation, access-control, DFD, STRIDE and data protection planning
should be preserved where applicable.

Sources to verify and cite by provision:

- Central Bank of Ireland, Consumer Protection Code 2025 (statutory instrument or code — status
  to be confirmed).
- Central Bank of Ireland, General Consumer Protection Requirements (confirm whether this is a
  separate instrument).
- Central Bank of Ireland, Investment Firm and Intermediary Newsletter, June 2026 (guidance,
  not law).

## 22. Revision history

| Version | Change |
|---|---|
| 0.2 | Initial product definition and specification. |
| 0.3 | Minimum release introduced; committed and optional scope separated; closure gates consolidated. |
| 0.4 | Contradictions resolved: no post-approval editing, approval snapshots, milestone records, acceptance uncertainty, permission matrix, scheduled-run records, single scope table, single test list. |
| 0.5 | Approval confined to the final response; approve-return-resubmit loop with recommendations and submission notes; receipt correction and CSV export promoted; PostgreSQL only; modular architecture and over-engineering guardrail; baseline authentication hardening; milestone supersession; recipient types. |

Superseded statements, retained only as record:

- An earlier draft implied a late-Friday cut-off; no such rule is modelled.
- An earlier draft treated 8 January as a submission date; the timetable governs.
- An earlier draft described features as belonging to "the original concept"; Section 3
  governs scope.
- An earlier draft used a precedence rule letting Section 16 override other sections; v0.4
  resolved the contradictions instead.
- Earlier drafts used "MVP", "minimum assessed release" and "minimum implementation"; this
  document uses "minimum release".
- Earlier drafts required independent approval of every message; v0.5 confines approval to
  the final response.

---

# Appendix A — Specification

## Purpose

An internal complaints-management application for handlers and compliance reviewers in a
small Irish insurance intermediary. It replaces spreadsheets and disconnected email with
deadline tracking, independent approval of outcomes, logged correspondence and an auditable
history.

## Entities

### User
- id (integer, primary key)
- name (text, required)
- email (text, required, unique)
- password_hash (text, required)
- role (one of: handler, compliance)
- active (boolean, default true)
- created_at (timestamp)

An administrator role is deferred to Section 16.2.

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
- handler_id (foreign key to User, required; must hold the handler role)
- received_date (date, required; changed only through the correction action)
- received_time (time, optional)
- received_channel (one of: email, phone, letter, in_person, other)
- receipt_note (text, required)
- product (enum, required)
- category (enum, required)
- description (text, required)
- status (one of: logged, investigating, pending_approval, approved, closed)
- closed_at (timestamp, optional)
- created_at (timestamp)
- updated_at (timestamp)

Due dates are not stored here; they derive from Milestone records.

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
- comment (text, required when a decision is recorded; states the reason for a return)
- recommendations (text, optional; change requests on a return)
- submission_note (text, optional; handler's record of changes and disagreement)
- package_snapshot (structured data, required; immutable copy of the reviewed
  investigation fields and final-response recipient type, recipient, subject and body)
- content_hash (text, required)
- submitted_at (timestamp, required)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)

### Correspondence
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- milestone_id (foreign key to Milestone, optional)
- message_type (one of: acknowledgement, progress_update, unresolved_notification,
  final_response)
- recipient_type (one of: complainant, provider, internal)
- recipient_email (text, required before sending)
- subject (text, required before sending)
- body (text, required before sending)
- template_version (text, required)
- status (one of: draft, sending, provider_accepted, failed, acceptance_unknown)
- authorised_by_id (foreign key to User, optional until confirmed or approved)
- authorised_at (timestamp, optional)
- provider_accepted_at (timestamp, optional)
- created_at (timestamp)
- Editable only while draft and not referenced by a pending or approved, non-invalidated
  Approval.

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
- sequence (integer, required)
- due_date (date, required)
- completed_correspondence_id (foreign key to Correspondence, optional)
- completed_at (timestamp, optional)
- superseded_at (timestamp, optional; set only by receipt correction)
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
- change_details (structured data, optional)
- created_at (timestamp)
- Append-only; UPDATE and DELETE revoked from the application role.

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
| POST | /login | Authenticate, throttled on repeated failure |
| POST | /logout | End session |
| POST | /account/password | Change own password |
| GET | / | Dashboard with milestones, queue age and urgent actions |
| GET | /complaints | List and filter authorised complaints |
| GET | /complaints/export | CSV export of the filtered, authorised register |
| GET | /complaints/new | Show intake form |
| POST | /complaints | Create complaint and generate milestones |
| GET | /complaints/<id> | Show case, milestones, correspondence and audit |
| POST | /complaints/<id>/investigation | Save investigation draft |
| POST | /complaints/<id>/receipt-correction | Reviewer correction with reason and recalculation |
| POST | /complaints/<id>/correspondence | Create a controlled draft |
| POST | /correspondence/<id>/edit | Edit a draft not under live approval |
| GET | /correspondence/<id>/preview | Preview recipient, subject, body and approval status |
| POST | /correspondence/<id>/send | Confirm or approve, persist, then attempt send |
| POST | /correspondence/<id>/retry | Retry a definite failure with unchanged content |
| POST | /correspondence/<id>/resolve-uncertainty | Record acceptance evidence or authorise resend |
| POST | /complaints/<id>/submit-outcome | Snapshot the package and open approval |
| GET | /approvals | Review queue with ages and prior rounds |
| POST | /approvals/<id>/decision | Approve or return the snapshotted package |
| POST | /complaints/<id>/return-to-investigation | Invalidate approval and reopen investigation |
| POST | /complaints/<id>/close | Enforce every closure gate in Section 8, then close |
| GET | /health | Minimal health status without sensitive information |

### Optional routes

Deferred to Section 16.2.

| Method | Path | Does |
|---|---|---|
| POST | /complaints/<id>/assign | Reassign the handler with audit |
| POST | /complaints/<id>/notes | Add a case note |
| POST | /complaints/<id>/attachments | Upload an attachment |
| GET | /admin/users | Account-management screen |
| POST | /admin/users/<id>/update | Change role or activation with audit |
| GET | /admin/holidays | Holiday configuration |
| POST | /admin/holidays | Add a verified holiday entry with audit |
| POST | /account/reset | Password reset by email |

## Technical constraints

- Python and Flask with versions pinned in the repository.
- PostgreSQL for development, testing and deployment, run through Docker Compose.
- Flask-SQLAlchemy for persistence and Alembic for migrations; every schema change via migration.
- Application factory with feature blueprints, service layer and pure deadline functions.
- Enumerations, status values and tunable values in one configuration module.
- Jinja templates grouped by feature; no separate JavaScript frontend framework.
- Responsive interface supporting the committed journey at 375 CSS pixels.
- No abstraction before two call sites; no plugin, DI container, workflow engine or event bus.
- Authentication, password hashing, CSRF protection, idle session expiry and server-side
  validation.
- Login throttling on repeated failure, with blocks audited.
- Reject future receipt dates and validate required intake fields server-side.
- Permissions enforced on every request, service call and query, including direct requests.
- Handlers reach assigned cases only; reviewers reach all cases but never decide a case they
  handled.
- Handler, reviewer and single-role constraints enforced at the data layer.
- A user holding open complaints cannot be deactivated.
- Receipt dates change only through the audited correction action, which supersedes prior
  milestones and recalculates them.
- Correspondence editable only in draft and only outside a live approval; frozen on
  authorisation.
- Approval applies to the final response only; acknowledgement, update and notification
  messages are handler-confirmed.
- Approver decisions are final; no appeal, override or conditional approval.
- Approved content never edited; change requires invalidation and resubmission.
- Closure requires every gate in Section 8.
- Provider acceptance is never described as delivery.
- All four message types are sent through the app with a recipient type and logged
  automatically.
- Progress updates are repeatable before and after the 40-working-day point and never reset the
  receipt date or resolution target.
- Milestones are stored per obligation; current deadlines derive from open, non-superseded
  milestones.
- Deadline calculation uses verified rules and the applicable working-day calendar.
- Countdowns show label, exact date and text urgency.
- Outbound content is persisted before any send attempt.
- Real sending restricted server-side to allowlisted addresses; no unrestricted CC or BCC.
- Failed and uncertain sends remain visible and never complete milestones.
- Unknown acceptance requires a recorded, audited resolution before any replacement send.
- Scheduled runs are idempotent per job and period and record failures.
- CSV export respects record permissions, excludes narrative and contact detail, and is
  audited.
- Synthetic data only; credentials from environment configuration, never in Git or AI tools.
- Scheduled work runs through a documented CLI command, not a web route.
- Users are provisioned and deactivated by CLI; holidays from a verified dataset; templates
  version-controlled.
- Audit table protected by revoked UPDATE and DELETE for the application role.
- Retention is a documented policy only; no deletion feature is implemented.
- Dockerfile, deployment documentation, persistent database, automated tests, scan evidence and
  meaningful Git history required.
- Exact regulatory interpretations, hosting provider and email provider must be verified or
  selected before implementation.

## Out of scope

Excluded capabilities are listed in the single scope table in Section 3. Items marked Optional
are deferred, not excluded; items marked Out of scope are not delivered in this release.



# Appendix B — Regulatory requirements register

This appendix records the provisions that drive the deadline engine and the
correspondence templates. It is the completion of Section 5 for every rule that affects
code. Rows marked "to confirm" must be read in the full text before their paragraph
letters are quoted in the write-up.

## B.1 Instrument and status

| Item | Detail |
|---|---|
| Instrument | Central Bank (Supervision and Enforcement) Act 2013 (Section 48) (Consumer Protection) Regulations 2025 |
| Citation | S.I. No. 81 of 2025 |
| Made | 24 March 2025 |
| Commencement | 24 March 2026 |
| Nature | Regulations made under section 48 of the 2013 Act; "Consumer Protection Code 2025" is the working name for this instrument |
| Complaints chapter | Chapter 12 of Part 2 |
| Key provisions | Regulation 105 (procedure for managing and resolving complaints), Regulation 106 (complaint log), Regulation 107 (analysis of complaints) |

Two clarifications that were previously open questions in this document:

- The "General Consumer Protection Requirements" is **Part 2 of the same instrument**, not
  a separate instrument. There is one instrument to cite, with numbered Parts.
- The June 2025 insurance newsletter located during verification refers to the **2012
  Code** and to "business days". It is superseded terminology and must not be used to
  interpret the 2025 Regulations.

## B.2 Definition of working day

The Code defines a working day as a day which is not a Saturday, a Sunday, **Good Friday**,
or a public holiday within the meaning of the Organisation of Working Time Act 1997.

Three consequences for the implementation:

- Good Friday is excluded explicitly. A holiday dataset built from bank-holiday lists will
  usually omit it, so it must be seeded deliberately and tested.
- The public holiday set is that of the 1997 Act, which includes the usual nine public
  holidays plus any day declared by ministerial order. The dataset must be dated and
  versioned.
- Saturday and Sunday are excluded by definition, so no separate weekend rule is required
  and no "if Saturday then Monday" adjustment exists. Any such logic in the code would be
  an invented rule.

### Worked examples (illustrative until checked against the seeded calendar)

| Scenario | Calculation | Due |
|---|---|---|
| Received Thursday 22 October 2026; Monday 26 October is the October public holiday | Fri 23 = 1; Mon 26 excluded; Tue 27 = 2; Wed 28 = 3; Thu 29 = 4; Fri 30 = 5 | Friday 30 October 2026 |
| Received Wednesday 24 March 2027; Good Friday 26 March 2027 | Thu 25 = 1; Fri 26 excluded; Mon 29 = 2; Tue 30 = 3; Wed 31 = 4; Thu 1 April = 5 | Thursday 1 April 2027 |

Both examples assume the clock starts on the next working day after receipt. That
convention is the one open interpretation remaining: the provisions state deadlines in
working days from receipt but do not state whether the day of receipt counts. Adopt one
convention, record it here, and demonstrate the alternative in the write-up.

## B.3 Complaint handling obligations

| Obligation | Provision | Requirement | System behaviour |
|---|---|---|---|
| Written procedure | Reg 105(1) | Implement a procedure for managing and resolving complaints | Reflected in the workflow and governance policy; not a system feature |
| Acknowledgement | Reg 105(4) | Acknowledge in writing within 5 working days, with procedure details, ombudsman information and contact details | Acknowledgement draft created at intake; 5-working-day milestone; handler-confirmed, no approval |
| Named contact | Reg 105(4) | Provide a point of contact until resolved or all steps exhausted | Handler name and contact recorded on the acknowledgement and shown on the case |
| Progress updates | Reg 105(4)(d) | Regular written updates at intervals no greater than 20 working days, starting from the date of receipt | Repeating progress-update milestone at receipt + 20, +40, +60 working days; never reset by a send |
| Reasonable efforts | Reg 105(4) | Investigate and make reasonable efforts to resolve within 40 working days of receipt | 40-working-day resolution target; breach shown as overdue, not as a blocking state |
| Unresolved at 40 days | Reg 105(4) | Notify the anticipated timeframe, the ombudsman referral right and the ombudsman's contact details | Unresolved-notification milestone and mandatory template fields |
| Final response | Reg 105(4) | Within 5 working days of completion of the investigation, state the decision and reasons, any offer or settlement terms, the ombudsman right and contact details | Final-response milestone created on submission; deadline recalculated on resubmission |
| Early resolution | Reg 105(3) | Procedure need not apply where resolved to the consumer's satisfaction within 5 working days of receipt, provided a record is kept | Normal journey retained; the log entry remains mandatory |

The 40-working-day point is a reasonable-efforts target and a communication trigger. It is
not an automatic closure deadline, and a complaint may remain open afterwards.

## B.4 Mandatory template content

These fields are acceptance criteria, not optional wording.

| Template | Mandatory content |
|---|---|
| Acknowledgement | Reference and date received; summary of the complaint as understood; the procedure and expected timeframe; named contact; ombudsman referral right and contact details |
| Progress update | Reference; what has been done since the last update; what remains; next expected update date; named contact |
| Unresolved notification | Reference; statement that the complaint is not yet resolved; anticipated timeframe; ombudsman referral right and contact details |
| Final response | Reference; decision and reasons; any offer, redress or settlement terms; ombudsman referral right and contact details; time limit for referral where applicable |

The ombudsman is the Financial Services and Pensions Ombudsman. Contact details must be
kept current and stored with the template version, because a later change of details must
not retrospectively alter what was sent.

## B.5 Complaint log requirements

Regulation 106 requires a complaint log. The fields it implies, and where each is held:

| Log field | Held in |
|---|---|
| Core reason or category of complaint | `Complaint.category`, with `root_cause_category` on Investigation |
| Date received | `Complaint.received_date`, with correction history in `AuditEvent` |
| Summary of the response and its date | Final-response `Correspondence` and `Investigation.outcome_rationale` |
| Other correspondence | All `Correspondence` rows, with recipient type and timestamps |
| Steps taken to resolve | Investigation findings and the milestone sequence |
| Resolution date | Closure timestamp; to be added explicitly if the export must show it separately |
| Status of any ombudsman referral or appeal | Not modelled. Record as a disclosed limitation, or add a single optional status field |

The last row is the only genuine gap against Regulation 106. Either add one optional field
or state plainly that the prototype ends at closure and does not track ombudsman outcomes.

## B.6 Analysis obligation

Regulation 107 requires periodic analysis of complaints, at least every six months. This is
out of scope for the prototype. It must appear in the limitations section as a regulatory
obligation the application does not support, and Section 3 should list it as out of scope
rather than optional.

## B.7 Superseded terminology

| Term | Status |
|---|---|
| "Business day" | Used by the 2012 Code and by the June 2025 newsletter. Superseded for this project |
| "Working day" | The 2025 term, with the Good Friday exclusion |
| "40 days" without qualification | Incorrect. The requirement is 40 working days |

Code, tests, user-facing text and the write-up must all use "working day". The word
"business day" should appear nowhere except where quoting the older source as history.

## B.8 Outstanding checks

- Confirm whether the day of receipt counts as the first working day.
- Confirm the paragraph letters within Regulation 105(4) for acknowledgement, contact,
  updates, resolution and final response before quoting them individually; only
  subparagraph (d) for updates is confirmed here.
- Confirm the definition's regulation number in Part 1; only its substance is confirmed.
- Confirm the referral time limit wording that must appear in the final response.
- Confirm whether any complaint category relevant to insurance intermediaries is excluded
  from Chapter 12.
- Verify that the June 2026 newsletter cited in Section 21 exists; if not, replace it.

## B.9 Sources

- Central Bank (Supervision and Enforcement) Act 2013 (Section 48) (Consumer Protection)
  Regulations 2025, S.I. No. 81 of 2025, Irish Statute Book.
- Central Bank of Ireland, Consumer Protection Code 2025, Part 1: Preliminary and General.
- Central Bank of Ireland, Consumer Protection Code 2025, Part 2: General Consumer
  Protection Requirements, Regulation 105.
- Central Bank of Ireland, redline of the section 48 provisions, paragraph-lettered version.
- Financial Services and Pensions Ombudsman, complaint process guidance for consumers.

This appendix records regulatory requirements for a coursework prototype. It is not legal advice, and it does not certify compliance.