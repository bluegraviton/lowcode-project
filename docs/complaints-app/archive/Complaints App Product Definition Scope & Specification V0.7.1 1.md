
# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.7.1 — 10 November 2026
Status: Minimum release specified for implementation; selected implementation decisions remain
open in Section 20. Regulatory provisions verified at
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
- CSV export, baseline authentication hardening and responsive checking are committed as supporting deliverables for Criterion 15 rather than as separate criteria.
## 5. Regulatory requirements register

The full register, with citations, worked examples and outstanding checks, is Appendix B. This
section records only what drives code and what remains open.

### Verified; to be implemented

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

### Adopted, unverified

The following convention is recorded in Appendix B:

- Whether the day of receipt counts as the first working day. The build starts the clock on the
  next working day after receipt. That is a chosen convention, not a verified reading.

The following additional convention is recorded in Appendix B.3:

- First submission for approval represents completion of the investigation. The build sets
  `Investigation.completed_at` once, at that first submission. This is a proxy for the statutory
  trigger, not a verified interpretation that internal submission and actual investigation
  completion necessarily coincide. The prototype does not separately capture an earlier actual
  completion date, so a delay before first submission is not measured by its final-response clock.

### Deadline-preservation control

The original final-response deadline is retained through a reviewer return, approval invalidation
and resubmission. These events neither clear `Investigation.completed_at` nor supersede or replace
the final-response milestone. A revised approval package therefore does not obtain a fresh
five-working-day period.

Preserving the first deadline is a chosen internal control. It removes the build's earlier
restart convention; it does not resolve the unverified first-submission proxy described above.

### Still open

- The retention period, proposed as six years from closure and labelled unverified.
- Paragraph letters within Regulation 1054 other than subparagraph d. Independent approval of the
  final response is a chosen internal control and must not be described as a statutory
  requirement. Where the source is silent, this section records the gap rather than an invented
  rule; Appendix B records only the provisions that drive implemented behaviour.


## 6. Roles, access and permissions

Two roles: handler and compliance. Each user holds exactly one role, which structurally prevents
self-approval. The same single-value model means a compliance officer cannot also handle cases,
and there is no reviewer cover when the only reviewer is absent; both are recorded in the
limitations register in Section 15.

### Actions by route

Actor named for every route. No route writes an entity directly; the named service performs the
write inside a transaction.

| Route or action                                 | Handler                   | Compliance reviewer              | Service or system actor                                                                                                                                                                                                              | Record scope and enforcement                                                                                                       |
| ----------------------------------------------- | ------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `GET /login`                                    | Anonymous                 | Anonymous                        | Session issuer                                                                                                                                                                                                                       | No case data                                                                                                                       |
| `POST /login`                                   | Anonymous                 | Anonymous                        | Authentication service                                                                                                                                                                                                               | Password hash check; CSRF                                                                                                          |
| `POST /logout`                                  | Yes                       | Yes                              | Session terminator                                                                                                                                                                                                                   | Own session only                                                                                                                   |
| `GET /`                                         | Yes                       | Yes                              | Dashboard query service                                                                                                                                                                                                              | Handler: assigned. Reviewer: all                                                                                                   |
| `GET /complaints`                               | Yes                       | Yes                              | Scoped query                                                                                                                                                                                                                         | Handler: assigned. Reviewer: all                                                                                                   |
| `GET /complaints/export`                        | Yes                       | Yes                              | Export service                                                                                                                                                                                                                       | Same filters and permissions as the list; audited                                                                                  |
| `GET /complaints/new`                           | Yes                       | No                               | Intake form renderer                                                                                                                                                                                                                 | No case record yet                                                                                                                 |
| `POST /complaints`                              | Yes                       | No                               | Complaint service: creates the complaint, the acknowledgement, first routine progress-update and unresolved-notification milestones, and the acknowledgement draft                                                                   | Handler self-assigns                                                                                                               |
| `GET /complaints/<id>`                          | Yes                       | Yes                              | Case query                                                                                                                                                                                                                           | Handler: assigned. Reviewer: all                                                                                                   |
| `POST /complaints/<id>/investigation`           | Yes                       | No                               | Investigation service: saves permitted drafting changes without altering an existing completed_at or final-response due date                                                                                                         | Assigned only                                                                                                                      |
| `GET /complaints/<id>/receipt-correction`       | No                        | Yes                              | Correction preview service: every affected milestone, old due date against new; final-response deadline unchanged                                                                                                                    | Any case                                                                                                                           |
| `POST /complaints/<id>/receipt-correction`      | No                        | Yes                              | Correction service: supersedes and recreates receipt-derived milestones, carries completion, creates the corrective update; final-response deadline unchanged                                                                        | Reason required; audited; refused on a closed case                                                                                 |
| `POST /complaints/<id>/correspondence`          | Yes                       | No                               | Correspondence service: creates a controlled draft, including a replacement for an authorised final response where permitted                                                                                                         | Assigned                                                                                                                           |
| `POST /correspondence/<id>/edit`                | Yes                       | No                               | Correspondence service                                                                                                                                                                                                               | Assigned; never-authorised draft; editing permitted only under Section 10                                                          |
| `GET /correspondence/<id>/preview`              | Yes                       | Yes                              | Preview renderer                                                                                                                                                                                                                     | Same read scope as the case                                                                                                        |
| `POST /correspondence/<id>/send`                | Yes, assigned cases only  | Yes, approved final response onl | Send service: checks permissions, authorisation, approval and ordering; commits one pending attempt reservation before the provider call; records the result in a second transaction under Section 10                                | Handler: assigned. Reviewer: any                                                                                                   |
| `POST /correspondence/<id>/retry`               | Yes                       | Yes                              | Send service: definite failures only, unchanged content, new attempt on the same record; rechecks approval and Section 8 ordering                                                                                                    | Same scope as sending                                                                                                              |
| `POST /correspondence/<id>/resolve-uncertainty` | Yes, non-final types only | Yes, any type                    | Resolution service: resolution note required; records acceptance or authorises a resend; every resulting attempt passes through the send service                                                                                     | Handler: assigned. Reviewer: any                                                                                                   |
| `POST /complaints/<id>/submit-outcome`          | Yes                       | No                               | Submission service: snapshot, hash and new Approval row on every submission; first submission alone sets completed_at and creates the final-response milestone                                                                       | Assigned; resubmission preserves the original completion timestamp and due date                                                    |
| `GET /approvals`                                | No                        | Yes                              | Queue query: excludes invalidated and decided approvals                                                                                                                                                                              | No handler access                                                                                                                  |
| `POST /approvals/<id>/decision`                 | No                        | Yes                              | Decision service: sets reviewer and decision time, freezes comment and submission note; a permitted return moves the case to investigating and increments its revision without changing completed_at or the final-response milestone | Any case they did not handle; return safety check under Section 8                                                                  |
| `POST /complaints/<id>/return-to-investigation` | Yes                       | Yes                              | Invalidation service: invalidates the live approval, moves the case to investigating and increments its revision; preserves completed_at and the original final-response milestone                                                   | Assigned (handler); any (reviewer); return safety check under Section 8                                                            |
| `POST /complaints/<id>/close`                   | Yes                       | Yes                              | Closure service: evaluates gates, records the day-40 outcome, waives remaining open milestones with enumerated reasons, and closes                                                                                                   | Assigned (handler); any (reviewer)                                                                                                 |
| `GET /health`                                   | No                        | No                               | System, for monitoring                                                                                                                                                                                                               | No sensitive information                                                                                                           |
| CLI: provision or deactivate a user             | No                        | No                               | Operator with hosting or repository access                                                                                                                                                                                           | Outside the application permission model                                                                                           |
| CLI: reassign a case handler                    | No                        | No                               | Operator with hosting or repository access                                                                                                                                                                                           | Outside the permission model; audited; refused for a closed case                                                                   |
| CLI: scheduled check                            | No                        | No                               | System, invoked by the operator                                                                                                                                                                                                      | Checks deadlines and stuck sends, performs permitted routine milestone generation, records ScheduledRun and sends the staff digest |

