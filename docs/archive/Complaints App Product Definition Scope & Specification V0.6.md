
# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.6 — 9 November 2026
Status: Minimum release baselined for implementation. Regulatory provisions verified at
Appendix B; remaining open interpretations recorded there.

## 1. Purpose

An internal web application for a small Irish regulated insurance intermediary. It manages
complaints from receipt through investigation, independent approval of the final response,
correspondence and closure, replacing a spreadsheet and disconnected email process with a
controlled case record, visible deadlines and an auditable history.

The application supports complaint handling under the Consumer Protection Code 2025. It is a
coursework prototype, not a certified compliance product. Statutory obligations, chosen
internal controls and prototype limitations are distinguished throughout.

The essential product is accurate deadline tracking, independent approval of the outcome
notified in the final response, correspondence sent through the application, and an audit
trail.

## 2. Intended users and operating context

- One small Irish insurance intermediary.
- Single organisation; no multi-tenancy.
- Handlers investigate their assigned cases and are the only users who create complaints.
- Compliance reviewers decide final responses independently and may correct a receipt date.
- Accounts are provisioned by a documented command-line procedure performed by an operator
  holding repository and hosting access. That privilege sits outside the application's
  permission model.
- Complainants have no account and no public portal. Some correspondence is addressed to the
  product provider or insurer rather than to the complainant.
- All records are synthetic. Real email reaches only controlled test addresses.
- Desktop-first, responsive on smaller screens, checked once at 375 CSS pixels.

The application cannot prevent a person holding database or hosting credentials from reading
complaint data outside the application. No role description claims otherwise.

### Stakeholders

The primary stakeholder is a complaints handler in a small intermediary who currently tracks
deadlines in a spreadsheet and keeps evidence in an inbox. Secondary stakeholders are the
compliance reviewer who must approve outcomes independently, and the firm's owner, who needs
to demonstrate a controlled process and produce a complaint log on request.

What has been validated: the workflow described here, against the provisions in Appendix B.
What has not been validated: no representative stakeholder has reviewed this design, and no
legal review has taken place. The write-up must not imply otherwise.

## 3. Scope boundary

| Capability | Status |
|---|---|
| Intake with actual receipt date and channel | Committed |
| Authorised receipt correction with recalculation | Committed |
| Verified working-day deadline calculation | Committed |
| Milestone records preserving due and completion dates | Committed |
| Countdown display with exact dates and text urgency | Committed |
| Investigation, outcome and redress with fixed categories | Committed |
| Independent approval of the final response | Committed |
| Approve, return with comment, resubmit | Committed |
| Approval invalidation before any post-approval change | Committed |
| Four correspondence types, complainant, provider or internal recipient | Committed |
| Outbox record, allowlist, failure handling, acceptance tracking | Committed |
| Repeated progress updates before and after the 40-working-day point | Committed |
| Scheduled deadline check with idempotent staff digest | Committed |
| CSV export of the authorised register | Committed |
| Audit trail covering decisions, denials, corrections and sends | Committed |
| Baseline authentication hardening | Committed |
| Responsive main journey, checked at 375 CSS pixels, failures reported | Committed |
| Docker deployment on PostgreSQL | Committed |
| Entity relationship diagram | Committed |
| Level-1 data flow diagram with trust boundaries | Committed |
| STRIDE threat table covering every boundary-crossing flow | Committed |
| Role and CRUD permissions table | Committed |
| GDPR write-up | Committed |
| Demonstration video and lecturer test accounts | Committed |
| Itemised change requests with per-item handler responses | Optional |
| Handler reassignment | Optional |
| Browser-based user, role and holiday administration | Optional |
| Case notes as a separate record type | Optional |
| Attachments and document uploads | Optional |
| Delivery and bounce webhooks, provider reconciliation | Optional |
| Background queue and automated retry scheduling | Optional |
| Advanced reporting, charts and further exports | Optional |
| Editable correspondence templates | Optional |
| Login throttling and lockout | Optional |
| Password reset by email, password change screen, multi-factor authentication | Optional |
| Browser end-to-end test automation | Optional |
| Expedited early-resolution workflow | Optional |
| Public intake, complainant accounts, self-service portal | Out of scope |
| Inbound email ingestion and mailbox integration | Out of scope |
| AI classification, summarisation or automated decisions | Out of scope |
| Redress payment and finance or policy-system integration | Out of scope |
| Multi-organisation operation | Out of scope |
| Configurable workflow designer | Out of scope |
| Automated retention deletion | Out of scope |
| Six-monthly complaint-pattern analysis required by Regulation 107 | Out of scope |
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
| Database | PostgreSQL for development, testing and deployment |
| Containerisation | Docker and Docker Compose |
| Version control | Git |
| Interface | Server-rendered pages; no separate frontend application |

Selected supporting components: Jinja templates, Flask-SQLAlchemy, Alembic, Flask-Login,
Flask-WTF, pytest, Gunicorn. Justification belongs in the write-up.

PostgreSQL runs in Docker Compose from the first commit so local and deployed behaviour match.
If the brief mandates a different development database, it is a local convenience only and the
deployed system remains PostgreSQL.

### Platform choice

The build uses a custom Flask application rather than a low-code platform. The comparison
recorded in the write-up covers four dimensions:

| Dimension | Position |
|---|---|
| Scalability | A single-container application scales adequately for one small firm; a low-code platform imposes its own runtime limits and pricing tiers |
| Vendor lock-in | Application logic, schema and tests live in the repository; low-code equivalents live in a vendor's environment and are hard to export |
| Total cost | Hosting and database costs are minimal; low-code licensing is recurring and per-seat |
| Maintainability | Server-rendered Python with migrations and tests is inspectable and diffable; low-code changes are configuration edits with weaker review evidence |

The decisive factor for this assessment is that the brief requires migrations, tests, container
deployment and scan evidence, all of which the custom build produces directly. The low-code
implementation is assessed separately in the other deliverable.

### Architecture

Three rules, and nothing further:

1. Routes validate input and delegate; services hold business rules and transactions; models
   hold persistence. No rule logic in routes or templates.
2. Deadline rules are pure functions in one module, taking dates and returning dates, with no
   database access.
3. All enumerations, status values and tunable values live in one configuration module, with no
   string literals in logic.

