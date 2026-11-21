
# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.7.1 — 10 November 2026
Status: Minimum release baselined for implementation. Regulatory provisions verified at
Appendix B; two timing conventions adopted but unverified; remaining open items recorded
there.

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
  permission model, and the same operator runs the reassignment command in Section 6.
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

**No stakeholder validation has occurred.** No handler, reviewer or owner has reviewed this
design, and no legal review has taken place. The workflow has been checked against the
provisions in Appendix B; that is desk research against published sources, not validation with
users. The write-up must not imply otherwise.

> **Placeholder — handler review, to be inserted once obtained.**
> To complete: date of the review; participant role and firm size; what was shown; what the
> participant confirmed; what the participant disputed; the changes made as a result.
> If no review takes place before submission, replace this placeholder with one sentence
> stating that no review took place. Do not complete it by assumption.

## 3. Scope boundary

| Capability | Status |
|---|---|
| Intake with actual receipt date and channel | Committed |
| Authorised receipt correction with preview, reason and recalculation | Committed |
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
| Responsive main journey, checked at 375 CSS pixels | Committed |
| Accessibility review, with failures reported rather than described as resolved | Committed |
| Docker deployment on PostgreSQL | Committed |
| Entity relationship diagram | Committed |
| Level-1 data flow diagram with trust boundaries | Committed |
| STRIDE threat table covering every boundary-crossing flow | Committed |
| Role and CRUD permissions table, route by route | Committed |
| GDPR write-up | Committed |
| Limitations register (factual list) | Committed |
| Operator-only CLI handler reassignment, outside the permission model | Committed |
| Hosting decision and pre-registered descope ladder in the baseline | Committed |
| Demonstration video and lecturer test accounts | Committed |
| Itemised change requests with per-item handler responses | Optional |
| Handler reassignment through the interface | Optional |
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
If the lecturer specifies a different development database, it is a local convenience only and the
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

The decisive factor is problem fit, not compliance with the brief. Working-day arithmetic over a
versioned public-holiday calendar is plain date logic, so a small pure-Python module expresses
and tests it exactly. Database-level audit protection needs direct control of PostgreSQL
privileges, because revoking UPDATE and DELETE from the application role is the control.
Approval snapshot hashing needs a hash computed in application code over the exact reviewed
content at the moment of submission. And the whole journey, from the allowlist to the closure
gates, has to be exercised by an automated suite against PostgreSQL. Tests, a Dockerfile and
security scanning are CA2 requirements; the migrations in this repository follow from owning the
schema, and neither source asks for them.

### Hosting decision

Recorded before the baseline is committed, because three baseline controls depend on it:

| Requirement | Why the baseline needs it | Consequence if unmet |
|---|---|---|
| Scheduled CLI job | The daily deadline check, stuck-send check and staff digest run as a CLI command, never as a web route | A host without scheduled one-off commands leaves the check dependent on a page request |
| Separate owner and application database roles | Audit revocation requires an application role that cannot UPDATE or DELETE `AuditEvent`; the owner role applies migrations | One shared credential would hold the privilege it must lack, and the revocation test would prove nothing |
| A chosen monitoring tool | Health, errors, scheduled-run failures and send failures must be visible in operations | Operational evidence reduces to log files read by hand |

The provider is selected against these three requirements, and the choice together with the
monitoring tool is entered in the decision log before the baseline commit. Section 20 keeps the
selection open until that entry exists.

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
built and are justified in the write-up and recorded in the decision log.

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

Verified; to be implemented:

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

Adopted, unverified, and recorded in Appendix B:

- Whether the day of receipt counts as the first working day. The build starts the clock on the
  next working day after receipt. That is a chosen convention, not a verified reading.
- Whether a return restarts the final-response clock. The build clears `completed_at` and
  restarts the clock on resubmission. That is a chosen convention, not a verified reading.

Still open, and recorded in Appendix B:

- The retention period, proposed as six years from closure and labelled unverified.
- Paragraph letters within Regulation 105(4) other than subparagraph (d).

Independent approval of the final response is a chosen internal control and must not be
described as a statutory requirement. Where the source is silent, the register records the gap
rather than an invented rule.

## 6. Roles, access and permissions

Two roles: handler and compliance. Each user holds exactly one role, which structurally prevents
self-approval. The same single-value model means a compliance officer cannot also handle cases,
and there is no reviewer cover when the only reviewer is absent; both are recorded in the
limitations register in Section 15.

| Route or action | Handler | Compliance reviewer | Service or system actor | Record scope and enforcement |
|---|---|---|---|---|
| `GET /login` | Anonymous | Anonymous | Session issuer | No case data |
| `POST /login` | Anonymous | Anonymous | Authentication service | Password hash check; CSRF |
| `POST /logout` | Yes | Yes | Session terminator | Own session only |
| `GET /` | Yes | Yes | Dashboard query service | Handler: assigned. Reviewer: all |
| `GET /complaints` | Yes | Yes | Scoped query | Handler: assigned. Reviewer: all |
| `GET /complaints/export` | Yes | Yes | Export service | Same filters and permissions as the list; audited |
| `GET /complaints/new` | Yes | No | Intake form renderer | No case record yet |
| `POST /complaints` | Yes | No | Complaint service: creates the complaint, the acknowledgement, first progress-update and unresolved-notification milestones, and the acknowledgement draft | Handler self-assigns |
| `GET /complaints/<id>` | Yes | Yes | Case query | Handler: assigned. Reviewer: all |
| `POST /complaints/<id>/investigation` | Yes | No | Investigation service | Assigned only |
| `GET /complaints/<id>/receipt-correction` | No | Yes | Correction preview service: every affected milestone, old due date against new | Any case |
| `POST /complaints/<id>/receipt-correction` | No | Yes | Correction service: supersedes, recreates, carries completion, creates the corrective update | Reason required; audited; refused on a closed case |
| `POST /complaints/<id>/correspondence` | Yes | No | Correspondence service | Assigned |
| `POST /correspondence/<id>/edit` | Yes | No | Correspondence service | Assigned; draft; no live approval |
| `GET /correspondence/<id>/preview` | Yes | Yes | Preview renderer | Same read scope as the case |
| `POST /correspondence/<id>/send` | Yes | Yes | Send service: authorises non-final types, checks approval for the final response, writes one attempt, completes the milestone on acceptance | Handler: assigned. Reviewer: any |
| `POST /correspondence/<id>/retry` | Yes | Yes | Send service: definite failures only, unchanged content, new attempt on the same record | Same scope as sending |
| `POST /correspondence/<id>/resolve-uncertainty` | Yes, non-final types only | Yes, any type | Resolution service: resolution note required; sets acceptance or authorises a resend | Handler: assigned. Reviewer: any |
| `POST /complaints/<id>/submit-outcome` | Yes | No | Submission service: snapshot, hash, Approval row, final-response milestone | Assigned |
| `GET /approvals` | No | Yes | Queue query: excludes invalidated and decided approvals | No handler access |
| `POST /approvals/<id>/decision` | No | Yes | Decision service: sets reviewer and decision time, freezes comment and submission note; a return also clears `completed_at` and supersedes the final-response milestone | Any case they did not handle |
| `POST /complaints/<id>/return-to-investigation` | Yes | Yes | Invalidation service | Assigned (handler); any (reviewer) |
| `POST /complaints/<id>/close` | Yes | Yes | Closure service: gates in order, breach recorded where needed, waivers, close | Assigned (handler); any (reviewer) |
| `GET /health` | No | No | System, for monitoring | No sensitive information |
| CLI: provision or deactivate a user | No | No | Operator with hosting or repository access | Outside the application permission model |
| CLI: reassign a case handler | No | No | Operator with hosting or repository access | Outside the permission model; audited; refused for a closed case |
| CLI: scheduled check | No | No | System, invoked by the operator | Writes `ScheduledRun` and the digest only |