No route writes a milestone directly. Milestone writes are performed by the responsible services:
the complaint service creates intake obligations; the correction service supersedes and replaces
receipt-derived obligations; the submission service creates the final-response obligation once;
the send and resolution services record completion; the closure service records waivers; and the
routine-generation service creates later routine updates.

Routine generation is invoked through the completion, page-rendering and scheduled-check entry
points described in Section 9. Reviewer return and approval invalidation do not write or supersede
the final-response milestone.

Optional routes carry no rows here because they are deferred to Section 16.2. Any implementation
must add its explicit permissions and enforcement point before release.

The CLI reassignment command exists so that a departing handler does not strand live deadlines.
It runs outside the application permission model, holds repository and hosting credentials, and is
recorded as an AuditEvent naming the operator. It changes Complaint.handler_id only; milestones
belong to the complaint and are untouched. Reassignment through the interface remains Optional.

### Data permissions

The application roles initiate permitted actions; the services perform the resulting writes.
System-driven updates listed below do not give reviewers permission to edit investigation findings
or other handler-authored content.

| Entity         | Handler                                                                                                                             | Compliance                                                                                                                            | Writes performed by                                                                                                                                                                             | Enforced where                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Complaint      | Create own; read assigned; initiate permitted lifecycle changes on assigned; no delete                                              | Create none; read all; initiate receipt correction and permitted lifecycle changes; no delete                                         | Complaint, investigation, submission, decision, invalidation, correction and closure services; operator CLI for reassignment                                                                    | Scoped queries and service checks                          |
| Investigation  | Read and edit assigned investigation content where lifecycle permits; submit; no delete                                             | Read all; approve or return packages, but no direct editing of investigation content; no delete                                       | Investigation service for content; submission service for first completed_at; decision and invalidation services for revision changes                                                           | Scoped queries, lifecycle and service checks               |
| Approval       | Read on assigned; initiate submission; no delete                                                                                    | Read all; decide eligible pending packages; initiate permitted invalidation; no delete                                                | Submission, decision and invalidation services                                                                                                                                                  | Service checks, revision checks and constraints            |
| Correspondence | Read assigned; create and edit permitted drafts; initiate permitted sends, retries and non-final uncertainty resolutions; no delete | Read all; approve final responses; initiate permitted sends, retries and uncertainty resolutions; no draft-content editing; no delete | Correspondence service; complaint and correction services for generated drafts; decision service for final-response authorisation; send, resolution and scheduled-check services for send state | Scoped queries, immutable-content rules and service checks |
| Milestone      | Read on assigned; no direct write                                                                                                   | Read all; no direct write                                                                                                             | Complaint, correction, submission, send, resolution, closure and routine-generation services                                                                                                    | Complaint scope and milestone rules                        |
| SendAttempt    | Read on assigned; no direct write                                                                                                   | Read all; no direct write                                                                                                             | Send, resolution and scheduled-check services                                                                                                                                                   | Correspondence scope and send-state rules                  |
| AuditEvent     | Read on assigned; no direct write, update or delete                                                                                 | Read all; no direct write, update or delete                                                                                           | Audit service and operator CLI append entries                                                                                                                                                   | Complaint scope; database UPDATE and DELETE revocation     |
| Complainant    | Read and create with assigned complaint; no delete                                                                                  | Read all; no direct update or delete                                                                                                  | Complaint service                                                                                                                                                                               | Derived complaint scope                                    |
| User           | Read own profile; no account-administration writes                                                                                  | Read own profile; no account-administration writes                                                                                    | Operator CLI                                                                                                                                                                                    | CLI controls; no route changes roles                       |
| PublicHoliday  | Read; no write                                                                                                                      | Read; no write                                                                                                                        | Operator CLI calendar loader                                                                                                                                                                    | Read-only application access                               |
| ScheduledRun   | No direct access                                                                                                                    | No direct access                                                                                                                      | Scheduled CLI job                                                                                                                                                                               | Operator access and job-period constraint                  |

No role deletes complaint data, correspondence, approvals or audit events. There is no delete route
in the application.

### Enforced constraints

- Complaint.handler_id is required and must reference a user holding the handler role.
- Approval.reviewer_id is null until a decision. When set, it must reference a compliance user who
  differs from the handler.
- No route changes a user's role. Provisioning and deactivation are CLI operations, and the command
  refuses to remove the last active compliance reviewer or deactivate a user holding open
  complaints.
- Permissions are checked in services and scoped queries, with tests proving that a direct request
  from the wrong user fails.
- Reviewer return and return-to-investigation are permitted only where the current final response
  has no send attempt, or every attempt on it is recorded as a definite failure. They are refused
  while an attempt is sending, accepted or of unknown acceptance. A pending approval may be
  abandoned through a permitted return-to-investigation action, which invalidates it.
- A return or invalidation that moves the case to investigating increments the investigation
  revision once for that transition.
- First submission sets Investigation.completed_at and creates the final-response milestone once.
  Reviewer return, approval invalidation and resubmission preserve that timestamp, the milestone
  and its original due date.
- Approval validity is rechecked inside the sending and closing transactions. An earlier authorised
  final-response version without current valid approval cannot be sent or retried.
- Every send, retry and authorised resend passes through Section 8's ordering checks. Confirmation
  of uncertain acceptance is evidence resolution, not permission to bypass those checks.
- A receipt correction is refused on a closed case and never changes the final-response deadline.
- Approval.comment and Approval.submission_note become write-once once decided_at is set.
- Authorisation timestamps are never cleared to enable content editing.
- Denials are audited.

Terminology: a handler confirms a message; a reviewer approves a final response. The authorising
user of a final response is the approving reviewer, and the user who initiates its send is recorded
separately in the audit trail.
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
- Creates a corrective progress update where the acknowledgement has already been sent, because sent content is frozen and quotes the original receipt date. It is a `progress_update` milestone taking the next unused sequence for the case, and its due date is the correction date plus five working days. That date follows the correction, not the receipt, so the twenty-working-day formula does not apply to it and the sequence exists only to order it. The five working days mirror the acknowledgement standard it corrects and are a chosen internal standard, not a statutory period. A further correction supersedes an open corrective milestone and creates a replacement, so a corrected date is never quoted twice. It appears in the milestone panel and the dashboard like any other, and if it is still open with a passed due date at closure it is waived as `missed` under Section 8. The answer does not extinguish it, because its purpose is to correct a statement the complainant already holds, so it is the one progress update exempt from the rule that an answer ends the obligation.
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

## ## 8. Case lifecycle

States: Logged → Investigating → Pending Approval → Approved → Closed.

The first save of the investigation record moves Logged to Investigating. A return moves the case
back to Investigating, remains in the history, and resubmission creates a new Approval row at a new
revision.

Acknowledgement and progress updates are correspondence milestones, not states.

### Post-approval changes

Approved content is never edited. Any change requires returning the case to Investigating, which
invalidates the approval and is audited with actor, time and reason.

A return or invalidation preserves `Investigation.completed_at` and the existing final-response
milestone, including its original due date. The final-response clock continues while the case is
Investigating or Pending Approval again. Resubmission changes the approval package, not the
deadline. The state Investigating therefore describes the current workflow activity; it does not
mean that the original completion timestamp has been erased.

The authorised final-response record itself is not reopened. A changed authorised outcome requires
a new final-response record for the next submission, as Section 10 sets out. The earlier record
and its authorisation timestamps remain unchanged. A never-authorised draft may be edited only
under Section 10's draft-editing rule.

Return-to-investigation is permitted only where the current final response has no send attempt, or
every attempt on it is recorded as a definite failure. It is refused while any attempt is sending,
accepted or of unknown acceptance. The same safety check applies whether the return is initiated
by the handler or reviewer.

Closed case content is read-only. Reopening after closure is out of scope, and a closed case cannot
have its receipt date corrected.

### Closure gates

A case may close only when every gate is satisfied. This list is the single definition of the
gates, including gate 4.

1. Findings, root-cause category, outcome, outcome rationale and redress amount are recorded for the
   current investigation revision.
2. A reviewer other than the handler approved the current revision and the exact final-response
   content now held, and that approval is not invalidated.