Enumerations are validated text columns rather than database enum types, so adding a value is a
configuration change plus a validation update, not a migration. Package names follow the code as
built and are justified in the write-up.

### Over-engineering guardrail

- No abstraction before two call sites, and no mechanism that exists only for future
  flexibility.
- The three rules above are the permitted structure. Anything further needs justification
  against a specific risk.
- No plugin registry, dependency-injection container, configuration-driven workflow or event bus.
- Every dependency and helper module must remove more code than it adds, or be required by an
  assessment deliverable.
- A feature added maps to a committed criterion; a feature removed deletes its route, template
  and tests together.

## 5. Regulatory requirements register

The full register, with citations, worked examples and outstanding checks, is Appendix B. This
section records only what drives code and what remains open.

Verified and implemented:

- Working day excludes Saturdays, Sundays, Good Friday and public holidays under the
  Organisation of Working Time Act 1997.
- Acknowledgement within five working days, with procedure details, named contact and ombudsman
  information.
- Progress updates at intervals no greater than twenty working days, measured from the date of
  receipt.
- Reasonable efforts to resolve within forty working days, with a prescribed notification if
  unresolved.
- Final response within five working days of completion of the investigation, with decision,
  reasons, any offer terms and ombudsman information.
- Early resolution exception at five working days, with the log still required.

Still open, and recorded in Appendix B:

- Whether the day of receipt counts as the first working day.
- Whether a return restarts the final-response clock.
- The retention period, proposed as six years from closure and labelled unverified.
- Paragraph letters within Regulation 105(4) other than subparagraph (d).

Independent approval of the final response is a chosen internal control and must not be
described as a statutory requirement. Where the source is silent, the register records the gap
rather than an invented rule.

## 6. Roles, access and permissions

Two roles: handler and compliance. Each user holds exactly one role, which structurally prevents
self-approval.

### Actions by role

| Action | Handler | Compliance reviewer | Record scope |
|---|---|---|---|
| Create complaint | Yes | No | Handler self-assigns |
| Read complaint | Yes | Yes | Handler: assigned. Reviewer: all |
| Export register to CSV | Yes | Yes | Handler: assigned. Reviewer: all |
| Edit investigation | Yes | No | Assigned |
| Correct a receipt date | No | Yes | Any case, with reason and audit |
| Prepare and confirm acknowledgement, update or notification | Yes | No | Assigned |
| Submit final response for approval | Yes | No | Assigned |
| Approve or return the final response | No | Yes | Any case they did not handle |
| Send an approved final response | Yes | Yes | Handler: assigned. Reviewer: any |
| Retry a failed send | Yes | Yes | Same scope as sending |
| Resolve unknown acceptance | No | Yes | Any case |
| View audit history | Yes | Yes | Same read scope as the case |
| Invalidate approval and reopen investigation | Yes | Yes | Assigned (handler); any (reviewer) |
| Close complaint | Yes | Yes | Assigned (handler); any (reviewer) |
| Provision or deactivate users | No | No | Requires hosting or repository access |

### Data permissions

| Entity | Handler | Compliance | Enforced where |
|---|---|---|---|
| Complaint | Create own; read assigned; update state fields on assigned; no delete | Create none; read all; update receipt date and closure; no delete | Query filter plus service check |
| Investigation | Read and update on assigned; no delete | Read all; no update; no delete | Query filter plus service check |
| Approval | Read on assigned; create submission; no delete | Read all; create decision; no delete | Service check plus data constraint |
| Correspondence | Create and update drafts on assigned; no delete | Read all; approve final responses; no delete | Query filter plus service check |
| Milestone | Read on assigned | Read all | Derived from complaint scope |
| SendAttempt | Read on assigned | Read all | Derived from correspondence scope |
| AuditEvent | Read on assigned; no create outside service; no update or delete | Read all; no update or delete | Database privilege revocation |
| Complainant | Read and create with complaint | Read all | Derived from complaint scope |
| User | Read own profile | Read own profile | Service check; no route changes roles |
| PublicHoliday | Read | Read | Loaded by CLI only |
| ScheduledRun | None | None | Operator access only |

No role deletes complaint data, correspondence, approvals or audit events. There is no delete
route in the application.

### Enforced constraints

- `Complaint.handler_id` is required and must reference a user holding the handler role.
- `Approval.reviewer_id` is null until a decision, and when set must hold the compliance role and
  differ from the handler. Because roles are single-valued, this difference is guaranteed by the
  role check rather than by a separate comparison alone.
- No route changes a user's role; provisioning and deactivation are CLI operations, and the
  command refuses to remove the last active compliance reviewer or to deactivate a user holding
  open complaints.
- Permissions are checked in services and scoped queries, with tests proving that a direct
  request from the wrong user fails.
- Return-to-investigation is refused once the final response has reached provider acceptance. A
  pending approval may be abandoned by returning the case, which invalidates it.
- Approval validity is rechecked inside the sending and closing transactions.
- Denials are audited.

Terminology: a handler **confirms** a message; a reviewer **approves** a final response. The
authorising user of a final response is the approving reviewer, and the handler who sends it is
recorded separately in the audit trail.

## 7. Receipt capture and correction

Required intake information: complainant name and controlled contact address; actual received
date and time where required; channel; receipt evidence note; product, category and description;
assigned handler; system-generated reference and creation timestamp.

The receipt date drives every deadline and never defaults to the entry date. Future dates are
rejected and required fields validated server-side.

The date is read-only to ordinary editing. A compliance reviewer may correct it through a
dedicated action requiring a reason, which audits the previous and new values and recalculates
milestones. Recalculation marks superseded milestones as superseded rather than deleting them and
creates replacements, so the earlier due dates remain visible as evidence of what was monitored.

After saving at intake, the calculated milestones are displayed immediately. There is no
pre-confirmation step.

## 8. Case lifecycle

States: Logged → Investigating → Pending Approval → Approved → Closed.

The first save of the investigation record moves Logged to Investigating. A return moves the case
back to Investigating, remains in the history, and resubmission creates a new Approval row at a
new revision.

Acknowledgement and progress updates are correspondence milestones, not states.

### Post-approval changes