No route writes a milestone. Milestone rows are written by the complaint, correction, submission,
send, resolution and invalidation services, in the transaction that causes them. Optional routes
carry no rows here because they are deferred to Section 16.2 and inherit the same pattern when
built.

The CLI reassignment command exists so that a departing handler does not strand live deadlines. It
runs outside the application permission model, holds repository and hosting credentials, and is
recorded as an `AuditEvent` naming the operator. It changes `Complaint.handler_id` only;
milestones belong to the complaint and are untouched. Reassignment through the interface remains
Optional.

### Data permissions

| Entity | Handler | Compliance | Writes performed by | Enforced where |
|---|---|---|---|
| Complaint | Create own; read assigned; update state fields on assigned; no delete | Create none; read all; update receipt date and closure; no delete | Query filter plus service check |
| Investigation | Read and update on assigned; no delete | Read all; no update; no delete | Query filter plus service check |
| Approval | Read on assigned; create submission; no delete | Read all; create decision; no delete | Service check plus data constraint |
| Correspondence | Create and update drafts on assigned; no delete | Read all; approve final responses; no delete | Correspondence, send and resolution services | Query filter plus service check |
| Milestone | Read on assigned | Read all | Services only; no route, no direct write | Derived from complaint scope |
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
- A receipt correction is refused on a closed case.
- `Approval.comment` and `Approval.submission_note` become write-once once `decided_at` is set.
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

The date is read-only to ordinary editing. A compliance reviewer may correct it. The screen is two
routes: `GET /complaints/<id>/receipt-correction` renders the current date, the proposed date, the
required reason, every milestone the correction would change with old due date against new,
whether a corrective progress update will be required, and the effect on the day-40 position,
before anything is written; `POST` applies it. Both are reviewer-only.

Applying a correction:

- Audits the previous and new values, with actor, time and reason.
- Marks each receipt-derived milestone superseded by setting `superseded_at`, rather than deleting
  it, so earlier due dates remain visible as evidence of what was monitored.
- Creates a replacement for each obligation at the recalculated due date, reusing the same type and
  sequence; superseded rows are retained and readable.
- Where the superseded milestone was already completed, the replacement carries over that
  completion: `completed_at` and `completed_correspondence_id` are copied, so a correctly sent
  acknowledgement does not reappear as overdue.
- Leaves the final-response milestone untouched, because it derives from
  `Investigation.completed_at` and not from the receipt date.
- Creates a corrective progress update where the acknowledgement has already been sent, because
  sent content is frozen and quotes the original receipt date. It is an ordinary progress update:
  same type, complainant recipient, template and sequence rules, new content stating the corrected
  date. It appears in the milestone panel and the dashboard like any other, and if it is still open
  with a passed due date at closure it is waived as `missed` under Section 8.
- Is refused on a closed case.

### Gate 4 after a correction

A correction can move the 40-working-day due date in either direction. The unresolved-notification
milestone is superseded and replaced like any other receipt-derived milestone, and the day-40
position is re-evaluated at closure against the replacement using the Section 8 rule. A corrected
date that moves the day-40 point into the future removes a breach the earlier date would have
recorded; one that moves it into the past records a breach if the final response was already
accepted after the corrected due date. The re-evaluation is audited with the correction.

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
4. The day-40 position is settled. Either the final response reached provider-accepted status on or
   before the 40-working-day due date, or the unresolved-at-40-days notification reached
   provider-accepted status before the final-response send was attempted.
5. Closure is recorded as an audited transition by a user permitted by Section 6.

Gate 4 refuses closure while the day-40 position is unresolved: while an unresolved-at-40-days
message for the case is authorised, sending, failed or `acceptance_unknown`. Where the final
response was accepted after the 40-working-day due date and no unresolved notification exists, the
missed notification is recorded as a **breach**, and the closure service resolves the case in this
fixed order inside one transaction. The order is the definition.

1. Gates 1, 2 and 3 are evaluated; any failure refuses closure and names the gate.
2. The day-40 position is read from current milestones; a message in flight refuses closure.
3. If the final response was accepted after the due date and no notification was ever accepted, the
   breach is written: the unresolved-notification milestone is waived with `waived_at` set and
   `waived_reason = missed`, and an audit entry names who recorded it.
4. Gate 4 is re-evaluated and now passes, because the position is recorded rather than unknown.
5. Remaining open milestones are waived with an enumerated reason.
6. The case is closed and the transition audited.

**Ordering rule.** On any case, an unresolved-at-40-days notification is created, confirmed and
accepted before the final response is sent. Once the final response has reached `sending`, the
composer no longer offers the unresolved type for that case, and the send service refuses a
`POST /correspondence/<id>/send` for an unresolved notification on a case whose final response has
been sent. A message is therefore never sent after the outcome it was meant to precede.

Any milestone still open at closure is waived with an audit entry recording who waived it and why.
`waived_reason` is enumerated, and the test is whether the obligation was ever owed:

- `not_applicable` where the obligation ceased to apply — the case was resolved, or the receipt date
  corrected, before the obligation's trigger point, so it was never owed — or where its due date had
  not passed at closure.
- `missed` where the obligation was owed and its due date passed without completion.

A case resolved on working day 30 and closed on day 50 therefore waives the day-40 notification as
`not_applicable`, because it was never owed; a case still unresolved past day 40 that sent nothing
waives it as `missed`. The enumeration stops a waiver disguising a missed deadline, and stops a
breach being manufactured against a case resolved in time.