3. That final response reached `provider_accepted` status.
4. The day-40 position is settled and recorded as one of these outcomes: (a) answered in time,
   because the final response reached `provider_accepted` status on or before the 40-working-day
   due date; (b) notification accepted before the outcome, because the unresolved-at-40-days
   notification reached `provider_accepted` status and its accepted attempt preceded the case's
   first final-response attempt; or (c) breached, because neither (a) nor (b) applies, with the
   breach recorded in the closure transaction.
5. Closure is recorded as an audited transition by a user permitted by Section 6.

Outcome (b) establishes the ordering of the notification and final response. It does not by itself
assert that the notification met its own due date. A late notification retains its due date and
completion date as evidence of lateness.

For the rules below, a notification is in flight when its current status is `sending` or
`acceptance_unknown`, or when it has been authorised but its first attempt has not yet started.
The continued presence of `authorised_at` does not make an accepted or definitely failed
notification in flight.

Gate 4 refuses closure while an unresolved-at-40-days notification is in flight. A `failed`
notification is a definite outcome and does not itself block closure. It is assessed under the
gate: an answer in time satisfies (a); otherwise, if no notification was accepted before the
outcome, (c) applies.

Recording the outcome is the closure service's work, in this order inside one transaction:

1. Gates 1, 2 and 3 are evaluated; any failure refuses closure and names the gate.
2. The day-40 position is read from the current milestones and send history. A notification still
   in flight refuses closure. For a notification accepted normally, the service reads the
   `attempted_at` of the attempt whose result is `provider_accepted`. For acceptance confirmed
   after uncertainty, it reads the `attempted_at` of the attempt carrying
   `resolution = confirmed_accepted`.
3. The outcome defined by gate 4 is recorded. Under (c), the open unresolved-notification milestone
   is waived with `waived_at` set and `waived_reason = missed`, and an audit entry names who
   recorded the breach. Under (a), an open notification milestone is waived as `not_applicable`.
   Under (b), the accepted notification's milestone retains its completion evidence.
4. Remaining open milestones are waived under the applicability rules below.
5. The case is closed and the transition audited.

A definitely failed notification may be retried while the ordering rule permits, or remain as
failure evidence and be assessed at closure. An `acceptance_unknown` notification must first be
resolved. Confirming acceptance records its completion; authorising a resend permits another
attempt only where the ordering rule allows it.

### Answering and milestone waivers

Any milestone still open at closure is waived with an audit entry recording who waived it and why.
`waived_reason` is enumerated, and the test is whether the obligation was ever owed.

A complaint is answered when its current final response reaches `provider_accepted` status, using
`Correspondence.provider_accepted_at` as the answer timestamp. Investigation completion does not
end routine update obligations, because the final response is still outstanding. Administrative
closure does not extend them after the answer.

- `not_applicable` applies where a routine update or unresolved-notification obligation ceased to
  apply because the complaint was answered on or before its due date, or where an applicable
  obligation had not yet fallen due at closure.
- `missed` applies where the obligation remained applicable through its due date and that date
  passed without completion. Under gate 4(c), this is the unresolved-notification milestone's
  reason.
- A corrective progress update created by a receipt correction is exempt from the answer rule.
  It remains owed because it corrects a statement the complainant already holds. If its due date
  passed without completion, it is waived as `missed`.
- Receipt correction changes the dates against which applicability and lateness are assessed.
  Correction alone is not a reason to classify an obligation as `not_applicable`.

A routine progress update whose due date falls on or after the answer date is therefore waived as
`not_applicable` if it already exists and remains open. Routine updates whose due dates passed
before the answer remain assessable as missed; answering does not retrospectively remove them.
An acknowledgement's earlier applicability is not extinguished merely by a later final response.

A case answered on working day 30 and closed on day 50 therefore waives its open day-40 notification
as `not_applicable`. A case that passed day 40 without answering and without notifying records the
missed notification under gate 4(c). The enumeration stops a waiver disguising a missed deadline,
and stops a breach being manufactured solely because administrative closure occurred late.

### Ordering rule

The notification precedes the outcome, and the send service enforces the rule for every attempt:
`/send`, `/retry` and a resend authorised through `/resolve-uncertainty`.

- Once any final-response record for the case has a send attempt, no further attempt may be made
  on an unresolved-at-40-days notification for that case. Creating a replacement final-response
  record does not reset this case-wide check.
- While an unresolved-at-40-days notification is in flight, every final-response attempt is
  refused, including retry and authorised resend.

The composer applies the same restrictions. The unresolved type is not offered once a final
response has been attempted, and a final response cannot be released while a notification is in
flight. Confirmation of acceptance after uncertainty is evidence resolution, not a new attempt,
and remains permitted; any resulting resend must pass the send-service checks.

The minimum release models no discretionary closure exception. A case requiring an alternative
handling path cannot be closed, which is a disclosed limitation.

### Early resolution

Where a complaint is resolved to the consumer's satisfaction within five working days of receipt,
the full procedure need not apply, but the complaint must still be logged. The prototype uses the
normal journey for such cases and records the receipt date, the outcome, the final-response
acceptance date, the closure date and the correspondence actually sent. It does not model an
expedited path and does not claim that this record alone discharges the logging obligation;
assessing that against Regulation 106 belongs in the write-up.
## 9. Deadline engine and milestones

### Records

Each obligation is a stored milestone: complaint, type, sequence, due date, completion state,
completing correspondence, completion timestamp, `superseded_at`, `waived_at` and `waived_reason`.
Existing due dates are not overwritten. Completion, supersession and waiver are recorded on the
retained rows. Current deadlines derive from open, non-superseded milestones.

Receipt correction sets `superseded_at` on the receipt-derived milestones it replaces. A reviewer
return or approval invalidation does not supersede any milestone: in particular, the original
final-response milestone and due date remain current through resubmission.

Types: acknowledgement, progress update, unresolved notification, final response.

All working-day calculations use Appendix B.2 and the obligations recorded in Appendix B.3.
The use of first submission as the investigation-completion trigger is adopted, unverified.

All timestamps are stored in UTC. For closure and milestone comparisons, a timestamp is converted
to the Europe/Dublin local date before comparison with a due date.
### Generation

- Acknowledgement at receipt plus five working days: created when the complaint is created.
- First routine progress update at receipt plus twenty working days: created when the complaint
  is created.
- Unresolved notification at receipt plus forty working days: created when the complaint is
  created.
- Each later routine progress-update milestone is generated when its predecessor completes or
  its due date passes, using the routine twenty-working-day schedule. Before generating
  milestones, the service checks whether the current final response has reached
  `provider_accepted` status. If it has not, generation continues normally. If it has, the service
  may create only missing routine milestones whose due dates fall before the answer date, read
  from `Correspondence.provider_accepted_at`. This catch-up preserves obligations that fell due
  before the answer even if the scheduled check did not run. It must not create a routine
  milestone whose due date falls on or after the answer date. Existing future milestones are
  retained and dealt with under Section 8's waiver rule; their presence does not restart
  generation. These checks apply to every generation entry point, including completion, page
  rendering and the scheduled check. A corrective progress update follows Section 7's separate
  creation and due-date rule: answering does not prevent its creation, and its creation or
  completion does not generate a successor in the routine update chain.
- Final response at `Investigation.completed_at` plus five working days: created once, at first
  submission for approval, not at intake. First submission sets `Investigation.completed_at`
  under the adopted, unverified convention in Section 5 and Appendix B.3.
- Return, approval invalidation and resubmission preserve that completion timestamp and the
  original final-response milestone. No replacement final-response milestone is created.
  If its due date passes during review or rework, it remains overdue until completion.

Receipt correction supersedes the acknowledgement, every affected progress update and the
unresolved notification, and recreates the receipt-derived obligations from the corrected date.
It never touches the final-response milestone. Corrective updates retain the separate creation
and due-date rule in Section 7 rather than taking a due date from the receipt-based routine
schedule.

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

A return or invalidation does not remove the final-response countdown or reset its overdue
display. The original due date remains visible while the next approval package is prepared and
reviewed.

### Continued updates

The unresolved notification neither closes the case nor ends update obligations. There is no
maximum number of routine updates. Each update is its own message and milestone, and sending one
leaves the receipt date, the 40-working-day target and the final-response deadline unchanged.
Routine generation stops at the answer as specified above; corrective updates remain subject to
their separate rule.