Approved content is never edited. Any change requires returning the case to Investigating, which
invalidates the approval and is audited with actor, time and reason. This clears
`Investigation.completed_at`, as a return does, so the final-response clock stops until
resubmission recalculates it.

Closed case content is read-only. Reopening after closure is out of scope.

### Closure gates

A case may close only when every gate is satisfied. This list is the single definition.

1. Findings, root-cause category, outcome, outcome rationale and redress amount are recorded for
   the current investigation revision.
2. A reviewer other than the handler approved the current revision and the exact final-response
   content now held, and that approval is not invalidated.
3. That final response reached provider-accepted status.
4. Either the final response was provider-accepted on or before the 40-working-day due date, or an
   unresolved-at-40-days notification reached provider-accepted status before closure.
5. Closure is recorded as an audited transition by a user permitted by Section 6.

Gate 4 requires a notification only where the final response was not accepted on or before the
40-working-day due date. A notification sent late satisfies the gate while leaving the overdue
milestone visible.

Any milestone still open at closure is waived with an audit entry recording who waived it and
why, rather than being deleted or left open.

The minimum release models no discretionary closure exception. A case requiring an alternative
handling path cannot be closed, which is a disclosed limitation.

### Early resolution

Where a complaint is resolved to the consumer's satisfaction within five working days of receipt,
the full procedure need not apply, but the complaint must still be logged. The prototype uses the
normal journey for such cases and records the outcome, which satisfies the logging obligation.

## 9. Deadline engine and milestones

### Records

Each obligation is a stored milestone: complaint, type, sequence, due date, completion state,
completing correspondence, completion timestamp, and a superseded flag used only by receipt
correction. Milestones are never overwritten. Current deadlines derive from open, non-superseded
milestones.

Types: acknowledgement, progress update, unresolved notification, final response.

### Generation

- Acknowledgement at receipt plus five working days.
- Progress updates at receipt plus twenty, forty, sixty working days, and onward.
- Unresolved notification at receipt plus forty working days.
- Final response at the completion timestamp plus five working days.

### Display

Every countdown shows milestone label, exact due date, working days remaining or overdue,
completion status and the next permitted action. Examples:

- "Acknowledgement due in 2 working days — 13 November 2026".
- "Progress update due today".
- "Acknowledgement overdue by 1 working day".
- "40-working-day point passed — unresolved notification required".
- "Acknowledged 12 November 2026 — within deadline".

Completed milestones retain due and completion dates. Overlapping obligations display together.
Text or icons accompany colour. Accuracy must not depend on the scheduler having run.

### Continued updates

The unresolved notification neither closes the case nor ends update obligations. There is no
maximum number of updates, each is its own message and milestone, and sending anything leaves the
receipt date, the 40-working-day target and the final-response deadline unchanged. Where one
verified message satisfies two obligations, both milestones are completed by it and the
combination is recorded.

## 10. Correspondence

### Types and recipients

1. Acknowledgement.
2. Progress update, repeatable before and after the 40-working-day point.
3. Unresolved-at-40-days notification.
4. Final response.

Each message records a recipient type: complainant, product provider or insurer, or internal.
Internal messages are staff notices containing references and links. Provider correspondence
travels through the same outbox because investigations frequently depend on the insurer.

Any substantive outgoing message uses one of these four types, so no case communication escapes
the log. A request for further information is sent as a progress update. Other ad hoc messages
are out of scope. Inbound contacts are not summarised in the application; that is a disclosed
limitation.

### Approval and confirmation

Acknowledgement, progress update and unresolved notification require handler confirmation only.
The final response requires independent approval of the exact package, because it carries the
outcome and redress position.

### Templates

Fixed and version-controlled, with the version recorded on every message. Mandatory content per
type is defined in Appendix B: procedure details, named point of contact, ombudsman referral right
and contact details, and for the final response the decision, reasons, any offer terms and the
referral time limit.

### Flow and authorisation

Prepare → preview → confirm or approve → persist → attempt send → record result.

Authorisation is the act that freezes content: handler confirmation for the three non-final types,
reviewer approval for the final response. The outbox record is written before the provider is
called and stores recipient, recipient type, subject, body, template version, actor, approval
reference, timestamps, status, provider reference, attempt count and last error.

### Editability

A message is editable only while its status is draft and no live approval refers to it. Editing
after a return is an in-place edit of that draft, because the returned approval is no longer live
and the reviewed content is preserved in the approval snapshot. Authorisation freezes content
permanently; changing a sent message means withdrawing approval and submitting a new final
response.

### Statuses and failure

Statuses: draft, sending, provider_accepted, failed, acceptance_unknown.

`acceptance_unknown` means provider acceptance is unknown. It never describes delivery, and
acceptance is never described as delivery or reading.

Failed and uncertain messages stay visible and never complete a milestone. Definite failures may
be retried with unchanged content, recorded as a new attempt on the same authorised record.
Unknown acceptance requires a recorded resolution by a compliance reviewer: confirm acceptance
with evidence, or authorise a replacement send. The scheduled check flags any message left in
sending beyond a configured age as acceptance_unknown and never resends automatically.

### Controlled live sending

Only allowlisted addresses receive real mail, enforced in the send service and checked after final
address resolution. No unrestricted CC or BCC. Content is synthetic with a demonstration notice.
Credentials stay outside Git and AI tools. Automated tests use a fake transport, with a separate
controlled test of real delivery.

If real sending has not been proven by the feasibility checkpoint, the demonstration falls back to
a sandbox inbox, and the limitation is disclosed rather than hidden.

## 11. Investigation, outcome and approval

Investigation records: findings, root-cause category, outcome, outcome rationale, redress amount
and completion timestamp. Root-cause category, product and complaint category are closed
enumerations in configuration, not free text.

Outcomes: Upheld, Partially upheld, Not upheld. Redress is recorded, including zero, and is not
paid by the application.

`Investigation.completed_at` is set on submission and cleared on return or invalidation. Whether a
return should restart a statutory clock is an open interpretation recorded in Appendix B.

On submission the system stores an immutable snapshot of the reviewed package — the investigation
fields for that revision plus the exact final-response recipient type, recipient, subject and body
— with a hash. The revision increments on return, and the Approval stores the revision at
submission.

### Return and resubmission

A return must state a reason in the decision comment and may include recommendations or change
requests. The comment is mandatory on return and optional on approval.