The minimum release models no discretionary closure exception. A case requiring an alternative
handling path cannot be closed, which is a disclosed limitation.

### Early resolution

Where a complaint is resolved to the consumer's satisfaction within five working days of receipt,
the full procedure need not apply, but the complaint must still be logged. The prototype uses the
normal journey for such cases and records the receipt date, the outcome, the resolution date and the
correspondence actually sent. It does not model an expedited path and does not claim that this
record alone discharges the logging obligation; assessing that against Regulation 106 belongs in
the write-up.

## 9. Deadline engine and milestones

### Records

Each obligation is a stored milestone: complaint, type, sequence, due date, completion state,
completing correspondence, completion timestamp, `superseded_at`, `waived_at` and `waived_reason`.
Milestones are never overwritten. Current deadlines derive from open, non-superseded milestones.

`superseded_at` is set by receipt correction, by return and by approval invalidation — the three
events that replace an obligation rather than satisfy it.

Types: acknowledgement, progress update, unresolved notification, final response.

- Acknowledgement at receipt plus five working days: created when the complaint is created.
- First progress update at receipt plus twenty working days: created when the complaint is created.
- Unresolved notification at receipt plus forty working days: created when the complaint is created.
- Each later progress update is created when the previous progress-update milestone completes, or
  when its due date passes. Its due date is receipt plus twenty working days multiplied by its
  sequence, so a case that stays open carries updates at day 60, day 80, day 100 and beyond.
  Generation runs in the transaction that completes the previous update, and on any page render or
  scheduled check that finds a passed due date, so it does not depend on the scheduler having run.
- Final response at the completion timestamp plus five working days: created when the outcome is
  submitted for approval, not at intake. Nothing exists to calculate before
  `Investigation.completed_at` is set.
- On return or invalidation the final-response milestone is superseded and a replacement is created
  at the next submission from the new completion timestamp.

Receipt correction supersedes the acknowledgement, every progress update and the unresolved
notification, and recreates them from the corrected date. It never touches the final-response
milestone.

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
receipt date, the 40-working-day target and the final-response deadline unchanged. Completion has one rule: only a complainant-addressed message completes a milestone, recorded once
in `Milestone.completed_correspondence_id`. A provider-addressed progress update, an internal staff
notice and any other non-complainant recipient complete nothing, because the obligation is owed to
the complainant. Because a message has a single type, one message cannot be represented as
satisfying two obligations: there is nowhere to record the second relationship.

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
are out of scope. Inbound contacts are not summarised in the application; that is a disclosed limitation, recorded in
Appendix B.5 and in the limitations register.

### Approval and confirmation

Acknowledgement, progress update and unresolved notification require handler confirmation only. The
final response requires independent approval of the exact package, because it carries the outcome
and redress position.

For the three non-final types the confirmation act is the `POST /correspondence/<id>/send`
submission itself, carrying the confirmation control. There is no separate confirmation record: the
POST stamps `authorised_by_id` and `authorised_at` and writes the first attempt in the same
transaction.

### Templates

Fixed and version-controlled, with the version recorded on every message. A template is selected by
message type **and** recipient type, so the composer offers these combinations and no others:

| Type | Complainant | Provider or insurer | Internal |
|---|---|---|---|
| Acknowledgement | Yes | No | No |
| Progress update | Yes | Yes | Yes |
| Unresolved notification | Yes | No | No |
| Final response | Yes | No | No |

Mandatory content per type is defined in Appendix B and attaches to the complainant-addressed
template of each type. Provider and internal templates carry the reference, the request or notice,
the expected timeframe and the named contact, and no referral-rights block, because they are not
addressed to the complainant.

### Flow and authorisation

Prepare → preview → confirm or approve → persist → attempt send → record result.

Authorisation is the act that freezes content: handler confirmation for the three non-final types,
reviewer approval for the final response. The outbox record is written before the provider is called and holds recipient, recipient type,
subject, body, template version, authorising user, timestamps, status and the current-state send
fields. It holds no approval reference: approval linkage is read from `Approval.final_response_id`.

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

One confirmation produces exactly one attempt. Failed and uncertain messages stay visible and never
complete a milestone. Only a definite failure may be retried, with unchanged content, recorded as a
new attempt on the same authorised record. `acceptance_unknown` is never retried directly; it is
resolved first.

Unknown acceptance requires a recorded resolution with a mandatory `resolution_note` naming the
evidence checked or the reason for a replacement send:

- **Confirmed acceptance.** `confirmed_accepted` moves the status to `provider_accepted` and sets
  `provider_accepted_at` to the resolution time, not the original attempt time, because that
  attempt's outcome was never established. The milestone is completed at that point.
- **Resend authorised.** `resend_authorised` leaves the record where it is until the resend runs. A
  resend is a new attempt on the same correspondence record, not a new record: status returns to
  `sending`, `attempt_count` increments, a new `SendAttempt` row is written, content unchanged.

A compliance reviewer may resolve any type on any case. A handler may resolve a non-final type on an
assigned case, so a five-day acknowledgement cannot be blocked by an absent reviewer. The final
response stays reviewer-only.

The scheduled check flags any message left in `sending` beyond a configured age as
`acceptance_unknown` and never resends automatically.

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

`Investigation.completed_at` is set on submission and cleared on return or invalidation. Whether a return should restart a statutory clock is an adopted, unverified convention recorded in
Appendix B.

On submission the system stores an immutable snapshot of the reviewed package — the investigation
fields for that revision plus the exact final-response recipient type, recipient, subject and body
— with a hash. The revision increments on return, and the Approval stores the revision at submission. Submission
creates the final-response milestone and opens the approval.

### Return and resubmission

A return must state a reason in the decision comment and may include recommendations or change
requests. The comment is mandatory on return and optional on approval.

The handler may edit and resubmit, optionally recording in the submission note what changed and any
disagreement with the recommendations. The note informs the next decision but never defers it.

A return applies to that revision only. Any compliance user may decide a resubmission, including
the reviewer who returned it; reviewer-shopping is recorded as a limitation. The approver's
decision is final: no appeal, no override, no conditional approval, and no closure without a valid
approval.

A return clears `completed_at` and supersedes the final-response milestone, exactly as an
invalidation does; the replacement is created at resubmission. Superseded rows are retained, so the
history shows what was monitored at each round.

Each round creates a new Approval row, so comments, recommendations, submission notes and decisions
form a history. Once a decision is recorded, `comment` and `submission_note` on that row are
write-once: `decided_at` freezes them and no later edit is accepted, by any role. Itemised change requests with per-item responses are optional.