Only a complainant-addressed message completes a milestone, recorded through
`Milestone.completed_correspondence_id`. A provider-addressed progress update, an internal staff
notice and any other non-complainant recipient complete nothing, because the obligation is owed to
the complainant. One message completes one obligation, not two.

The send service selects the milestone at acceptance, by type and sequence:

- An acknowledgement, an unresolved notification or a final response completes the single open,
  non-superseded milestone of that type for the case.
- A progress update completes the open, non-superseded progress-update milestone with the highest
  sequence whose due date is on or before the acceptance date; where none has fallen due, it
  completes the one with the lowest sequence.

Where an earlier routine update and a later one are both overdue, this selection completes the
later interval. The skipped earlier interval remains open and is assessed as `missed` at closure.
Completion after a due date does not erase lateness: due and completion dates remain visible.

For a final response, selection is additionally restricted to the correspondence record covered
by the current valid approval under Sections 8, 10 and 11. A replacement authorised version
therefore completes the original final-response milestone when accepted; an earlier authorised
version cannot be sent or retried to complete it.

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

Acknowledgement, progress update and unresolved notification require confirmation by the assigned
handler. A compliance reviewer may not confirm or send these non-final types. The final response
is sent by the assigned handler or, where necessary, by a compliance reviewer after a valid
approval exists.The
final response requires independent approval of the exact package, because it carries the outcome
and redress position.

For the three non-final types, the confirmation act is the
`POST /correspondence/<id>/send` submission itself, carrying the confirmation control. The first
database transaction stamps `authorised_by_id` and `authorised_at`, reserves the initial attempt
with `SendAttempt.result = pending`, and sets the correspondence status to `sending`. These changes
are committed together before the provider is called. The transaction and result-recording
sequence is defined under Flow and authorisation below.
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

Prepare → preview → confirm or approve → commit the attempt reservation → call the provider →
commit the result.

Authorisation freezes content: handler confirmation for the three non-final types, reviewer
approval for the final response. Authorisation timestamps are never cleared to enable editing.

The correspondence record holds recipient, recipient type, subject, body, template version,
authorising user, timestamps, status and the current-state send fields. Approval linkage is read
only from `Approval.final_response_id`; milestone completion is recorded only through
`Milestone.completed_correspondence_id`.

Every initial send, retry and authorised resend uses the following sequence.

1. In the first database transaction, the send service locks the complaint row and then the
   correspondence row. All attempt-creation paths use this same lock order. It rechecks
   permissions, content authorisation, current final-response approval where applicable,
   Section 8's ordering rule, and eligibility for this particular action.
2. For a non-final initial send, that transaction records authorisation. For every permitted
   attempt, it inserts one SendAttempt with `result = pending`, sets `attempted_at` to the
   reservation time, increments `Correspondence.attempt_count`, updates `last_attempted_at`, and
   sets the correspondence status to `sending`. The frozen content and attempt reservation are
   committed before any provider call. If this commit fails, the provider is not called.
3. The provider is called outside the database transaction, using the committed, frozen content.
4. In a second database transaction, the service locks the same complaint and correspondence,
   records the outcome on the reserved attempt, and updates the correspondence head consistently.
   The result is `provider_accepted`, `failed` or `acceptance_unknown`. Provider acceptance also
   records the acceptance timestamp and completes any eligible milestone under Section 9 in
   this transaction. A definite failure or unknown acceptance completes no milestone.

`pending` means that the attempt has been durably reserved but no outcome has been recorded. Its
`attempted_at` is the reservation timestamp, not proof that the external call began. The prototype
uses that timestamp for attempt ordering.

A repeated or concurrent confirmation cannot create a second initial attempt. After acquiring
the locks, it finds the existing reservation or changed correspondence state and returns the
existing state without calling the provider again. A retry requires a definite failure. An
authorised resend requires an unconsumed `resend_authorised` resolution for the latest uncertain
attempt; the new attempt reservation consumes that permission, so it cannot authorise multiple
resends.

If execution stops after reservation but before the result is committed, the attempt remains
pending and the correspondence remains sending. Once the configured stale-send threshold passes,
the scheduled check locks the same records and changes the pending attempt and correspondence
head to `acceptance_unknown`. It never resends automatically. This treatment is deliberately
conservative: a crash before the external call and a crash after provider acceptance can leave the
same database evidence.

A delayed provider result must not overwrite a stale-send classification or a human resolution.
The result-writing transaction updates the attempt only if it is still pending. Otherwise, it
records the late result as audit evidence without changing the resolved send state, and any
remaining uncertainty is handled through the resolution action.
### Editability

A message is editable only while its status is draft, it has never been authorised, and it is not the `final_response_id` of a non-invalidated approval. That covers the three non-final types, whose
drafts may be corrected in place after a return, because the returned approval is no longer live and the reviewed content is preserved in the approval snapshot.

The final response is different. Once authorised it is never edited, and invalidation does not reopen it: `authorised_by_id` and `authorised_at` record an authorisation that did happen and are never cleared, and the reviewed content is preserved in the package snapshot and its hash. Changing
an approved outcome means preparing a new final-response record, which the next submission snapshots, approves and sends. The earlier row is retained as the record of what was authorised and, where applicable, attempted.

Only the current final-response row may be sent or retried. The current row is the one referenced by the most recent non-invalidated approval; every earlier row is history and is refused by the send service.

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

The scheduled check flags any message left in `sending` beyond a configured age as `acceptance_unknown` and never resends automatically.

Retries and resends authorised under `resend_authorised` are attempts on the same record and pass through the same send service, so Section 8's ordering rule applies to them exactly as it applies to the first send.

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

### Completion and the final-response clock

`Investigation.completed_at` is null before first submission. First submission sets it once,
using that submission's timestamp as the prototype's proxy for investigation completion. This is
an adopted, unverified convention recorded in Section 5 and Appendix B.3; it does not establish
that actual completion could not have occurred earlier.

First submission creates the final-response milestone at that timestamp plus five working days.
A reviewer return, approval invalidation or resubmission neither clears the timestamp nor
supersedes or replaces the milestone. Further investigation or drafting may occur, but the
original clock continues. Resubmission therefore cannot make an overdue final response appear
within deadline again.

### Submission and snapshot

On each submission the system stores an immutable snapshot of the reviewed package: the
investigation fields for that revision plus the exact final-response recipient type, recipient,
subject and body, with a hash. The Approval stores the investigation revision at submission.

Each submission creates a new Approval row. Only first submission creates the final-response
milestone; subsequent submissions reuse the existing obligation and original due date.

An authorised final-response record is never edited. A changed authorised outcome uses a new
Correspondence record for the next submission, while the earlier record and its authorisation
timestamps are retained. A never-authorised draft may be edited only under Section 10's
draft-editing rule. In either case, changing the correspondence record does not change the
final-response deadline.

### Return and resubmission

A return must state a reason in the decision comment and may include recommendations or change
requests. The comment is mandatory on return and optional on approval.

The handler may edit the investigation and prepare the next final-response package, optionally
recording in the submission note what changed and any disagreement with the recommendations.
The note informs the next decision but never defers it.

A return applies to that revision only. Any compliance user may decide a resubmission, including
the reviewer who returned it; reviewer-shopping is recorded as a limitation. The approver's
decision is final: no appeal, no override, no conditional approval, and no closure without a
valid approval.

A reviewer return or approval invalidation moves the case to Investigating and increments the
investigation revision once for that transition. It preserves `Investigation.completed_at`,
the final-response milestone and its due date. Section 8's send-attempt safety check applies
before the transition is allowed.

Each round creates a new Approval row, so comments, recommendations, submission notes and
decisions form a history. Once a decision is recorded, `comment` and `submission_note` on that row
are write-once: `decided_at` freezes them and no later edit is accepted, by any role. Itemised
change requests with per-item responses are optional.

Approval validity is checked when the decision is made and again inside the send and close
transactions. A revision check rejects a stale submission. The reviewer queue lists only
pending, non-invalidated approvals, so an invalidated package leaves the queue; it remains
readable on the case.

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
update columns, steps taken through the state and progress columns, and the date the file was closed through the closure date column. The response summary is not exported, because narrative is excluded; that gap is
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