The handler may edit and resubmit, optionally recording in the submission note what changed and any
disagreement with the recommendations. The note informs the next decision but never defers it.

A return applies to that revision only. Any compliance user may decide a resubmission, including
the reviewer who returned it; reviewer-shopping is recorded as a limitation. The approver's
decision is final: no appeal, no override, no conditional approval, and no closure without a valid
approval.

Each round creates a new Approval row, so comments, recommendations, submission notes and decisions
form a history. Itemised change requests with per-item responses are optional.

Approval validity is checked when the decision is made and again inside the send and close
transactions. A revision check rejects a stale submission.

## 12. Logical data model

| Entity | Purpose |
|---|---|
| User | Identity, single role, activation |
| Complainant | Contact details, separate from narrative |
| Complaint | Receipt, handler, classification, lifecycle |
| Investigation | Findings, root cause, outcome, redress, revision, completion |
| Approval | Snapshot, revision, decision, recommendations, submission note |
| Correspondence | Outbound content, type, recipient type, approval link, milestones, status |
| SendAttempt | Attempt result, provider reference, error, uncertainty resolution |
| Milestone | Obligation, sequence, due date, completion, supersession, waiver |
| ScheduledRun | Job name, period key, status, timestamps, error |
| AuditEvent | Actor, time, action, change details |
| PublicHoliday | Date, name, calendar |

This is a logical model, not a table-count target. Separating complainant details supports
permission design but is not anonymisation; message bodies and findings also contain personal data.

A case-note entity and an investigation-revision table are deferred; the approval snapshot holds
the evidence a revision table would otherwise provide.

## 13. Logical screens

Dashboard: counts of open cases, acknowledgements due, updates due, day-40 cases, responses due,
pending approvals and failed or uncertain sends, with urgent items first.

Complaint list: reference, state, handler, received date, next milestone and next action, with
filters for state, handler, date range, category and overdue status, and a CSV export control
applying the same filters and permissions.

The export contains reference, state, handler, received date, milestone dates, outcome and closure
date. It excludes narrative and personal contact details, and every export is audited.

Intake: required fields, explicit receipt date, contact validation, self-assigned handler, and the
calculated milestones shown after saving.

Complaint detail: header with reference, state, handler and milestone panel; sections for summary,
investigation, outcome and approval, correspondence, audit history. Role-appropriate actions are
shown and independently enforced.

Correspondence composer: type, recipient type, template, required fields, preview, allowlisted
recipient, approval status, confirmation, clear send outcome.

Approval queue: pending packages with age, read-only snapshot, prior comments and submission notes,
approve or return with mandatory comment on return.

Receipt correction: reviewer-only form showing the current date, the new date, a required reason,
and the milestone changes the correction will cause before confirmation.

No configuration screens exist in the minimum release.

### Responsive behaviour

The interface is one responsive website using a CSS framework, with the main journey checked once at
375 CSS pixels. Any layout or accessibility failure found is recorded in the accessibility review
rather than being described as resolved.

## 14. Automations

The three automations below are the ones demonstrated with a screenshot and a successful test run.

| Type | Behaviour | Evidence |
|---|---|---|
| Scheduled | Daily deadline check, stuck-send check and staff digest to one allowlisted recipient | Screenshot of the run, the ScheduledRun row, and the received digest |
| Event-triggered | `POST /complaints` creates the milestones and an acknowledgement draft; a completed message completes its milestone; submission opens an approval | Screenshot of the case after intake and the milestone panel |
| Human approval | Submission enters the reviewer queue and blocks release until decided | Screenshot of the queue, decision and resulting audit entries |

Nothing substantive to a complainant is sent because a timer fired; monitoring prompts a human to
act. Each scheduled run records job name and period key, so a rerun cannot duplicate a digest for
the same period. Failures and the last successful run are recorded.

## 15. Security, privacy and operations

- Authentication with password hashing, CSRF protection, secure cookie and session settings, idle
  expiry, and server-side validation. Login throttling is optional.
- Authorisation in services and scoped queries, tested against direct requests.
- One authoritative audit event list: case creation, state transitions, approvals, returns,
  invalidations, receipt corrections, milestone waivers, correspondence attempts, uncertainty
  resolutions, denials, exports and CLI provisioning.
- UPDATE and DELETE on the audit table revoked for the application role in PostgreSQL, with a test
  proving the revocation.
- Operational logs separate from audit evidence, without secrets or narrative.
- Synthetic data only, with production legal basis described separately.
- Data protection: lawful basis described for production use; minimisation by excluding narrative
  from exports and staff digests; retention proposed as six years from closure, labelled unverified;
  personal data visible to handlers for assigned cases and to compliance reviewers for all cases,
  with no access for any other role.
- Data-subject access, correction and erasure handling is a documented paragraph in the GDPR
  write-up, with no automated request handling.
- Retention is a documented policy only; no deletion feature exists, and that is stated as a
  limitation.
- Backup and restore, access review, incident response, change control and ownership in the
  governance policy, including an incident walk-through of what the audit trail and monitoring would
  show, the licence position of generated code, and the IP position.
- Monitoring of health, errors, scheduled-run failures and send failures.
- Accessible labels, keyboard navigation, visible focus, contrast, clear errors and non-colour status
  indicators, with real failures reported honestly.
- Persistent storage and a documented recovery route.

## 16. Success criteria and release priorities

### 16.1 Minimum release — fifteen committed criteria

1. **Complete journey.** Using separate handler and compliance accounts, complete intake →
   investigation → submission → independent approval → final-response sending → closure, with
   every closure gate enforced and each unmet gate named in the refusal.
2. **Receipt capture and correction.** Record the actual receipt date and channel separately from
   creation time, reject future dates, keep the date read-only to ordinary editing, and support a
   reviewer-only correction that requires a reason, audits old and new values, supersedes prior
   milestones and recalculates deadlines.
3. **Investigation validation and approval loop.** Reject submission while findings, category,
   outcome, rationale or redress are missing; require a comment on return, allow optional
   recommendations and a submission note, freeze content on approval, and require invalidation
   before any change.
4. **Closure evidence.** Refuse closure without valid approval, provider acceptance, recorded
   findings and the day-40 position; waive remaining milestones with an audited reason.