Approval validity is checked when the decision is made and again inside the send and close
transactions. A revision check rejects a stale submission. The reviewer queue lists only pending, non-invalidated
approvals, so an invalidated package leaves the queue; it remains readable on the case.



## 12. Logical data model

| Entity | Purpose |
|---|---|
| User | Identity, single role, activation |
| Complainant | Contact details, separate from narrative |
| Complaint | Receipt, handler, classification, lifecycle |
| Investigation | Findings, root cause, outcome, redress, revision, completion |
| Approval | Snapshot, revision, decision, recommendations, submission note, final-response link |
| Correspondence | Outbound content, type, recipient type, status, current send state |
| SendAttempt | Per-attempt result, error detail, uncertainty resolution |
| Milestone | Obligation, sequence, due date, completion, supersession, waiver |
| ScheduledRun | Job name, period key, status, timestamps, error |
| AuditEvent | Actor, time, action, change details |
| PublicHoliday | Date, name, calendar |

This is a logical model, not a table-count target. Separating complainant details supports
permission design but is not anonymisation; message bodies and findings also contain personal data.

Each linkage is stored once: approval to final response on `Approval.final_response_id`, and
milestone completion on `Milestone.completed_correspondence_id`. `Correspondence` stores no
milestone or approval reference.

A case-note entity and an investigation-revision table are deferred; the approval snapshot holds
the evidence a revision table would otherwise provide.

## 13. Logical screens

Dashboard: counts of open cases, acknowledgements due, updates due, day-40 cases, responses due,
pending approvals and failed or uncertain sends, with urgent items first.

Complaint list: reference, state, handler, received date, next milestone and next action, with
filters for state, handler, date range, category and overdue status, and a CSV export control
applying the same filters and permissions.

The export is one row per case, because milestone counts vary. Fixed columns carry the case identity
and classification: reference, state, handler, received date, received channel, product, category,
root-cause category, outcome, redress amount. Fixed milestone columns carry the acknowledgement and
the first two progress updates, due date and completion timestamp each, followed by counters for the
remainder: progress updates due, completed and overdue, and the latest update completion timestamp.
The day-40 position is carried by the unresolved-notification due and completion dates and a breach
indicator. The final-response due date and the final-response date taken from `provider_accepted_at`
follow, then the approval decision date and the closure date.

That shape reproduces the Regulation 106 log fields named in Appendix B.5: category and root-cause
category, date received, response and its date, other correspondence through the milestone and
update columns, steps taken through the state and progress columns, and resolution date through the
closure date. The response summary is not exported, because narrative is excluded; that gap is
stated in Appendix B.5. Every export is audited, and personal contact details are never included.

Intake: required fields, explicit receipt date, contact validation, self-assigned handler, and the
calculated milestones shown after saving.

Complaint detail: header with reference, state, handler and milestone panel; sections for summary,
investigation, outcome and approval, correspondence, audit history. Role-appropriate actions are
shown and independently enforced.

Correspondence composer: type, recipient type, template, required fields, preview, allowlisted
recipient, approval status, confirmation, clear send outcome.

Approval queue: pending, non-invalidated packages only, with age, read-only snapshot, prior comments
and submission notes, approve or return with mandatory comment on return.

Receipt correction: reviewer-only. The preview route shows the current date, the proposed date, a
required reason, every affected milestone with old and new due dates, whether a corrective progress
update will be required, and the effect on the day-40 position, before confirmation. The control is
absent on a closed case.

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
| Event-triggered | `POST /complaints` creates the acknowledgement, first progress-update and unresolved-notification milestones and an acknowledgement draft; the acceptance of a complainant-addressed message completes its milestone | Screenshot of the case after intake and the milestone panel |
| Human approval | Submission enters the reviewer queue and blocks release until decided | Screenshot of the queue, decision and resulting audit entries |

Nothing substantive to a complainant is sent because a timer fired; monitoring prompts a human to
act. Each scheduled run records job name and period key, so a rerun cannot duplicate a digest for
the same period. Failures and the last successful run are recorded.

### Failed runs

A failed period may be re-run, and the re-run recovers without duplicating anything:

- The unique constraint on `(job_name, period_key)` prevents a second row for the same period.
- A re-run of a failed period updates the existing row: `status` returns to started, `started_at`
  records the re-run time, and `finished_at` and `error_summary` are cleared.
- The row reaches succeeded or failed again with its own evidence.

The constraint blocks duplication; it does not block recovery. A succeeded period is not re-run.

## 15. Security, privacy and operations

- Authentication with password hashing, CSRF protection, secure cookie and session settings, idle
  expiry, and server-side validation. Login throttling is optional.
- Authorisation in services and scoped queries, tested against direct requests.
- One authoritative audit event list: case creation, state transitions, approvals, returns,
  invalidations, receipt corrections, milestone waivers, correspondence attempts, uncertainty resolutions, milestone waivers and breaches, denials, exports,
  CLI provisioning and CLI reassignment.
- UPDATE and DELETE on the audit table revoked for the application role in PostgreSQL, with a test
  proving the revocation.
- Operational logs separate from audit evidence, without secrets or narrative.
- Synthetic data only, with production legal basis described separately.
- Data protection: lawful basis described for production use; minimisation by excluding narrative
  from exports and staff digests; retention proposed as six years from closure, labelled unverified;
  personal data visible to handlers for assigned cases and to compliance reviewers for all cases,
  with no access for any other role.
- Disclosure to the insurer: where a complaint concerns a product the firm placed with an insurer,
  the case detail sent to that insurer is a disclosure of personal data to a named external entity,
  made because the investigation depends on it. The write-up states the recipient, what is
  disclosed, the basis relied on, and the fact that the insurer's own handling is outside this
  application's control. The insurer is a named external entity in the data flow diagram, and the
  flow to it carries STRIDE threats like any other boundary-crossing flow.
- Data-subject access, correction and erasure handling is a documented paragraph in the GDPR
  write-up, with no automated request handling.
- Retention is a documented policy only; no deletion feature exists, and that is stated as a
  limitation.
- Backup and restore, access review, incident response, change control and ownership in the
  governance policy, including an incident walk-through of what the audit trail and monitoring would
  show, the licence position of generated code, and the IP position.
- Monitoring of health, errors, scheduled-run failures and send failures, through the tool chosen
  in the hosting decision.
- Accessible labels, keyboard navigation, visible focus, contrast, clear errors and non-colour status
  indicators, with real failures reported honestly.
- Persistent storage and a documented recovery route.

### Limitations register

Factual items. Analysis of them belongs in the write-up and is the student's own work.

1. Reviewer-shopping is possible: any compliance user may decide a resubmission, including the
   reviewer who returned it.