## 15. Security, privacy, operations and disclosed limitations

- Authentication with password hashing, CSRF protection, secure cookie and session settings, idle
  expiry, and server-side validation. Login throttling is optional.
- Authorisation in services and scoped queries, tested against direct requests.
- One authoritative audit event list: case creation, state transitions, approvals, returns,
  invalidations, receipt corrections, milestone waivers and breaches, correspondence attempts, uncertainty
  resolutions, denials, exports,
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
4. Two timing conventions are adopted but unverified: excluding the day of receipt from the working-day count, and using first submission for approval as the proxy for investigation completion. The prototype does not separately capture an earlier actual completion date.
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
   reviewer-only correction that previews the affected milestones, requires a reason, audits old and
   new values, supersedes prior
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
6. **Correspondence.** Send all four types with recipient type and a version-controlled template selected by type and
   recipient;
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
15. Delivery and evidence pack. Docker and PostgreSQL deployment from a clean checkout, baseline authentication hardening, responsive main-journey checking at 375 CSS pixels, CSV export of the authorised register, the test suite passing against PostgreSQL, one or two scanners with what each covers and what remains unscanned stated and each findings response recorded, the demonstration video including the mistyped-receipt-date scenario, the accessibility review, the AI-usage log and AI Fluency declaration appendix, and the Moodle submission package including the single write-up, cover page and AI declaration    

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

### 16.3 Implementation choices

- Users are created, deactivated, and have cases reassigned, by CLI. The command refuses to remove
  the last active compliance reviewer or deactivate a handler with open cases. Reassignment runs
  outside the application permission model.
- The holiday calendar is a version-controlled dataset including Good Friday and Easter Monday,
  covering the test period and the following year; a test asserts that every seeded year contains
  both.
- Templates are files in version control, keyed by message type and recipient type.
- One email provider is called inline; no queue or worker.
- No reassignment or administrative routes exist; reassignment is the operator CLI command only.

### 16.4 Checkpoints

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

1. **Minimum demonstrable workflow.** Removes CSV export, provider send pathway and the
   unknown-acceptance resolution flow together. Retains intake, deadlines, acknowledgement,
   progress updates, unresolved notification, approval, final response, closure, audit and
   authentication. A stuck send remains visible for manual investigation outside the application;
   no automated resend occurs.
2. **CSV export.** Removes the export route, template and tests; Section 3, Section 13, Appendix B.5
   and criterion 15 are updated to state that the log fields are readable on screen only.
2. **Provider send pathway.** Removes provider-addressed templates and the ability to send correspondence to a product provider or insurer. The insurer remains an external entity in the data flow diagram, STRIDE table and GDPR disclosure discussion. Any necessary insurer contact is made outside the application and disclosed as a limitation.
3. **Unknown-acceptance flow.** Removes the resolution route, the `acceptance_unknown` handling and
   its tests; a stuck send becomes an operator task, disclosed.
4. **Approval recommendations.** Removes the recommendations field from the return decision and the
   submission note's disagreement text; approve and return with a mandatory comment remain.

Descoping never removes the approval gate, the audit trail, the closure gates or the authentication
baseline. Anything descoped moves to the disclosed limitations register.
## 17. Tests

Tests are grouped by feature area and tagged with the relevant STRIDE threat identifier where the mitigation is code, so the suite doubles as evidence that those mitigations exist. A control delivered by policy, configuration or hosting
carries no threat tag and is listed against the control in Section 15 instead.

- Unit: working-day arithmetic including Good Friday, Easter Monday and public holidays; a
  seeded-calendar test asserting every seeded year contains both Good Friday and Easter Monday;
  both worked examples in Appendix B.2; milestone generation and regeneration; receipt-correction
  recalculation; state transitions; approval invalidation; stale revision rejection.
- Milestones: no final-response milestone exists before first submission and exactly one current
  final-response milestone exists after it; first submission sets completed_at and the original
  due date; repeated return, invalidation and resubmission preserve that timestamp, milestone
  identity and due date; a deadline that passes during rework remains overdue; receipt correction
  supersedes receipt-derived milestones but leaves the final-response milestone unchanged.
- Progress updates: later routine updates are created when the previous routine update completes
  or its due date passes, including a case exercising day 80 and beyond; a completed obligation's
  completion carries over to its receipt-correction replacement; a superseded row and its
  replacement coexist under the partial unique index; the completion selector skips superseded
  milestones; a message completes the later of two overdue routine updates and leaves the earlier
  one open; the corrective update follows its sequence-allocation rule and its correction-plus-five-
  working-days due date; routine generation does not duplicate an existing current obligation;
  routine generation stops at the answer date through completion, page rendering and the
  scheduled check; catch-up creates missing routine milestones due before the answer but none due
  on or after it; existing future milestones are retained without restarting generation; a
  corrective update can be created after the answer without generating a routine successor.
- Single authority: per-attempt history is held only in SendAttempt. Correspondence holds the
  current-state send fields attempt_count, last_attempted_at, provider_reference and last_error as
  a denormalised current-state view; the send service updates them atomically with the authoritative attempt record. provider_accepted_at records correspondence-level acceptance, not a per-attempt fact. Approval linkage resolves only through Approval.final_response_id; completion resolves only through Milestone.completed_correspondence_id; only a complainant-addressed message completes a milestone, and a provider progress update completes
  nothing.
- Integration: persistence, permissions, transactional approve and close, correspondence logging,
  approval snapshot retention, export scoping and column shape, receipt-correction preview
  rendering.
- Approval loop: return without comment rejected; a permitted return or invalidation increments the
  investigation revision once and preserves completed_at and the original final-response
  milestone; resubmission creates a new Approval row without creating another final-response
  milestone; approver decision final; closure refused with an invalidated approval; comment and
  submission note immutable after a decision; the queue excludes an invalidated approval; a newly
  approved replacement final response completes the original milestone when accepted.
- Closure: one negative test per unmet gate; the day-40 boundary in both directions; a missed
  notification recorded as a breach with waived_reason = missed; a case answered before day 40 and
  closed after it waives the open notification as not_applicable; a notification in flight under
  Section 8's definition refuses closure; a failed notification does not itself refuse closure;
  a failed notification with an answer after day 40 and no accepted notification records a breach;
  an answer on or before day 40 satisfies gate 4(a) despite an earlier failed notification;
  routine updates due on or after the answer date are not_applicable, while applicable updates
  missed before the answer remain missed; a corrective update is not extinguished by the answer.
- Ordering: notification send, retry and authorised resend are refused after any final-response
  attempt for the case, including an attempt on an earlier final-response record; every
  final-response attempt is refused while a notification is in flight; confirmation of acceptance
  after uncertainty remains permitted as evidence resolution, but cannot bypass the restrictions
  on a resulting resend.
- Negative: self-approval, cross-handler access, non-allowlisted recipient, editing a frozen message,
  editing under an approval that prevents editing, a handler attempting a receipt correction, and
  a receipt correction on a closed case are refused.
- Correspondence: success, definite failure, unknown acceptance and its recorded resolution; one
  confirmation produces exactly one initial attempt, including a repeated or concurrent submission
  of that confirmation; only definite failures use the retry action; an authorised resend follows
  uncertainty resolution as a new attempt on the same record; a handler can resolve a non-final
  type; stale sending is flagged by the scheduled check; an earlier final-response row without
  current valid approval is refused by send and retry; return is refused while the final response
  is sending, acceptance_unknown or provider_accepted, and permitted with no attempt or where every
  attempt is recorded as a definite failure; invalidation never clears authorisation timestamps or
  makes authorised content editable. 
- A reviewer cannot send an acknowledgement, progress update or unresolved notification; a
  reviewer can send an approved final response; a handler cannot send a final response before
  valid approval exists.