5. **Deadlines.** Pass independently checked examples covering weekends, the October public holiday,
   Good Friday and a year boundary; retain completed milestone dates; support at least two progress
   updates after the day-40 notification without resetting the target; pass the day-40 boundary test.
6. **Correspondence.** Send all four types with recipient type and version-controlled templates;
   enforce the allowlist in the service; persist before sending; distinguish acceptance, failure and
   unknown acceptance; retry definite failures only; require recorded resolution of unknown
   acceptance.
7. **Three automations with evidence.** A scheduled check with an idempotent digest, an
   event-triggered intake, and a human approval step, each evidenced by a screenshot and a successful
   test run.
8. **Role-based access enforced on the data.** Two roles with permissions enforced in services and
   scoped queries, not only by hiding buttons or screens, proven by tests that a direct request from
   the wrong user fails and that self-approval is impossible.
9. **Role table.** A table of roles stating what each can create, read, update and delete for every
   entity, with the enforcement point named.
10. **Data model.** At least three related tables, each with a primary key and the foreign keys that
    link them, delivered as an entity relationship diagram generated from the implemented models.
11. **Audit trail.** Record the listed events, keep entries immutable through the application, and
    prove the database privilege revocation.
12. **Level-1 data flow diagram.** Show every external entity, process, datastore and trust boundary
    in the implemented system.
13. **Threat analysis.** Apply STRIDE to every flow that crosses a trust boundary, with a mitigation
    recorded for each threat and automated tests tagged by threat identifier.
14. **Data protection write-up.** State the lawful basis, the minimisation measures, the retention
    period and who can see personal data.
15. **Delivery and evidence pack.** Docker and PostgreSQL deployment from a clean checkout, the test
    suite passing against PostgreSQL, one or two scanners with each finding's response recorded, the
    demonstration video, lecturer test accounts, and the Moodle submission package including the
    single write-up, cover page and AI declaration.

### Brief minimum coverage

| Brief requirement | Criterion |
|---|---|
| Data model with at least three related tables and an ERD | 10 |
| Three automations, screenshots and successful test runs | 7 |
| Two roles enforced on the data, with a role table | 8, 9 |
| Level-1 DFD with all elements and trust boundaries | 12 |
| STRIDE on every boundary-crossing flow with mitigations | 13 |
| Lawful basis, minimisation, retention, visibility | 14 |
| Evidence to submit | 11, 15 |

### 16.2 Optional enhancements

Itemised change requests, handler reassignment, browser-based administration, case notes,
attachments, delivery webhooks, background queue, advanced reporting, editable templates, login
throttling, password reset and change screens, multi-factor authentication, browser test automation,
and an expedited early-resolution path.

Optional status removes no security requirement. Anything implemented carries its permissions,
validation, audit and tests.

### 16.3 Implementation choices

- Users are created and deactivated by CLI, which refuses to remove the last active compliance
  reviewer or deactivate a handler with open cases.
- The holiday calendar is a version-controlled dataset including Good Friday, covering the test period
  and the following year.
- Templates are files in version control.
- One email provider is called inline; no queue or worker.
- No reassignment or administrative routes exist.

### 16.4 Checkpoints

- End of course week 9: criteria 1–6 demonstrable end to end; Section 1 register complete for every
  rule that drives code; real sending proven or the sandbox fallback adopted.
- End of course week 10: feature freeze. Only defects, evidence and documentation thereafter.
- Course week 11: testing, scanning, accessibility review, DFD and STRIDE evidence, write-up and
  package complete for submission.
- Course week 12: demonstration.

Anything unfinished at the freeze becomes a disclosed limitation, not a reason to extend the build.
Confirm the actual dates and the late-submission penalty against the timetable.

## 17. Tests

Tests are organised by STRIDE threat identifier where they mitigate a threat, so the suite doubles as
evidence that mitigations exist in code.

- Unit: working-day arithmetic including Good Friday and public holidays; milestone generation and
  regeneration; receipt-correction recalculation; state transitions; approval invalidation; stale
  revision rejection.
- Integration: persistence, permissions, transactional approve and close, correspondence logging,
  approval snapshot retention, export scoping.
- Approval loop: return without comment rejected; resubmission creating a new revision; approver
  decision final; closure refused with an invalidated approval.
- Closure: one negative test per unmet gate; return-to-investigation blocked after provider
  acceptance; milestones waived on closure; the day-40 boundary in both directions.
- Negative: self-approval, cross-handler access, non-allowlisted recipient, editing a frozen message,
  editing under live approval.
- Correspondence: success, definite failure, unknown acceptance and its recorded resolution, retry
  without duplication, stale sending flagged by the scheduled check.
- Scheduling: idempotent digest for a repeated period key; recorded failure.
- Audit and templates: audit-table privilege revocation; referral-rights content present in the
  unresolved and final-response templates.
- PostgreSQL: full suite against the deployment database before submission.
- Security: one or two scanners appropriate to source, dependencies, container and deployed
  application, with triage and remediation or acceptance recorded.
- Accessibility: automated checks plus manual keyboard review.

## 18. Repository and assessment deliverables

- Source with meaningful incremental history and AI-generated code flagged.
- Migrations and synthetic seed data.
- Working Dockerfile and deployment documentation.
- Example environment file with placeholders only.
- Automated tests and documented commands.
- Security-scan output and remediation evidence.
- Deployed application with role-specific accounts supplied to the lecturer.
- Entity relationship diagram and numbered level-1 data flow diagram with trust boundaries.
- STRIDE threat table covering every boundary-crossing flow, with mitigations.
- Role and CRUD permissions table.
- GDPR write-up covering lawful basis, minimisation, retention and visibility.
- Governance policy, operational runbook and incident walk-through.
- Approximately 2,500-word technical write-up with Harvard references and cover page.
- Demonstration video, and live demonstration in week 12.
- AI-usage log and AI Fluency declaration appendix.
- Decision log including the hindsight question.

The assessment prohibits AI authorship of the design-decision analysis, security findings discussion,
accessibility review and limitations section. Those remain the student's own work.

## 19. Delivery approach

Following the CA2 session sequence:

1. Commit this baseline, the decision log and the rule register.
2. Repository, Flask skeleton, PostgreSQL in Docker Compose, authentication, container build.
3. Prove real sending to one allowlisted address, or adopt the sandbox fallback and disclose it.
4. Deadline engine with the Appendix B fixtures and worked examples.
5. Case journey: intake, investigation, approval with snapshot, correspondence, closure gates, audit.
6. Role and permission tests written alongside, not after.
7. Testing, scanning, accessibility review, DFD and STRIDE evidence.
8. Governance documents, demo video, then the written report.
9. Live demonstration.

Submission is at the end of course week 11, with the demonstration in week 12 and a late penalty
stated in the timetable. Confirm both before planning further.

Available hours remain unconfirmed; plan conservatively around work and family commitments and
re-estimate after the first slice.

## 20. Open decisions

- Verified interpretation of the day-of-receipt convention and the return-clock question.
- Retention period confirmation.
- Hosting provider.
- Email provider, test recipient and the uncertainty age threshold.
- CSS framework and visual design.
- Any lecturer requirement for a specific development database.
- Confirmed timetable and sustainable weekly effort.

## 21. Reference and evidence register

Primary coursework source: MCLCD_Oct26_CA2_LowCodeNoCodeAIDev.docx, read 9 November 2026, confirmed
applicable to this deliverable and to the low-code comparison in Section 4.

Additional source: Low-Code-No-Code-Project-Brief.pdf, confirmed applicable as the source of the
seven minimum requirements mapped in Section 16.1.

Regulatory sources, verified: see Appendix B. The single instrument is S.I. No. 81 of 2025. The
June 2025 insurance newsletter located during verification predates the 2025 Code and uses
superseded "business day" wording; it is retained only as history.

## 22. Revision history

| Version | Change |
|---|---|
| 0.2 | Initial product definition and specification. |
| 0.3 | Minimum release introduced; committed and optional scope separated. |
| 0.4 | Contradictions resolved: no post-approval editing, approval snapshots, milestone records, acceptance uncertainty, permission matrix, scheduled runs, single scope table, single test list. |
| 0.5 | Approval confined to the final response; approve-return-resubmit loop; receipt correction and CSV export promoted; PostgreSQL only; modular architecture and guardrail; baseline authentication hardening; milestone supersession; recipient types. |
| 0.6 | Criteria reduced from 27 to 15 and mapped to brief minima; regulatory provisions verified in Appendix B; stakeholder and platform-comparison sections added; architecture reduced to three rules; enumerations as validated text; CRUD permission table; milestone waiver; course-week checkpoints and feature freeze; STRIDE-tagged tests. |

Superseded statements, retained only as record:

- An earlier draft implied a late-Friday cut-off; no such rule is modelled.
- An earlier draft treated 8 January as a submission date; the timetable governs.
- An earlier draft described features as belonging to "the original concept"; Section 3 governs.
- An earlier draft used a precedence rule letting Section 16 override other sections; contradictions
  were resolved instead.
- Earlier drafts used "MVP", "minimum assessed release" and "minimum implementation"; this document
  uses "minimum release".
- Earlier drafts required independent approval of every message; from 0.5 it applies to the final
  response only.

---

# Appendix A — Specification

## Purpose

An internal complaints-management application for handlers and compliance reviewers in a small
Irish insurance intermediary. It replaces spreadsheets and disconnected email with deadline
tracking, independent approval of the final response, logged correspondence and an auditable
history.

## Entities

### User
- id (integer, primary key)
- name (text, required)
- email (text, required, unique)
- password_hash (text, required)
- role (text, required; validated against: handler, compliance)
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
- received_channel (text, required; validated against: email, phone, letter, in_person, other)
- receipt_note (text, required)
- product (text, required; validated enumeration)
- category (text, required; validated enumeration)
- description (text, required)
- status (text, required; validated against: logged, investigating, pending_approval, approved,
  closed)
- closed_at (timestamp, optional)
- created_at (timestamp)
- updated_at (timestamp)

Due dates derive from Milestone records.

### Investigation
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required, unique)
- findings (text, optional while drafting)
- root_cause_category (text, optional while drafting; validated enumeration)
- outcome (text, optional while drafting; validated against: upheld, partially_upheld, not_upheld)
- outcome_rationale (text, optional while drafting)
- redress_amount (decimal, non-negative, default 0)
- revision (integer, default 1; incremented on return)
- completed_at (timestamp, optional; set on submission, cleared on return or invalidation)
- updated_at (timestamp)

### Approval
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- investigation_revision (integer, required)
- final_response_id (foreign key to Correspondence, required)
- reviewer_id (foreign key to User, nullable until a decision; must hold the compliance role and
  differ from the handler)
- decision (text, required; validated against: pending, approved, returned; default pending)
- comment (text, required on return, optional on approval)
- recommendations (text, optional)
- submission_note (text, optional)
- package_snapshot (structured data, required; immutable copy of the reviewed investigation fields
  and final-response recipient type, recipient, subject and body)
- content_hash (text, required)
- submitted_at (timestamp, required)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)

### Correspondence
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- approval_id (foreign key to Approval, optional)
- milestone_id (foreign key to Milestone, optional)
- message_type (text, required; validated against: acknowledgement, progress_update,
  unresolved_notification, final_response)
- recipient_type (text, required; validated against: complainant, provider, internal)
- recipient_email (text, required before sending)
- subject (text, required before sending)
- body (text, required before sending)
- template_version (text, required)
- status (text, required; validated against: draft, sending, provider_accepted, failed,
  acceptance_unknown)
- authorised_by_id (foreign key to User, optional until confirmed or approved)
- authorised_at (timestamp, optional)
- provider_accepted_at (timestamp, optional)
- attempt_count (integer, default 0)
- last_attempted_at (timestamp, optional)
- provider_reference (text, optional)
- last_error (text, optional)
- created_at (timestamp)
- Editable only while draft and not referenced by a pending or approved, non-invalidated Approval.

### SendAttempt
- id (integer, primary key)
- correspondence_id (foreign key to Correspondence, required)
- attempted_at (timestamp, required)
- result (text, required; validated against: provider_accepted, failed, acceptance_unknown)
- provider_reference (text, optional)
- error_code (text, optional)
- error_summary (text, optional; excludes secrets)
- resolved_by_id (foreign key to User, optional)
- resolved_at (timestamp, optional)
- resolution (text, optional; validated against: confirmed_accepted, resend_authorised)
- resolution_note (text, optional)