2. Ombudsman referral or appeal status is not modelled.
3. Regulation 107 six-monthly analysis is out of scope.
4. Two timing conventions are adopted but unverified: the day of receipt, and whether a return
   restarts the final-response clock.
5. Inbound contacts are not captured or summarised; the application records outbound messages only.
6. Handler absence leaves no cover: cases belong to one handler.
7. There is no reviewer cover; the system refuses to remove the last active compliance reviewer.
8. Single-value roles mean a compliance officer cannot also handle cases, and a dual-role officer
   cannot be represented.
9. The retention period is unverified.
10. No password reset, no login throttling and no multi-factor authentication are implemented.
11. Immutable messages restrict erasure: sent content is frozen, hashed where snapshotted, and
    covered by audit protection.

### Write-up guidance

- The write-up argues that the application is the only data path: complaint data enters through
  intake and correspondence from the interface, and the only other route to the data is direct
  database access by a credential holder, which no role claims to prevent. Row-level security is
  named as the next step, because it is the mechanism that would constrain that remaining path.
- The GDPR paragraph states that correction and erasure of complaint data are manual operator
  actions, not application features, and that they conflict with three properties built into the
  design: immutable sent messages, content hashes over approved packages, and revoked UPDATE and
  DELETE on the audit table. It states the retention basis relied on, and that the period is
  unverified.

## 16. Success criteria and release priorities

### 16.1 Minimum release — fifteen committed criteria

1. **Complete journey.** Using separate handler and compliance accounts, complete intake →
   investigation → submission → independent approval → final-response sending → closure, with
   every closure gate enforced and each unmet gate named in the refusal; present one defended design
   recommendation at the demonstration.
2. **Receipt capture and correction.** Record the actual receipt date and channel separately from
   creation time, reject future dates, keep the date read-only to ordinary editing, and support a
   reviewer-only correction that requires a reason, audits old and new values, previews the affected milestones, requires a reason, audits old and new values, supersedes prior
   milestones, carries over a completed obligation's completion, creates the corrective progress
   update where the acknowledgement was already sent, and is refused on a closed case.
3. **Investigation validation and approval loop.** Reject submission while findings, category,
   outcome, rationale or redress are missing; require a comment on return, allow optional
   recommendations and a submission note, freeze content on approval, make the comment and submission note write-once after a decision, and
   require invalidation before any change.
4. **Closure evidence.** Refuse closure without valid approval, provider acceptance, recorded
   findings and a settled day-40 position; record a missed day-40 notification as a breach; never
   send an unresolved notification after the final response; waive remaining milestones with an
   enumerated, audited reason.
5. **Deadlines.** Pass independently checked examples covering weekends, the October public holiday, Good Friday, Easter Monday and a year boundary, with
   every seeded calendar year containing both Good Friday and Easter Monday; retain completed
   milestone dates; create later progress updates as earlier ones complete or fall due, so updates
   beyond day 80 exist; support at least two progress updates after the day-40 notification without resetting the target; pass the day-40 boundary test.
6. **Correspondence.** Send all four types with recipient type and version-controlled templates;
   enforce the allowlist in the service; persist before sending; produce exactly one attempt per
   confirmation; distinguish acceptance, failure and unknown acceptance; retry definite failures
   only; require a recorded resolution note for unknown acceptance; complete milestones only from
   complainant-addressed messages.
7. **Three automations with evidence.** A scheduled check with an idempotent digest, an
   event-triggered intake, and a human approval step, each evidenced by a screenshot and a successful
   test run.
8. **Role-based access enforced on the data.** Two roles with permissions enforced in services and
   scoped queries, not only by hiding buttons or screens, proven by tests that a direct request from the wrong user fails and that self-approval is
   impossible, and stated route by route with the service or system actor named.
9. **Role table.** A table of roles stating what each can create, read, update and delete for every
   entity, with the enforcement point named.
10. **Data model.** At least three related tables, each with a primary key and the foreign keys that
    link them, delivered as an entity relationship diagram generated from the implemented models.
11. **Audit trail.** Record the listed events, keep entries immutable through the application, and
    prove the database privilege revocation.
12. **Level-1 data flow diagram.** Show every external entity - including the email provider and the insurer - process, datastore and
    trust boundary in the implemented system.
13. **Threat analysis.** Apply STRIDE to every flow that crosses a trust boundary, including provider correspondence and
    the flow to the insurer, with a mitigation recorded for each threat and automated tests tagged by
    threat identifier only where the mitigation is code.
14. **Data protection and disclosed limitations.** State the lawful basis, the minimisation
    measures, the retention period and who can see personal data, and deliver the limitations
    register as a factual list.
15. **Delivery and evidence pack.** Docker and PostgreSQL deployment from a clean checkout, the test
    suite passing against PostgreSQL, one or two scanners with what each covers and what remains unscanned stated and each finding's
    response recorded, the demonstration video including the mistyped-receipt-date scenario, the
    accessibility review, the AI-usage log, lecturer test accounts, and the Moodle submission package including the
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

The brief sets six minimum requirements. Its separate evidence schedule is a submission list rather
than a seventh minimum and maps to criteria 11 and 15.

### 16.2 Optional enhancements

Itemised change requests, handler reassignment through the interface, browser-based administration, case notes,
attachments, delivery webhooks, background queue, advanced reporting, editable templates, login
throttling, password reset and change screens, multi-factor authentication, browser test automation,
and an expedited early-resolution path.

Optional status removes no security requirement. Anything implemented carries its permissions,
validation, audit and tests.

- Users are created, deactivated, and have cases reassigned, by CLI. The command refuses to remove
  the last active compliance reviewer or deactivate a handler with open cases. Reassignment runs
  outside the application permission model.
- The holiday calendar is a version-controlled dataset including Good Friday and Easter Monday,
  covering the test period and the following year; a test asserts that every seeded year contains
  both.
- Templates are files in version control, keyed by message type and recipient type.
- One email provider is called inline; no queue or worker.
- No reassignment or administrative routes exist; reassignment is the operator CLI command only.

- Baseline commit: hosting decision recorded; descope ladder pre-registered; DFD draft and STRIDE
  table with threat identifiers committed with the baseline; Section 5 and Appendix B complete for
  every rule that drives code.
- End of course week 9: criteria 1-6 demonstrable end to end; real sending proven or the sandbox
  fallback adopted; tests and the first scan run and recorded.
- End of course week 10: feature freeze. Tests, both scans and the suite against PostgreSQL are green
  before the freeze, not after it. Only defects, evidence and documentation thereafter.
- Course week 11: accessibility review, refreshed DFD and STRIDE evidence, write-up and package
  complete for submission.