- Attempt transactions: frozen content and a pending attempt are committed before the provider
  is called; a failed reservation commit produces no provider call; repeated and concurrent
  confirmations produce exactly one initial attempt and at most one provider call for that
  reservation; every permitted retry or authorised resend creates one new attempt on the same
  correspondence record; resend permission cannot be consumed twice; interruption after
  reservation leaves a pending attempt that the stale-send check changes to acceptance_unknown
  without resending; a delayed result cannot overwrite stale classification or human resolution;
  successful result recording updates the attempt, correspondence head and eligible milestone
  completion atomically; competing notification and final-response reservations obey Section 8
  under the shared complaint lock.
- Scheduling: idempotent digest for a repeated period key; recorded failure; a failed period re-run
  on the existing row without creating a second row.
- Audit and templates: audit-table privilege revocation against the application role; audit events
  for the listed actions; referral-rights content present in the complainant-addressed unresolved
  and final-response templates and absent from provider templates.
- Security controls: CSRF token missing or wrong rejected on every POST; cookie flags set on the
  session cookie; idle session expiry enforced; each control pointed at its test.
- PostgreSQL: full suite against the deployment database before submission.
- Security scanning: record the selected tools and their actual coverage. Source scanning covers
  recognised insecure code patterns; dependency scanning covers published advisories for
  identified dependencies; container scanning covers vulnerable packages identified in the built
  image; a baseline dynamic scan covers the deployed transport and header configuration it can
  observe. Do not claim a scan category was covered unless that scan was run. Areas not covered by
  these scans include authenticated business-logic and authorisation paths beyond the automated
  tests, the email provider's configuration, and host and network hardening. Advisory-based scans
  do not establish that packages without reported advisories are safe. Each finding's response is
  recorded.
- Accessibility: automated checks plus manual keyboard review, with failures recorded.

The tests above trace to the committed criteria as follows:

| Test group            | Criteria       |
| --------------------- | -------------- |
| Unit                  | 2, 3, 5        |
| Milestones            | 2, 3, 5        |
| Progress updates      | 2, 5, 6        |
| Single authority      | 6, 10          |
| Integration           | 1, 2, 6, 8, 15 |
| Approval loop         | 1, 3, 4        |
| Closure               | 1, 4, 5        |
| Ordering              | 4, 6           |
| Negative              | 2, 3, 6, 8     |
| Correspondence        | 3, 6, 7, 8     |
| Scheduling            | 7              |
| Audit and templates   | 6, 11          |
| Security controls     | 8, 13, 15      |
| PostgreSQL            | 10, 15         |
| Security scanning     | 13, 15         |
| Accessibility         | 15             |
| Attempt transactions  | 6, 7, 8, 11    |

Tests that implement a mitigation in code additionally carry the relevant identifier from the
baseline STRIDE table. Criterion references do not replace those threat identifiers.

## 18. Repository and assessment deliverables

- Source with meaningful incremental history and AI-generated code flagged.
- Migrations and synthetic seed data.
- Working Dockerfile and deployment documentation.
- Example environment file with placeholders only.
- Automated tests and documented commands.
- Security-scan output, with what each scanner covers and what remains unscanned stated, and
  remediation evidence.
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

- Confirmation of the two adopted, unverified timing conventions: excluding the day of receipt from
  the working-day count, and using first submission for approval as the proxy for investigation
  completion.
- Confirmation of whether the workflow needs a separate capture of actual investigation completion
  before first submission. The current minimum release does not capture that earlier event; this
  limitation must remain disclosed unless the design is formally changed.
- Retention period confirmation.
- Hosting provider selection against the three requirements in Section 4, with the monitoring tool.
- Email provider, test recipient and the uncertainty age threshold.
- CSS framework and visual design.
- Any lecturer requirement for a specific development database.
- Confirmed timetable and sustainable weekly effort.

Reviewer return, approval invalidation and resubmission do not restart the final-response clock.
Preserving the first completion timestamp and original due date is the selected internal control,
not an open restart convention.

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
| 0.7.1 | Completeness and logic repair. Appendix B completed from B.1 to B.9, including the inbound-correspondence gap and the disclosed CSV limitations in B.5; the 2027 example corrected to Friday 2 April with Easter Monday excluded. Closure records the day-40 outcome in an ordered transaction and applies enumerated waiver reasons. Authorised correspondence remains immutable; a changed authorised final response requires a new record. Notification ordering applies to send, retry and authorised resend. Receipt correction provides preview, completion carry-over, a corrective update and closed-case refusal. First submission sets the investigation-completion proxy and creates the final-response milestone once; reviewer return, approval invalidation and resubmission preserve the original timestamp, milestone and due date. Later routine updates are generated on completion or due-date passage, stop at the answer, and remain separate from corrective-update generation. Milestone completion and approval linkage have one authoritative relationship each. Handler resolution is permitted for non-final message types. Route-level permissions name service actors, and operator CLI reassignment is outside the application permission model. Export shape, demonstration script, security tests and test-to-criterion mapping are specified. Limitations register, write-up guidance, descope ladder and pre-baseline hosting decision are recorded. |

### Decision log

| Decision | Adopted position | Status and consequence |
|---|---|---|
| Package naming | Package names follow the code as built and are justified in the write-up; no additional naming architecture is imposed in advance | Implementation choice |
| Day-of-receipt convention | Working-day counting begins on the next working day after receipt | Adopted, unverified; recorded in Section 5 and Appendix B.2 |
| Investigation-completion proxy | First submission for approval sets Investigation.completed_at once | Adopted, unverified; actual completion may have occurred earlier, and the prototype does not separately capture that earlier event |
| Final-response deadline preservation | Reviewer return, approval invalidation and resubmission preserve the first completed_at, the original final-response milestone and its due date | Internal control; replaces the earlier restart convention and prevents repeated review rounds from refreshing the displayed deadline |
| Authorised final-response changes | An authorised record is immutable; a permitted changed outcome uses a new record and a new approval package | Authorisation timestamps and earlier content remain evidence; the original final-response deadline is unchanged |
| Notification ordering | Every send, retry and authorised resend passes through the Section 8 checks | No notification attempt follows any final-response attempt for the case; no final-response attempt occurs while a notification is in flight |
| Routine and corrective updates | Answering ends routine generation under Section 9; corrective updates remain separately owed under Section 7 | A corrective update does not restart the routine chain |
| Descope ladder | Cut order is CSV export, provider recipients, unknown-acceptance flow, approval recommendations | Pre-registered contingency only; no rung is treated as removed until formally applied and reconciled throughout the specification |

### Superseded timing convention

An earlier draft cleared Investigation.completed_at on return or invalidation and created a fresh
final-response milestone on resubmission. That convention is withdrawn. No operational rule in the
current specification permits those actions to reset the final-response deadline.

---

# Appendix A — Specification

## Purpose

An internal complaints-management application for handlers and compliance reviewers in a small Irish insurance intermediary. It replaces spreadsheets and disconnected email with deadline tracking, independent approval of the final response, logged correspondence and an auditable history.

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
- revision (integer, default 1; incremented once for each return or invalidation that moves the
  case back to investigating)
- completed_at (timestamp, optional before first submission; set once at first submission and
  preserved through return, approval invalidation and resubmission)
- updated_at (timestamp)

First submission represents investigation completion under the adopted, unverified convention in
Section 5 and Appendix B.3. The prototype does not separately capture an earlier actual completion
date.

Once set, completed_at is not cleared or moved forward. Rework and further approval rounds preserve
the original final-response deadline.

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
- submitted_at (timestamp, required; records this approval round, not a new investigation-completion
  timestamp)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)

Each submission creates a new Approval row. Only the first submission sets
Investigation.completed_at and creates the final-response milestone. Later submissions preserve
both that timestamp and the original milestone due date.

A changed authorised final response requires a new Correspondence record. The earlier record,
authorisation timestamps and approval snapshot remain unchanged. A never-authorised draft may be
edited only under Section 10's draft-editing rule.

A pending approval with invalidated_at set is excluded from the reviewer queue.

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
- Editable only while draft, never authorised, and not the final_response_id of a non-invalidated Approval. An authorised final response is never edited; a change is a new row, and authorised_at is never cleared.
- Holds no approval reference and no milestone reference. Attempt history lives only in SendAttempt.

### SendAttempt