### Milestone
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- type (text, required; validated against: acknowledgement, progress_update,
  unresolved_notification, final_response)
- sequence (integer, required)
- due_date (date, required)
- completed_correspondence_id (foreign key to Correspondence, optional)
- completed_at (timestamp, optional)
- superseded_at (timestamp, optional; set only by receipt correction)
- waived_at (timestamp, optional; set only at closure)
- waived_reason (text, optional)
- created_at (timestamp)
- Unique on (complaint_id, type, sequence).

### ScheduledRun
- id (integer, primary key)
- job_name (text, required)
- period_key (text, required)
- status (text, required; validated against: started, succeeded, failed)
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
| POST | /login | Authenticate and start session |
| POST | /logout | End session |
| GET | / | Dashboard with counts, milestones and urgent actions |
| GET | /complaints | List and filter authorised complaints |
| GET | /complaints/export | CSV export of the filtered, authorised register |
| GET | /complaints/new | Show intake form |
| POST | /complaints | Create complaint, generate milestones, create acknowledgement draft |
| GET | /complaints/<id> | Show case, milestones, correspondence and audit |
| POST | /complaints/<id>/investigation | Save investigation draft; first save begins investigating |
| POST | /complaints/<id>/receipt-correction | Reviewer correction with reason and recalculation |
| POST | /complaints/<id>/correspondence | Create a controlled draft |
| POST | /correspondence/<id>/edit | Edit a draft not under live approval |
| GET | /correspondence/<id>/preview | Preview recipient, subject, body and approval status |
| POST | /correspondence/<id>/send | Verify authorisation or approval, persist, then send |
| POST | /correspondence/<id>/retry | Retry a definite failure with unchanged content |
| POST | /correspondence/<id>/resolve-uncertainty | Record acceptance evidence or authorise resend |
| POST | /complaints/<id>/submit-outcome | Snapshot the package and open approval |
| GET | /approvals | Review queue with ages and prior rounds |
| POST | /approvals/<id>/decision | Approve or return the snapshotted package |
| POST | /complaints/<id>/return-to-investigation | Invalidate approval; refused after provider acceptance |
| POST | /complaints/<id>/close | Enforce every closure gate in Section 8, waive open milestones, close |
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
| POST | /account/password | Change own password |
| POST | /account/reset | Password reset by email |

## Technical constraints

- Python and Flask with versions pinned; PostgreSQL for development, testing and deployment through
  Docker Compose.
- Flask-SQLAlchemy and Alembic; every schema change via migration.
- Application factory; routes delegate to services; deadline rules are pure functions; one
  configuration module for enumerations and tunables.
- Enumerations are validated text columns, not database enum types.
- Jinja templates; no separate JavaScript frontend framework.
- One responsive CSS framework; main journey checked at 375 CSS pixels with failures reported.
- No abstraction before two call sites; no plugin, DI container, workflow engine or event bus.
- Authentication, password hashing, CSRF, secure cookies, idle session expiry and server-side
  validation.
- Permissions enforced in services and scoped queries, proven by direct-request tests.
- Handlers reach assigned cases only; reviewers reach all cases but never decide a case they
  handled.
- No route changes roles; provisioning and deactivation are CLI operations that refuse to remove the
  last compliance reviewer or deactivate a handler with open cases.
- Receipt dates change only through the audited correction action, which supersedes and recalculates
  milestones.
- Correspondence editable only in draft and outside a live approval; frozen on authorisation.
- Approval applies to the final response only; the other three types are handler-confirmed.
- Comment mandatory on return, optional on approval; approver decisions are final, with no appeal,
  override or conditional approval.
- Approved content never edited; change requires invalidation and resubmission.
- Return-to-investigation refused after the final response is provider-accepted.
- Closure requires every gate in Section 8; open milestones are waived with an audited reason.
- Provider acceptance is never described as delivery.
- All four message types are sent through the app with a recipient type and logged automatically.
- Mandatory template content per Appendix B, including ombudsman referral rights and contact
  details.
- Progress updates repeat before and after the 40-working-day point and never reset the receipt date
  or resolution target.
- Milestones are stored per obligation; current deadlines derive from open, non-superseded
  milestones.
- Deadline calculation uses the Appendix B conventions, including the Good Friday exclusion.
- Countdowns show label, exact date and text urgency.
- Outbound content persisted before any send attempt; attempts recorded individually.
- Real sending restricted server-side to allowlisted addresses; no unrestricted CC or BCC.
- Failed and uncertain sends remain visible and never complete milestones.
- Unknown acceptance requires recorded, audited resolution before any replacement send; the
  scheduled check flags stale sending records.
- Scheduled runs are idempotent per job and period and record failures.
- CSV export respects record permissions, excludes narrative and contact detail, and is audited.
- Synthetic data only; credentials from environment configuration, never in Git or AI tools.
- Scheduled work runs through a documented CLI command, not a web route.
- Audit table protected by revoked UPDATE and DELETE for the application role.
- Retention is a documented policy only; no deletion feature is implemented.
- Dockerfile, deployment documentation, tests, scan evidence, ERD, DFD, STRIDE table, role table,
  GDPR write-up, demo video and Git history are required deliverables.

## Out of scope

Excluded capabilities are listed in the single scope table in Section 3. Items marked Optional are
deferred, not excluded; items marked Out of scope are not delivered in this release.

---

# Appendix B — Regulatory requirements register

This appendix is the completion of Section 5 for every rule that drives code. Rows marked
"open" must be settled before the related logic is merged.

## B.1 Instrument and status

| Item | Detail |
|---|---|
| Instrument | Central Bank (Supervision and Enforcement) Act 2013 (Section 48) (Consumer Protection) Regulations 2025 |
| Citation | S.I. No. 81 of 2025 |
| Made | 24 March 2025 |
| Commencement | 24 March 2026 |
| Complaints chapter | Chapter 12 of Part 2 |
| Key provisions | Regulation 105 (procedure), Regulation 106 (complaint log), Regulation 107 (analysis) |

The "General Consumer Protection Requirements" is Part 2 of the same instrument, not a separate
one. It is the only deadline source for this project.