- Course week 12: demonstration, including the defended recommendation.

Anything unfinished at the freeze becomes a disclosed limitation, not a reason to extend the build.
Confirm the actual dates and the late-submission penalty against the timetable.

### 16.5 Pre-registered descope ladder

If the schedule fails, scope is cut in this order, decided in advance so the decision is not taken
under pressure. Each rung is applied whole and recorded in the revision history and decision log:

1. **CSV export.** Removes the export route, template and tests; Section 3, Section 13, Appendix B.5
   and criterion 15 are updated to state that the log fields are readable on screen only.
2. **Provider recipients.** Removes the provider cells of the template matrix and the insurer flow
   from the data flow diagram and STRIDE table; provider correspondence reverts to the firm's email,
   disclosed as a limitation.
3. **Unknown-acceptance flow.** Removes the resolution route, the `acceptance_unknown` handling and
   its tests; a stuck send becomes an operator task, disclosed.
4. **Approval recommendations.** Removes the recommendations field from the return decision and the
   submission note's disagreement text; approve and return with a mandatory comment remain.

Descoping never removes the approval gate, the audit trail, the closure gates or the authentication
baseline. Anything descoped moves to the disclosed limitations register.

## 17. Tests

Tests are organised by STRIDE threat identifier where the mitigation is code, so the suite doubles
as evidence that those mitigations exist. A control delivered by policy, configuration or hosting
carries no threat tag and is listed against the control in Section 15 instead.

- Unit: working-day arithmetic including Good Friday, Easter Monday and public holidays; a
  seeded-calendar test asserting every seeded year contains both Good Friday and Easter Monday; both
  worked examples in Appendix B.2; milestone generation and regeneration; receipt-correction
  recalculation; state transitions; approval invalidation; stale revision rejection.
- Milestones: no final-response milestone exists before submission and one exists after it; later
  progress updates are created when the previous one completes and when its due date passes, with a
  case exercising day 80 and beyond; supersession by correction, by return and by invalidation; a
  completed obligation's completion carries over to its replacement; a superseded row and its
  replacement coexist under the partial unique index; only a complainant-addressed message completes
  a milestone, and a provider progress update completes nothing.
- Single authority: no `Correspondence` field duplicates an attempt fact or a current-state fact;
  approval linkage resolves only through `Approval.final_response_id`; completion resolves only
  through `Milestone.completed_correspondence_id`.
- Integration: persistence, permissions, transactional approve and close, correspondence logging,
  approval snapshot retention, export scoping and column shape, receipt-correction preview
  rendering.
- Approval loop: return without comment rejected; resubmission creating a new revision and
  superseding the final-response milestone; approver decision final; closure refused with an
  invalidated approval; comment and submission note immutable after a decision; the queue excludes an
  invalidated approval.
- Closure: one negative test per unmet gate; the day-40 boundary in both directions; a missed
  notification recorded as a breach with `waived_reason = missed`; a case resolved before day 40 and
  closed after it waiving the notification as `not_applicable`, not `missed`; the closure ordering
  leaving no refused-then-unclosable state; an unresolved notification refused once the final
  response has been sent; return-to-investigation blocked after provider acceptance.
- Negative: self-approval, cross-handler access, non-allowlisted recipient, editing a frozen message,
  editing under live approval, a handler attempting a receipt correction refused, a receipt
  correction on a closed case refused.
- Correspondence: success, definite failure, unknown acceptance and its recorded resolution, one
  confirmation producing exactly one attempt, only definite failures retryable, a resend recorded as
  a new attempt on the same record, a handler resolving a non-final type, stale sending flagged by
  the scheduled check.
- Scheduling: idempotent digest for a repeated period key; recorded failure; a failed period re-run
  on the existing row without creating a second row.
- Audit and templates: audit-table privilege revocation against the application role;
  referral-rights content present in the complainant-addressed unresolved and final-response
  templates and absent from provider templates.
- Security controls: CSRF token missing or wrong rejected on every POST; cookie flags set on the
  session cookie; idle session expiry enforced; each control pointed at its test.
- PostgreSQL: full suite against the deployment database before submission.
- Security scanning: a source and dependency scan and a container image scan. Coverage stated
  factually: source and dependency scanning for known patterns and published advisories, image
  scanning for vulnerable packages in the built layers, and a baseline dynamic scan of the deployed
  application for transport and header configuration. Unscanned, and stated as such: authenticated
  business-logic and authorisation paths beyond the automated tests, the email provider's
  configuration, host and network hardening, and any library without a published advisory. Each
  finding's response is recorded.
- Accessibility: automated checks plus manual keyboard review, with failures recorded.

## 18. Repository and assessment deliverables

- Source with meaningful incremental history and AI-generated code flagged.
- Migrations and synthetic seed data.
- Working Dockerfile and deployment documentation.
- Example environment file with placeholders only.
- Automated tests and documented commands.
- Security-scan output and remediation evidence.
- Deployed application with role-specific accounts supplied to the lecturer.
- Entity relationship diagram and numbered level-1 data flow diagram with trust boundaries, naming
  the email provider and the insurer as external entities.
- STRIDE threat table covering every boundary-crossing flow, including provider correspondence and
  the insurer flow, with mitigations.
- Role and CRUD permissions table, route by route, naming the service or system actor.
- GDPR write-up covering lawful basis, minimisation, retention, visibility and disclosure to the
  insurer.
- Limitations register as a factual list.
- Governance policy, operational runbook and incident walk-through.
- Approximately 2,500-word technical write-up with Harvard references and cover page.
- Demonstration video and the live demonstration in week 12, including the defended recommendation.
- Accessibility review.
- AI-usage log and AI Fluency declaration appendix.
- Decision log including the hindsight question, the package-naming decision, the adopted timing
  conventions and the descope ladder.

### Demonstration script

Each retained route is demonstrated, and each has a template and a test behind it.

1. Login as handler; intake a complaint with a deliberately mistyped receipt date - 3 November
   entered as 3 October - and show the calculated deadlines that follow from the wrong date.
2. Reviewer opens the receipt-correction preview, shows every affected milestone old against new, and
   confirms the correction. Show supersession, the carried-over acknowledgement completion, the
   created corrective progress update, and the recalculated day-40 position.
3. Send the acknowledgement and show the single attempt recorded; show a definite failure and its
   retry; show an unknown acceptance and its resolution with a note, including a handler resolving a
   non-final type.
4. Export the register and show the log columns, then show the audit entry the export wrote.
5. Submit the outcome, return it with a comment, resubmit, approve.
6. Send the final response; show the unresolved notification refused after it; close the case and
   show a waived milestone with its enumerated reason and, where applicable, a recorded breach.