- id (integer, primary key)
- correspondence_id (foreign key to Correspondence, required)
- attempted_at (timestamp, required; time the attempt reservation was committed for provider
  submission, not proof that the external call began)
- result (text, required; validated against: pending, provider_accepted, failed,
  acceptance_unknown; initially pending)
- error_code (text, optional)
- error_detail (text, optional; excludes secrets)
- resolved_by_id (foreign key to User, optional)
- resolved_at (timestamp, optional)
- resolution (text, optional; validated against: confirmed_accepted, resend_authorised)
- resolution_note (text, optional; required when a resolution is recorded)

The attempt row is inserted and committed with result pending before the provider is called.
The result is subsequently recorded on that same row. The stale-send check changes an abandoned
pending attempt to acceptance_unknown without creating another attempt or resending.

An uncertainty resolution records its resolver, time, resolution and required note on the
uncertain attempt. A resend is a new SendAttempt on the same Correspondence record, not a new
correspondence record.

An authorised resend is available only for the latest uncertain attempt with
resolution = resend_authorised and no subsequent attempt. Creating that subsequent attempt
consumes the permission; no separate consumed flag is stored.

Per-attempt history lives here. The current-state fields attempt_count, last_attempted_at,
provider_reference and last_error live only on Correspondence.

The reservation, provider call, result update and late-result handling follow Section 10.
### Milestone
- id (integer, primary key)
- complaint_id (foreign key to Complaint, required)
- type (text, required; validated against: acknowledgement, progress_update,
  unresolved_notification, final_response)
- sequence (integer, required; orders progress updates within a case, is never reused, and a corrective update takes the next unused number)
- due_date (date, required)
- completed_correspondence_id (foreign key to Correspondence, optional; the only completion linkage,
  and only to a complainant-addressed message)
- completed_at (timestamp, optional)
- superseded_at (timestamp, optional; set when receipt correction replaces a receipt-derived milestone; never set by reviewer return or approval invalidation) 
- waived_at (timestamp, optional; set only at closure)
- waived_reason (text, optional; validated against: not_applicable, missed; required when waived_at
  is set)
- created_at (timestamp)
- Partial unique index on (complaint_id, type, sequence) where superseded_at is null. Superseded rows
  keep their type and sequence and remain readable; replacements reuse them.

The final-response milestone is created once, at first submission, from
Investigation.completed_at plus five working days. Receipt correction, reviewer return, approval
invalidation and resubmission leave this milestone and its due date unchanged. If a revised
final-response record is subsequently approved and accepted, it completes this same milestone.

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

| Method | Path                                     | Does                                                                                                                                                                                                                               |
| ------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | /login                                   | Show login form                                                                                                                                                                                                                    |
| POST   | /login                                   | Authenticate and start session                                                                                                                                                                                                     |
| POST   | /logout                                  | End session                                                                                                                                                                                                                        |
| GET    | /                                        | Dashboard with counts, milestones and urgent actions                                                                                                                                                                               |
| GET    | /complaints                              | List and filter authorised complaints                                                                                                                                                                                              |
| GET    | /complaints/export                       | CSV export of the filtered, authorised register, one row per case                                                                                                                                                                  |
| GET    | /complaints/new                          | Show intake form                                                                                                                                                                                                                   |
| POST   | /complaints                              | Create complaint, generate receipt-derived milestones, create acknowledgement draft                                                                                                                                                |
| GET    | /complaints/<id>                         | Show case, milestones, correspondence and audit                                                                                                                                                                                    |
| POST   | /complaints/<id>/investigation           | Save investigation draft; first save begins investigating; later edits preserve any existing completed_at and final-response due date                                                                                              |
| GET    | /complaints/<id>/receipt-correction      | Reviewer preview of affected receipt-derived milestones before correction; final-response deadline unchanged                                                                                                                       |
| POST   | /complaints/<id>/receipt-correction      | Reviewer correction with reason, supersession, completion carry-over and recalculation; refused on a closed case; final-response deadline unchanged                                                                                |
| POST   | /complaints/<id>/correspondence          | Create a controlled draft, including a replacement final-response draft where an authorised version must change                                                                                                                    |
| POST   | /correspondence/<id>/edit                | Edit a never-authorised draft only where Section 10 permits; never clear authorisation to enable editing                                                                                                                           |
| GET    | /correspondence/<id>/preview             | Preview recipient, subject, body and approval status                                                                                                                                                                               |
| POST   | /correspondence/<id>/send                | Confirm a non-final message or verify current valid final-response approval, persist, enforce Section 8 ordering, then attempt send                                                                                                |
| POST   | /correspondence/<id>/retry               | Retry a definite failure with unchanged content; recheck current final-response approval and Section 8 ordering                                                                                                                    |
| POST   | /correspondence/<id>/resolve-uncertainty | Record acceptance evidence or authorise a resend, with a required resolution note; every resulting attempt passes through the send service and Section 8 ordering checks                                                           |
| POST   | /complaints/<id>/submit-outcome          | Snapshot the package and create an Approval row; first submission alone sets completed_at and creates the final-response milestone; resubmission preserves the original timestamp and due date                                     |
| GET    | /approvals                               | Review queue of pending, non-invalidated approvals with ages and prior rounds                                                                                                                                                      |
| POST   | /approvals/<id>/decision                 | Approve or return the snapshotted package; a permitted return increments the investigation revision and preserves completed_at and the final-response milestone                                                                    |
| POST   | /complaints/<id>/return-to-investigation | Invalidate the live approval and increment the investigation revision; permitted only with no final-response attempt or where every attempt is a definite failure; preserve completed_at and the original final-response milestone |
| POST   | /complaints/<id>/close                   | Enforce Section 8 closure gates, record the day-40 outcome, waive remaining open milestones with enumerated reasons, and close                                                                                                     |
| GET    | /health                                  | Minimal health status without sensitive information                                                                                                                                                                                |
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
- No route changes roles; provisioning and deactivation are CLI operations that refuse to remove
  the last compliance reviewer or deactivate a handler with open cases.
- Operator-only CLI reassignment changes the handler without changing case milestones. It sits
  outside the application permission model and is audited.
- Receipt dates change only through the previewed, audited correction action, which supersedes and
  recalculates receipt-derived milestones, carries over a completed obligation and is refused on a
  closed case.
- Correspondence is editable only while never authorised, in draft, and outside an approval that
  prevents editing under Section 10. Authorisation permanently freezes content and is never cleared
  to enable an edit.
- A changed authorised final response is a new Correspondence record. Earlier authorised versions
  remain history and cannot be sent or retried without current valid approval.
- Approval applies to the final response only; the other three types are handler-confirmed at the
  /send POST.
- Comment mandatory on return, optional on approval; approver decisions are final, with no appeal,
  override or conditional approval; comment and submission note write-once after a decision.
- First submission sets Investigation.completed_at once and creates the final-response milestone at
  that timestamp plus five working days. Treating first submission as investigation completion is
  adopted, unverified, and disclosed in Section 5 and Appendix B.3.
- Reviewer return, approval invalidation and resubmission neither clear Investigation.completed_at
  nor supersede or replace the final-response milestone. The original deadline continues through
  review and rework, and remains overdue if it passes.
- A return or invalidation that moves the case to investigating increments the investigation
  revision once for that transition.
- Return-to-investigation is permitted only where the current final response has no attempt, or
  every attempt on it is recorded as a definite failure. It is refused while an attempt is sending,
  accepted or of unknown acceptance.
- Closure requires every gate in Section 8. The day-40 outcome is recorded in the closure
  transaction, and remaining open milestones are waived with an enumerated reason.
- Section 8's ordering rule applies to every send, retry and authorised resend. No unresolved
  notification attempt is permitted after any final-response attempt for the case, and no
  final-response attempt is permitted while an unresolved notification is in flight.
- Resolving uncertain acceptance is not itself a new attempt. Any resend resulting from that
  resolution must pass the same send-service checks.
- Provider acceptance is never described as delivery.
- All four message types are sent through the app with a recipient type and logged automatically.
- Templates are selected by message type and recipient type; mandatory content comes from
  Appendix B.
- Routine progress updates repeat before and after the 40-working-day point while applicable,
  without resetting the receipt date, resolution target or final-response deadline.