## B.2 Definition of working day

A working day is a day that is not a Saturday, a Sunday, Good Friday, or a public holiday within
the meaning of the Organisation of Working Time Act 1997.

Consequences:

- Good Friday is excluded explicitly and must be seeded deliberately; bank-holiday lists usually
  omit it.
- The public holiday set follows the 1997 Act, so the dataset must be dated and versioned.
- Weekends are excluded by definition, so no "if Saturday, roll to Monday" logic may exist.

### Worked examples

| Scenario                                                                           | Calculation                                                                      | Due                    |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------- |
| Received Thursday 22 October 2026; Monday 26 October is the October public holiday | Fri 23 = 1; Mon 26 excluded; Tue 27 = 2; Wed 28 = 3; Thu 29 = 4; Fri 30 = 5      | Friday 30 October 2026 |
| Received Wednesday 24 March 2027; Good Friday 26 March 2027                        | Thu 25 = 1; Fri 26 excluded; Mon 29 = 2; Tue 30 = 3; Wed 31 = 4; Thu 1 April = 5 | Thursday 1 April 2027  |

**Open:** whether the day of receipt counts as the first working day. Adopted convention for the
build: the clock starts on the next working day after receipt, matching both examples above. The
alternative must be acknowledged in the write-up.

## B.3 Obligations

| Obligation | Provision | Requirement | Implementation |
|---|---|---|---|
| Written procedure | Reg 105(1) | Procedure for managing and resolving complaints | Governance policy; not a system feature |
| Acknowledgement | Reg 105(4) | Written acknowledgement within 5 working days with procedure details, ombudsman information and contact details | Acknowledgement draft at intake; 5-working-day milestone; handler-confirmed |
| Named contact | Reg 105(4) | Point of contact until resolved or all steps exhausted | Handler recorded on acknowledgement and case |
| Progress updates | Reg 105(4)(d) | Regular written updates at intervals no greater than 20 working days from the date of receipt | Progress-update milestones at receipt + 20, +40, +60 working days |
| Reasonable efforts | Reg 105(4) | Investigate and make reasonable efforts to resolve within 40 working days | 40-working-day target; breach shown as overdue |
| Unresolved at 40 days | Reg 105(4) | Notify anticipated timeframe, referral right and ombudsman contact details | Unresolved-notification milestone with mandatory template fields |
| Final response | Reg 105(4) | Within 5 working days of completion of the investigation: decision and reasons, offer or settlement terms, referral right and contact details | Final-response milestone from `completed_at`; recalculated on resubmission |
| Early resolution | Reg 105(3) | Procedure need not apply where resolved to satisfaction within 5 working days, provided a record is kept | Normal journey retained; log entry mandatory |

**Open:** whether a return restarts the final-response clock. Adopted convention: a return clears
`completed_at` and restarts the clock on resubmission. This is a chosen interpretation and must be
disclosed.

## B.4 Mandatory template content

| Template | Mandatory content |
|---|---|
| Acknowledgement | Reference and date received; complaint as understood; procedure and expected timeframe; named contact; referral right and contact details |
| Progress update | Reference; what has been done; what remains; next expected update; named contact |
| Unresolved notification | Reference; not yet resolved; anticipated timeframe; referral right and contact details |
| Final response | Reference; decision and reasons; offer, redress or settlement terms; referral right and contact details; referral time limit where applicable |

The ombudsman is the Financial Services and Pensions Ombudsman. Contact details are stored with the
template version so later changes do not retrospectively alter what was sent.

## B.5 Complaint log

Regulation 106 requires a complaint log. Mapping to the data model:

| Log field | Held in |
|---|---|
| Core reason or category | `Complaint.category`, `Investigation.root_cause_category` |
| Date received | `Complaint.received_date`, with correction history in `AuditEvent` |
| Summary of response and date | Final-response `Correspondence`, `Investigation.outcome_rationale` |
| Other correspondence | All `Correspondence` rows with recipient type and timestamps |
| Steps taken | Investigation findings and the milestone sequence |
| Resolution date | Closure timestamp |
| Ombudsman referral or appeal status | Not modelled; disclosed limitation |

## B.6 Analysis obligation

Regulation 107 requires periodic analysis of complaints, at least every six months. Out of scope for
the prototype; disclosed in the limitations section.

## B.7 Retention

Proposed retention period: **six years from closure**, aligned to the limitation period applicable
to contract and consumer claims. This position is **unverified** and must be confirmed against the
firm's record-keeping obligations before it is presented as a compliance position. No deletion
feature is implemented.

## B.8 Terminology

| Term | Status |
|---|---|
| "Business day" | 2012 Code and June 2025 newsletter wording; superseded |
| "Working day" | The 2025 term, with the Good Friday exclusion |
| "40 days" unqualified | Incorrect; the requirement is 40 working days |

The "no Central Bank notification after 40 working days" point in the 2025 Code overview concerns
errors, not complaints, and must not be applied to this workflow.

## B.9 Sources

- Central Bank (Supervision and Enforcement) Act 2013 (Section 48) (Consumer Protection) Regulations
  2025, S.I. No. 81 of 2025 — https://www.irishstatutebook.ie/eli/2025/si/81/made/en/print
- Consumer Protection Code 2025, Part 1: Preliminary and General —
  https://www.centralbank.ie/regulation/consumer-protection/consumer-protection-code/section-48-regulations/part-1-preliminary-and-general
- Consumer Protection Code 2025, Part 2: General Consumer Protection Requirements —
  https://www.centralbank.ie/regulation/consumer-protection/consumer-protection-code/section-48-regulations/part-2-general-consumer-protection-requirements
- Central Bank redline of the section 48 provisions, paragraph-lettered version —
  https://edit.centralbank.ie/docs/default-source/regulation/consumer-protection/other-codes-of-conduct/consumer-protection-code-review/redline---(section-48)-(consumer-protection)-regulations-2025---23-march-2025.pdf
- Financial Services and Pensions Ombudsman, complaint process guidance for consumers —
  https://fspo.ie/make-a-complaint/how-to-make-a-complaint-to-your-provider/financial-services-provider/default.asp

This appendix records requirements for a coursework prototype. It is not legal advice and does not
certify compliance.