The assessment prohibits AI authorship of the design-decision analysis, security findings discussion,
accessibility review and limitations discussion. Those remain the student's own work; the
limitations register is a factual list, not that discussion.

## 19. Delivery approach

Following the CA2 session sequence:

1. Record the hosting decision, then commit the baseline with the decision log, the rule register,
   the descope ladder, a DFD draft and the STRIDE table with threat identifiers.
2. Repository, Flask skeleton, PostgreSQL in Docker Compose with owner and application roles,
   authentication, container build; first tests and first scan in the same slice.
3. Prove real sending to one allowlisted address, or adopt the sandbox fallback and disclose it.
4. Deadline engine with the Appendix B fixtures and both worked examples.
5. Case journey: intake, investigation, approval with snapshot, correspondence, closure gates, audit.
6. Role and permission tests written alongside, not after.
7. Tests and scans re-run at each slice; DFD and STRIDE refreshed before the freeze; accessibility
   review completed before submission.
8. Governance documents, demo video, then the written report.
9. Live demonstration.

Submission is at the end of course week 11, with the demonstration in week 12 and a late penalty
stated in the timetable. Confirm both before planning further.

Available hours remain unconfirmed; plan conservatively around work and family commitments and
re-estimate after the first slice.

## 20. Open decisions

- Confirmation of the two adopted, unverified timing conventions: the day-of-receipt convention and
  the return-clock question.
- Retention period confirmation.
- Hosting provider selection against the three requirements in Section 4, with the monitoring tool.
- Email provider, test recipient and the uncertainty age threshold.
- CSS framework and visual design.
- Any lecturer requirement for a specific development database.
- Confirmed timetable and sustainable weekly effort.

## 21. Reference and evidence register

Primary coursework source: MCLCD_Oct26_CA2_LowCodeNoCodeAIDev.docx, read 9 November 2026, confirmed
applicable to this deliverable and to the low-code comparison in Section 4.

Additional source: Low-Code-No-Code-Project-Brief.pdf, confirmed applicable as the source of the six
minimum requirements mapped in Section 16.1. Neither source requires migrations.

Regulatory sources, verified: see Appendix B. The single instrument is S.I. No. 81 of 2025. The June 2025 insurance newsletter located during verification predates the Code's commencement on
24 March 2026, not the Code itself, and uses superseded "business day" wording; it is retained only
as history.

## 22. Revision history

| Version | Change |
|---|---|
| 0.2 | Initial product definition and specification. |
| 0.3 | Minimum release introduced; committed and optional scope separated. |
| 0.4 | Contradictions resolved: no post-approval editing, approval snapshots, milestone records, acceptance uncertainty, permission matrix, scheduled runs, single scope table, single test list. |
| 0.5 | Approval confined to the final response; approve-return-resubmit loop; receipt correction and CSV export promoted; PostgreSQL only; modular architecture and guardrail; baseline authentication hardening; milestone supersession; recipient types. |
| 0.6 | Criteria reduced from 27 to 15 and mapped to brief minima; regulatory provisions verified in Appendix B; stakeholder and platform-comparison sections added; architecture reduced to three rules; enumerations as validated text; CRUD permission table; milestone waiver; course-week checkpoints and feature freeze; STRIDE-tagged tests. |
| 0.7.1 | Completeness and logic repair. Appendix B completed from B.1 to B.9, including the inbound-correspondence gap and the Regulation 106 export mapping in B.5, and the 2027 example corrected to Friday 2 April with Easter Monday excluded. Closure service ordering written as an ordered transaction so gate 4 no longer refuses what it then records. `waived_reason` defined by whether the obligation was ever owed, so a case resolved before day 40 is not recorded as a breach. Receipt-correction preview, completion carry-over, corrective update and closed-case refusal. Final-response milestone created at submission; later progress updates generated on completion or due date. Single-authority rules with `Correspondence.milestone_id` and `Correspondence.approval_id` removed. Handler resolution for non-final message types. Route-level permissions with a service column and CLI reassignment. Export shape defined. Demonstration script and additional security tests. Limitations register, write-up guidance and descope ladder. Hosting decision before the baseline. |

### Decision log entries added at 0.7.1

- **Package naming.** Package names follow the code as built and are justified in the write-up; no
  naming scheme is imposed in advance.
- **Timing conventions.** The clock starts on the next working day after receipt, and a return
  restarts the final-response clock. Both are adopted for the build and both are unverified.
- **Descope ladder.** Cut order is CSV export, provider recipients, unknown-acceptance flow, approval
  recommendations; descoping never removes the approval gate, the audit trail, the closure gates or
  the authentication baseline.

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
- Earlier drafts claimed stakeholder validation, seven brief minima, and that the brief required
  migrations and scanning; no stakeholder validation has occurred, the brief sets six minima, and
  tests, the Dockerfile and scanning are CA2 requirements.
- Earlier drafts stored milestone and approval references on `Correspondence`; linkage is stored
  once, on `Milestone.completed_correspondence_id` and `Approval.final_response_id`.

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
- handler_id (foreign key to User, required; must hold the handler role; changed only by the CLI
  reassignment command)
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

Due dates derive from Milestone records. No final-response milestone exists before submission.

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
- final_response_id (foreign key to Correspondence, required; the only approval linkage)
- reviewer_id (foreign key to User, nullable until a decision; must hold the compliance role and
  differ from the handler)
- decision (text, required; validated against: pending, approved, returned; default pending)
- comment (text, required on return, optional on approval; write-once once decided_at is set)
- recommendations (text, optional)
- submission_note (text, optional; write-once once decided_at is set)
- package_snapshot (structured data, required; immutable copy of the reviewed investigation fields
  and final-response recipient type, recipient, subject and body)
- content_hash (text, required)
- submitted_at (timestamp, required)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)
- A pending approval with invalidated_at set is excluded from the reviewer queue.

### Correspondence
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
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
- provider_accepted_at (timestamp, optional; set on acceptance, or at resolution time when
  acceptance is confirmed after uncertainty)
- attempt_count (integer, default 0)
- last_attempted_at (timestamp, optional)
- provider_reference (text, optional)
- last_error (text, optional)
- created_at (timestamp)
- Editable only while draft and not the final_response_id of a live Approval.
- Holds no approval reference and no milestone reference. Attempt history lives only in SendAttempt.