- Routine generation checks the answer date at every entry point and follows Section 9's
  generation stop and catch-up rules. Corrective updates follow Section 7's separate rule and do
  not create successors in the routine chain.
- Milestones are stored per obligation. Only a complainant-addressed message completes one, through
  Milestone.completed_correspondence_id, using Section 9's selection rule. Current deadlines derive
  from open, non-superseded milestones.
- Deadline calculation uses the Appendix B conventions, including the Good Friday and Easter Monday
  exclusions.
- Countdowns show label, exact date and text urgency. A return or resubmission never resets the
  final-response countdown.
- Outbound content is persisted before any send attempt. One confirmation produces one initial
  attempt, recorded individually in SendAttempt; retries and authorised resends are further
  attempts on the same correspondence record.
- Current-state send fields live only on Correspondence; per-attempt history lives only in
  SendAttempt.
- Approval linkage is held only in Approval.final_response_id. Correspondence holds no approval
  reference or milestone reference.
- Real sending is restricted server-side to allowlisted addresses; no unrestricted CC or BCC.
- Failed and uncertain sends remain visible and never complete milestones until acceptance is
  established.
- Unknown acceptance requires a recorded, audited resolution note. A resend is a new attempt on the
  same record; the scheduled check flags stale sending records and never resends automatically.
- Scheduled runs are idempotent per job and period, record failures, and a failed period is re-run
  by updating the existing row.
- CSV export respects record permissions, is one row per case, excludes narrative and contact
  detail, carries the fields and disclosed gaps described in Appendix B.5, and is audited.
- Synthetic data only; credentials from environment configuration, never in Git or AI tools.
- Scheduled work runs through a documented CLI command, not a web route.
- Deployment uses separate database owner and application roles; the audit table is protected by
  revoked UPDATE and DELETE for the application role.
- Retention is a documented policy only; no deletion feature is implemented.
- Dockerfile, deployment documentation, tests, scan evidence, ERD, DFD, STRIDE table, role table,
  GDPR write-up, limitations register, demo video and Git history are required deliverables.

## Out of scope

Excluded capabilities are listed in the single scope table in Section 3. Items marked Optional are
deferred, not excluded; items marked Out of scope are not delivered in this release.

---

# Appendix B — Regulatory requirements register

This appendix is the completion of Section 5 for every rule that drives code. Rows marked "adopted, unverified" are implemented as chosen interpretations and must be disclosed
as such. Rows marked "open" must be settled before the related logic is merged.

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
- Easter Monday is a public holiday under the 1997 Act and is excluded by the same rule. It must be
  seeded for every year, including years where it falls immediately after Good Friday.
- Every seeded calendar year must contain both Good Friday and Easter Monday. A test asserts their
  presence for each seeded year, so a truncated calendar cannot silently pass the worked examples.
- The public holiday set follows the 1997 Act, so the dataset must be dated and versioned.
- Weekends are excluded by definition, so no "if Saturday, roll to Monday" logic may exist.

### Worked examples

| Scenario                                                                           | Calculation                                                                      | Due                    |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------- |
| Received Thursday 22 October 2026; Monday 26 October is the October public holiday | Fri 23 = 1; Mon 26 excluded; Tue 27 = 2; Wed 28 = 3; Thu 29 = 4; Fri 30 = 5      | Friday 30 October 2026 |
| Received Wednesday 24 March 2027; Good Friday 26 March and Easter Monday 29 March 2027 | Thu 25 = 1; Fri 26 excluded; Mon 29 excluded; Tue 30 = 2; Wed 31 = 3; Thu 1 April = 4; Fri 2 April = 5 | Friday 2 April 2027 |

**Adopted, unverified:** whether the day of receipt counts as the first working day. The convention
adopted for the build: the clock starts on the next working day after receipt, matching both examples above. The
alternative must be acknowledged in the write-up.

## B.3 ## B.3 Obligations

| Obligation | Provision | Requirement | Implementation |
|---|---|---|---|
| Written procedure | Reg 105(1) | Procedure for managing and resolving complaints | Governance policy; not a system feature |
| Acknowledgement | Reg 105(4) | Written acknowledgement within 5 working days with procedure details, ombudsman information and contact details | Acknowledgement draft at intake; 5-working-day milestone; handler-confirmed |
| Named contact | Reg 105(4) | Point of contact until resolved or all steps exhausted | Handler recorded on acknowledgement and case |
| Progress updates | Reg 105(4)(d) | Regular written updates at intervals no greater than 20 working days from the date of receipt | Routine progress-update milestones from receipt + 20 working days; generation, completion and applicability follow Sections 8 and 9; corrective updates follow the separate internal rule in Section 7 |
| Reasonable efforts | Reg 105(4) | Investigate and make reasonable efforts to resolve within 40 working days | 40-working-day target and visible overdue position; the prototype's handling evidence does not by itself establish that reasonable efforts were made |
| Unresolved at 40 days | Reg 105(4) | Notify anticipated timeframe, referral right and ombudsman contact details | Unresolved-notification milestone with mandatory template fields; ordering and closure treatment follow Section 8, with late completion retained as evidence |
| Final response | Reg 105(4) | Within 5 working days of completion of the investigation: decision and reasons, offer or settlement terms, referral right and contact details | First submission sets Investigation.completed_at and creates the final-response milestone once; reviewer return, approval invalidation and resubmission preserve the original timestamp and due date |
| Early resolution | Reg 105(3) | Procedure need not apply where resolved to satisfaction within 5 working days, provided a record is kept | Normal journey retained; the record the prototype keeps is listed in Section 8 |

### Adopted, unverified completion convention

First submission for approval represents completion of the investigation. The prototype sets
Investigation.completed_at at that first submission and does not separately capture an earlier
actual completion date.

This is a chosen implementation convention, not a verified interpretation that internal submission
and actual investigation completion necessarily coincide. A delay between actual completion and
first submission is therefore not measured by the prototype's final-response clock.

### Deadline-preservation control

The original completion timestamp and final-response milestone are retained through reviewer return,
approval invalidation and resubmission. These events do not start a fresh five-working-day period,
and the original due date remains visible throughout rework and later approval rounds.

This replaces the earlier adopted restart convention. It is an internal control against repeatedly
refreshing the deadline, not a claim that the first-submission proxy is a verified regulatory
trigger.
## B.4 Mandatory template content

| Template | Mandatory content |
|---|---|
| Acknowledgement | Reference and date received; complaint as understood; procedure and expected timeframe; named contact; referral right and contact details |
| Progress update | Reference; what has been done; what remains; next expected update; named contact |
| Unresolved notification | Reference; not yet resolved; anticipated timeframe; referral right and contact details |
| Final response | Reference; decision and reasons; offer, redress or settlement terms; referral right and contact details; referral time limit where applicable |

Mandatory content attaches to the complainant-addressed template of each type. Templates are keyed by
message type and recipient type; provider and internal variants carry the reference, the request or
notice, the expected timeframe and the named contact, and no referral-rights block.

The ombudsman is the Financial Services and Pensions Ombudsman. Contact details are stored with the
template version so later changes do not retrospectively alter what was sent.

## B.5 Complaint log

Regulation 106 requires a complaint log. Mapping to the data model:

| Log field                           | Held in                                                                                                                                        |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Core reason or category             | `Complaint.category`, `Investigation.root_cause_category`                                                                                      |
| Date received                       | `Complaint.received_date`, with correction history in `AuditEvent`                                                                             |
| Summary of response and date        | Final-response `Correspondence`, `Investigation.outcome_rationale`                                                                             |
| Other correspondence                | All `Correspondence` rows with recipient type and timestamps                                                                                   |
| Steps taken                         | Investigation findings and the milestone sequence                                                                                              |
| Date the complaint was resolved     | `Complaint.closed_at` stands in for it. The true resolution date is the final response's `provider_accepted_at`; the prototype records closure |
| Ombudsman referral or appeal status | Not modelled; disclosed limitation                                                                                                             |
| Inbound correspondence              | Not captured; the application records outbound messages only, so inbound contacts are a disclosed limitation                                   |

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
| "Working day" | The 2025 term, with the Good Friday and Easter Monday exclusions |
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