### SendAttempt
- id (integer, primary key)
- correspondence_id (foreign key to Correspondence, required)
- attempted_at (timestamp, required)
- result (text, required; validated against: provider_accepted, failed, acceptance_unknown)
- error_code (text, optional)
- error_detail (text, optional; excludes secrets)
- resolved_by_id (foreign key to User, optional)
- resolved_at (timestamp, optional)
- resolution (text, optional; validated against: confirmed_accepted, resend_authorised)
- resolution_note (text, optional; required when a resolution is recorded)
- Per-attempt history only. No current-state field is stored here: attempt_count, last_attempted_at,
  provider_reference and last_error belong to Correspondence, and no field name appears in both.

### Milestone
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- type (text, required; validated against: acknowledgement, progress_update,
  unresolved_notification, final_response)
- sequence (integer, required)
- due_date (date, required)
- completed_correspondence_id (foreign key to Correspondence, optional; the only completion linkage,
  and only to a complainant-addressed message)
- completed_at (timestamp, optional)
- superseded_at (timestamp, optional; set by receipt correction, return or invalidation)
- waived_at (timestamp, optional; set only at closure)
- waived_reason (text, optional; validated against: not_applicable, missed; required when waived_at
  is set)
- created_at (timestamp)
- Partial unique index on (complaint_id, type, sequence) where superseded_at is null. Superseded rows
  keep their type and sequence and remain readable; replacements reuse them.

### ScheduledRun
- id (integer, primary key)
- job_name (text, required)
- period_key (text, required)
- status (text, required; validated against: started, succeeded, failed)
- started_at (timestamp, required; updated when a failed period is re-run)
- finished_at (timestamp, optional)
- item_count (integer, optional)
- recipient (text, optional; allowlisted)
- error_summary (text, optional)
- Unique on (job_name, period_key). A failed period is re-run by updating this row, not by inserting
  a new one.

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
- Every seeded calendar year contains Good Friday and Easter Monday; a test asserts it.

A case-note entity is deferred to Section 16.2.

## Routes

| Method | Path | Does |
|---|---|---|
| GET | /login | Show login form |
| POST | /login | Authenticate and start session |
| POST | /logout | End session |
| GET | / | Dashboard with counts, milestones and urgent actions |
| GET | /complaints | List and filter authorised complaints |
| GET | /complaints/export | CSV export of the filtered, authorised register, one row per case |
| GET | /complaints/new | Show intake form |
| POST | /complaints | Create complaint, generate the receipt-derived milestones, create acknowledgement draft |
| GET | /complaints/<id> | Show case, milestones, correspondence and audit |
| POST | /complaints/<id>/investigation | Save investigation draft; first save begins investigating |
| GET | /complaints/<id>/receipt-correction | Reviewer preview of affected milestones before correction |
| POST | /complaints/<id>/receipt-correction | Reviewer correction with reason and recalculation |
| POST | /complaints/<id>/correspondence | Create a controlled draft |
| POST | /correspondence/<id>/edit | Edit a draft not under live approval |
| GET | /correspondence/<id>/preview | Preview recipient, subject, body and approval status |
| POST | /correspondence/<id>/send | Verify authorisation or approval, persist, then send |
| POST | /correspondence/<id>/retry | Retry a definite failure with unchanged content |
| POST | /correspondence/<id>/resolve-uncertainty | Record acceptance evidence or authorise resend |
| POST | /complaints/<id>/submit-outcome | Snapshot the package, create the final-response milestone and open approval |
| GET | /approvals | Review queue of pending, non-invalidated approvals with ages and prior rounds |
| POST | /approvals/<id>/decision | Approve or return the snapshotted package |
| POST | /complaints/<id>/return-to-investigation | Invalidate approval; refused after provider acceptance |
| POST | /complaints/<id>/close | Enforce every closure gate in Section 8, record a breach or waive open milestones, close |
| GET | /health | Minimal health status without sensitive information |

Every route above has a template. The export, receipt-correction and uncertainty-resolution routes
each additionally have a test and a step in the demonstration script in Section 18.

### Operator CLI commands

Outside the application permission model; no route exposes them.

| Command | Does |
|---|---|
| provision-user, deactivate-user | Create or deactivate an account; refuses to remove the last active compliance reviewer or deactivate a handler with open cases |
| reassign-handler | Change `Complaint.handler_id` with an audit entry; refused for a closed case; leaves milestones untouched |
| deadline-check | Run the scheduled deadline, stuck-send and digest job; writes `ScheduledRun` |

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
- Flask-SQLAlchemy and Alembic; every schema change via migration, because the schema is owned here,
  not because a source requires migrations.
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
- Approval applies to the final response only; the other three types are handler-confirmed at the
  `/send` POST.
- Comment mandatory on return, optional on approval; approver decisions are final, with no appeal,
  override or conditional approval; comment and submission note write-once after a decision.
- Approved content never edited; change requires invalidation and resubmission.
- Return-to-investigation refused after the final response is provider-accepted.
- Closure requires every gate in Section 8; a missed day-40 notification is recorded as a breach;
  open milestones are waived with an enumerated reason.
- An unresolved-at-40-days notification is never sent after the final response has been sent.
- Provider acceptance is never described as delivery.
- All four message types are sent through the app with a recipient type and logged automatically.
- Templates are selected by message type and recipient type; mandatory content comes from Appendix B.
- Progress updates repeat before and after the 40-working-day point and never reset the receipt date
  or resolution target.
- Milestones are stored per obligation; only a complainant-addressed message completes one, through
  `Milestone.completed_correspondence_id`; current deadlines derive from open, non-superseded
  milestones.
- Deadline calculation uses the Appendix B conventions, including the Good Friday and Easter Monday
  exclusions.
- Countdowns show label, exact date and text urgency.
- Outbound content persisted before any send attempt; one confirmation produces one attempt, recorded
  individually in `SendAttempt`.
- Real sending restricted server-side to allowlisted addresses; no unrestricted CC or BCC.
- Failed and uncertain sends remain visible and never complete milestones.
- Unknown acceptance requires a recorded, audited resolution note; a resend is a new attempt on the
  same record; the scheduled check flags stale sending records and never resends.
- Scheduled runs are idempotent per job and period, record failures, and a failed period is re-run by
  updating the existing row.
- CSV export respects record permissions, is one row per case, excludes narrative and contact detail,
  carries the Regulation 106 fields listed in Appendix B.5, and is audited.
- Synthetic data only; credentials from environment configuration, never in Git or AI tools.
- Scheduled work runs through a documented CLI command, not a web route.
- Deployment uses separate database owner and application roles; audit table protected by revoked
  UPDATE and DELETE for the application role.
- Retention is a documented policy only; no deletion feature is implemented.
- Dockerfile, deployment documentation, tests, scan evidence, ERD, DFD, STRIDE table, role table,
  GDPR write-up, limitations register, demo video and Git history are required deliverables.

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