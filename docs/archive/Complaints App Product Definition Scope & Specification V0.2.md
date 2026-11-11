# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.2 — 9 November 2026
Status: Proposed coursework baseline; regulatory rules require source verification before implementation.

## 1. Purpose

An internal web application for a small Irish regulated insurance intermediary. It manages complaints from receipt through investigation, independent approval, correspondence and closure. It replaces a spreadsheet and disconnected email process with a controlled case record, visible deadlines and an auditable history.

The application is intended to support complaint handling under the Consumer Protection Code 2025, effective from 24 March 2026. It is a coursework prototype, not a certified compliance product. Legal requirements and internal controls must be distinguished in the specification and tests.

The essential product is the combination of accurate deadline tracking, independent approval, correspondence sent through the application, and an audit trail. Advanced reporting is secondary.

## 2. Intended users and operating context

- One small Irish insurance intermediary, approximately 5–50 staff.
- Single organisation; no multi-tenancy.
- Complaints handlers investigate assigned cases.
- Compliance reviewers independently approve outcomes and final responses.
- Application administrators manage accounts and configuration.
- Complainants have no account and no public portal.
- All coursework records are synthetic. Real email is sent only to controlled test addresses.
- Desktop-first, with usable layouts on smaller screens.

The administrator role is an application permission boundary. A person with infrastructure or database credentials may have technical access outside the app. The prototype must not claim to prevent that access.

A representative stakeholder should validate the workflow where possible. Do not imply stakeholder validation has occurred unless it has.

## 3. Goals and non-goals

### Goals

1. Capture the actual receipt of a complaint accurately.
2. Calculate and display relevant deadlines using verified rules.
3. Guide the handler through investigation and outcome preparation.
4. Prevent self-approval and premature closure.
5. Send all normal outgoing case correspondence from the app and log it automatically.
6. Continue tracking and sending progress updates while a difficult complaint remains unresolved, including after the 40-working-day notification.
7. Preserve evidence of decisions, correspondence and changes.
8. Deliver a reproducible, tested, deployed application with documented limitations.

### Non-goals

- Public intake form, complainant login or self-service portal.
- Automated inbound email ingestion.
- Attachments, document uploads or document redaction.
- AI classification, summarisation or automated complaint decisions.
- Redress payment processing.
- CRM, policy administration or finance integrations.
- Multi-organisation operation.
- Configurable workflow designer.
- Full reporting suite or bespoke PDF generator.
- Claims of regulatory certification or guaranteed compliance.

## 4. Confirmed technical foundation

| Area | Baseline |
|---|---|
| Language | Python |
| Framework | Flask |
| Initial database | SQLite |
| Integration/deployment database | PostgreSQL |
| Containerisation | Docker; Docker Compose where useful |
| Version control | Git repository |
| Interface | Server-rendered pages; no separate frontend application |
| Deployment | Reachable deployed application; provider to be selected |

### Proposed supporting components

These are implementation candidates, not final selections: Jinja templates, SQLAlchemy/Flask-SQLAlchemy, Flask-Migrate/Alembic, Flask-Login, Flask-WTF, pytest, a small browser-test suite and Gunicorn. Select and justify tools before adoption.

Use a Flask application factory and separate modules for complaints, deadlines, approvals, correspondence and audit. Business rules should be testable independently of page rendering.

Introduce schema migrations from the start. Move to PostgreSQL early enough to run integration tests against the deployment database. Schema migration and transfer of existing records are different tasks; synthetic seed data may be recreated instead of transferred.

Run scheduled checks through a documented command invoked by an external scheduler. Hosting, scheduling, CSS framework and email provider remain open technical decisions.

## 5. Regulatory requirements register

Before implementing deadline rules, record the exact official source, interpretation, expected test examples and verification status for each requirement.

| Rule area | Intended behaviour | Verification requirement |
|---|---|---|
| Receipt | Capture actual receipt date/channel separately from record creation | Confirm relevant receipt conventions |
| Acknowledgement | Track the five-working-day acknowledgement point | Confirm counting and exceptions |
| Progress updates | Track updates at intervals no greater than 20 working days | Confirm applicable provision and timing anchor |
| Unresolved complaint | Track the 40-working-day point and required notification | Confirm content and trigger |
| Final response | Track notification within five working days of investigation completion | Confirm exact provision and definition of completion |
| Early resolution | Keep a log even when the shortened procedure applies | Confirm exception and required records |
| Working day | Exclude days according to the applicable legal definition | Verify holidays, non-working-day receipt and counting convention |
| Retention | Apply a defined record-retention policy | Verify applicable requirements before setting a period |

The 40-working-day point is a resolution target and communication/escalation point, not an automatic closure deadline. A complaint can remain active afterwards.

Independent approval of every final outcome is a chosen internal governance control; do not describe it as an express statutory requirement without supporting text.

Do not invent a late-Friday cut-off or treat an office closure as a statutory non-working day. Do not replace working-day calculations with calendar days as a shortcut.

The source register must be completed using the Central Bank regulations and relevant official guidance. Progress-update rules and final-response timing must be included, not deferred merely because the original concept omitted them.

## 6. Roles and access

| Role | Permitted activity | Restrictions |
|---|---|---|
| Handler | Create complaints; read assigned cases; investigate; prepare correspondence and outcomes; send authorised messages | Cannot approve own cases, alter locked receipt details or bypass closure gates |
| Compliance reviewer | Review cases; approve or return outcomes; authorise receipt corrections and reassignment | Cannot approve a case they handled; cannot silently alter the approved package |
| Application administrator | Manage accounts, roles and approved configuration | No routine access to complaint narrative or complainant details through the app |

No public registration. Accounts are provisioned administratively. Use separate test accounts for the roles and two handlers to demonstrate isolation.

Enforce permissions on server-side routes, service operations and data queries, not only in templates. Direct requests must be subject to the same checks. Database row-level security is an optional additional control, not a substitute for correct application authorisation.

Technical administrators, migrations and backups are documented privileged operations. Do not claim the audit trail is tamper-proof against the database owner.

## 7. Receipt capture and correction

Required intake information:

- Complainant name and controlled contact address.
- Actual received date; time if relevant to the verified rule.
- Channel: phone, email, letter, in person or other approved category.
- Receipt evidence/reference note, without attachments.
- Product/category and complaint description.
- Assigned handler.
- System-generated record reference and created-at timestamp.

The actual receipt date drives deadlines. It must not default silently to the day the handler enters the complaint.

After saving, the receipt date is locked for ordinary editing. A compliance-authorised correction requires a reason, records old and new values and triggers recalculation. Preserve the original deadline history so the correction does not erase evidence of earlier monitoring.

Reject future receipt dates. Validate contact information and required fields server-side.

## 8. Case lifecycle

### Main states

Logged → Investigating → Pending Approval → Approved/Awaiting Final Response → Closed.

A reviewer may return a proposed outcome to Investigating with a mandatory reason. A returned decision remains in the history.

Acknowledgement and progress updates are correspondence milestones, not separate case states. Deadline status is tracked independently of case state.

### Closure gates

A case may close only when:

1. Findings, root-cause category and outcome rationale are recorded.
2. A reviewer other than the handler has approved the current outcome and final-response package.
3. The approved final response has reached the defined successful-send status.
4. Any required unresolved-complaint notification or an explicit exception is accounted for.
5. Closure is audited.

A failed final-response send leaves the case awaiting final response. Provider acceptance is evidence of submission to the email service, not proof of delivery or legal sufficiency.

Changing the substantive approved outcome, redress, recipient or final-response content invalidates approval and requires resubmission. Freeze the approved message content to avoid ambiguity.

Closed case content is read-only. Retention deletion is a separate controlled operation. Reopening is deferred unless stakeholder validation shows it is essential; corrections must not silently rewrite history.

### Early resolution

Support a shortened path for early resolution, subject to verified eligibility. Record satisfaction evidence, outcome and correspondence. Retain independent approval as an internal control, with a lightweight workflow rather than omitting the complaint log.

## 9. Deadline engine and countdown UI

### Tracked milestones

- Acknowledgement due.
- Next progress update due.
- 40-working-day resolution target/unresolved-notification point.
- Final-response deadline following investigation completion.

Use verified calculation rules with explicit date conventions and the applicable holiday calendar. Store timestamps consistently and display them in Europe/Dublin local time. Working-day calculation must not use an arbitrary rolling 24-hour approximation.

### Display behaviour

Every countdown shows a milestone label, exact due date, working days remaining or overdue, completion status and the next permitted action.

Examples:

- “Acknowledgement due in 2 working days — [date]”.
- “Progress update due today”.
- “Acknowledgement overdue by 1 working day”.
- “40-working-day point passed — unresolved notification required”.
- “Acknowledged on [date] — within deadline”.

Show multiple active clocks when obligations overlap. Use text/icons as well as colour. A working-day countdown does not need a second-by-second timer.

Completed milestones retain their due date and actual completion timestamp. Countdown calculations must remain accurate even if the scheduled notification job has not run.

### Continued updates after day 40

The unresolved-at-40-days notification does not end the progress-update requirement or close the case.

For a prolonged case, support:

Acknowledgement → Progress update(s) → Unresolved-at-40-days notification → Further progress update(s) → Approved final response → Closure.

There is no fixed maximum number of progress updates. Each is its own logged message. The next update deadline follows the verified timing rule. Do not assume any email resets the clock: explicitly determine whether a particular message qualifies as an update. Preserve the distinction between a scheduled update and the day-40 notification even if a verified combined message satisfies both.

Sending a progress update must not reset the original receipt date, the 40-working-day target or the final-response deadline.

## 10. Correspondence through the app

### Controlled message types

1. Acknowledgement.
2. Progress update — repeatable before and after the 40-working-day point.
3. Unresolved-at-40-days notification.
4. Final response.

“Additional progress update” is another instance of the progress-update type, not a separate workflow or schema type.

All normal outgoing case correspondence is prepared, reviewed, sent and logged through the app. Manual logging of externally sent messages is outside the normal MVP workflow. Inbound telephone/email interactions can be summarised in case notes; there is no inbound mailbox integration.

### Message preparation

Use controlled templates with validated mandatory fields. Provide a preview showing recipient, subject, body and related milestone. Acknowledgements, updates and unresolved notifications require handler confirmation. Final responses require approval of the exact package before sending.

Staff notifications contain case IDs and links, not complaint narratives. Complainant correspondence necessarily contains appropriate substantive information; minimise it rather than enforcing an unusable “IDs only” rule.

### Outbox and send flow

Prepare → Preview → Confirm → Save immutable outbound snapshot → Attempt send → Record result.

Persist the message before invoking the email provider. Do not mark the corresponding milestone complete merely because a message was queued.

Store:

- Complaint reference and message type.
- Recipient and authorising user.
- Subject/body snapshot and template version.
- Approval reference where required.
- Created, attempted and provider-accepted timestamps.
- Status and provider reference.
- Failure information and retry history.

Model send attempts separately if needed to preserve retry evidence.

### Failure handling

Distinguish Draft, Queued, Sending, Provider Accepted, Failed and Delivery Unknown where appropriate. Do not call provider acceptance “delivered” or “read”. Delivery webhooks are a stretch goal.

Show failed messages in the case and operational queue. Retrying must reuse the authorised content and minimise duplicate sends. Where an attempt times out after possible provider acceptance, flag uncertainty rather than blindly resending. Use provider idempotency support if available.

For the MVP, provider acceptance may complete the operational send milestone, explicitly documented as a prototype limitation. If delivery failures become known, surface them for action rather than leaving the case looking unconditionally successful.

### Safe live demonstration

- Only allowlisted test recipients can receive messages.
- Enforce the allowlist in the server-side send service, not just the UI.
- Test the recipient after final address resolution; do not permit unrestricted CC/BCC.
- Use synthetic content and a clear demonstration notice.
- Keep API/SMTP credentials outside Git and AI prompts.
- Automated tests use a fake provider; a separate controlled test demonstrates real sending.

Build the outbox and fake transport first, then integrate real sending. Real sending is part of the intended finished MVP, not a replacement for testing failure paths.

## 11. Investigation, outcome and approval

Investigation records include findings, fixed root-cause category, rationale and completion timestamp. No guided 5 Whys, Fishbone or configurable RCA engine is required.

Outcomes: Upheld, Partially upheld, Not upheld. Record proposed redress, including zero where appropriate, and a rationale. Redress is recorded, not paid by the app.

The reviewer sees the investigation, outcome, redress and final-response preview. Approval and return decisions require comments. Approval must be checked at the time of decision and again before final-response sending/closure.

Use transactional state changes so a concurrent edit cannot bypass approval. A stale form should prompt a refresh rather than overwrite a newer decision.

## 12. Logical data model

| Entity | Purpose |
|---|---|
| User | Identity, role, activation and assignments |
| Complainant | Contact details held separately from case narrative |
| Complaint | Receipt details, handler, category, lifecycle and key milestone information |
| Investigation | Findings, root cause, completion and outcome proposal |
| Approval | Version-specific outcome/final-response decision |
| Correspondence | Immutable authorised outbound content and milestone association |
| SendAttempt | Send status, provider reference, retries and failures |
| AuditEvent | Actor, timestamp, action and relevant change history |
| PublicHoliday | Applicable dates and calendar metadata |

This is a logical model, not a fixed table-count target. Template configuration or deadline history may justify additional tables. Avoid adding tables solely to appear sophisticated.

Separating complainant details supports permissions but is not itself anonymisation. Correspondence and notes may also contain personal data.

## 13. Logical screens

### Dashboard

My open cases, acknowledgements due, next updates due, day-40 cases, final responses due, pending approvals and failed sends. Show urgent actions before aggregate charts.

### Complaint list

Reference, state, handler, received date and next action/deadline. Filters for state, handler where authorised, date range, category and overdue status. Only authorised records contribute to search results and counts.

### Intake

Clear required fields, explicit receipt date, contact validation, handler assignment and confirmation of calculated deadlines.

### Complaint detail

Header: reference, lifecycle state, handler and deadline panel.

Sections: summary, investigation, outcome/approval, correspondence, audit history. Show role-appropriate actions, while enforcing the same permissions server-side.

### Correspondence composer

Message type, controlled template, required fields, preview, allowlisted recipient, approval status and confirmation. Show send outcome and failures clearly.

### Approval queue

Pending cases, read-only proposed package, Approve/Return, mandatory comment and self-approval prevention.

### Configuration

Accounts, roles and carefully controlled holiday/template settings. Log configuration changes. Calendar changes must not silently rewrite existing compliance history.

Detailed visual design is deliberately left for the next UI specification.

### Responsive and mobile behaviour

The application is desktop-first but must adapt to mobile screens through
a responsive layout. This is one website, not a separate mobile application.

The main complaint journey must remain usable on mobile, including viewing
deadlines, recording investigation details, preparing and sending correspondence,
and performing authorised approval actions.

| Area | Mobile behaviour |
|---|---|
| Navigation | Collapse desktop navigation into a keyboard-accessible menu with a clearly labelled toggle. |
| Dashboard | Stack summary cards and deadline panels vertically, prioritising urgent actions. |
| Complaint list | Use compact cards or a simplified list showing reference, status, next deadline and next action. Do not squeeze every desktop column onto a narrow screen. |
| Complaint detail | Stack sections vertically. Keep the complaint reference, status and next deadline near the top. |
| Forms | Use a single-column layout with clear labels, usable controls and validation messages next to the relevant fields. Preserve entered values after validation errors. |
| Correspondence | Allow message preparation, preview and sending without page-level horizontal scrolling. Wrap long text and email addresses. |
| Approval | Make the investigation summary, outcome, redress and final-response preview available before confirmation. Do not hide essential review information on mobile. |
| Action buttons | Use comfortably spaced touch controls. Fixed or sticky controls must not obscure content, validation messages or keyboard focus. |
| Countdown indicators | Retain milestone labels, exact due dates and text-based urgency indicators. Do not rely on colour alone. |

Administrative configuration may be optimised for desktop, but it must remain
readable and navigable on smaller screens.

Native mobile applications, offline operation and push notifications are
outside the MVP scope.

## 14. Automations

| Type | Behaviour |
|---|---|
| Scheduled | Daily deadline/failed-send check and staff digest; include continuing updates after day 40 |
| Event-triggered | Complaint creation calculates milestones and creates the acknowledgement task/draft; successful correspondence updates relevant milestones |
| Human approval | Outcome/final-response submission enters a reviewer queue and blocks release until approved |

Do not automatically send substantive complainant correspondence simply because a timer fires. Monitoring prompts a human to review and send.

Scheduled processing should be safe to rerun without duplicate notifications. Record failures and last successful execution.

## 15. Security, privacy and operational requirements

- Authentication, password hashing, CSRF protection, secure session configuration and server-side validation.
- Authorisation on every protected request and record access.
- No credentials, real personal data or production secrets in Git or AI tools.
- Audit material changes, approvals, receipt corrections, correspondence attempts, account changes and relevant access denials.
- Separate operational logs from business audit evidence; avoid secrets and unnecessary narrative in logs.
- Append-only audit behaviour through the application, with documented infrastructure limitations.
- Synthetic coursework data only. Describe production legal basis and retention separately from demonstration data handling.
- Verified retention policy; no invented retention period. Configuration alone is not evidence of implemented deletion.
- Document backup/restore, access review, incident response, change control and ownership in the governance policy.
- Monitor health, application errors, scheduled-job failures and email-send failures.
- Accessible labels, keyboard navigation, focus visibility, contrast, error messages and non-colour status indicators. Review and report actual failures honestly.
- Deploy with persistent database storage and a documented recovery/redeployment route.

## 16. Success criteria established before build

1. Complete the normal intake-to-closure journey using separate handler and reviewer accounts.
2. Pass independently checked working-day and deadline examples, including holiday/year boundaries and verified non-working-day receipt rules.
3. Prevent cross-handler access through UI, direct URLs and crafted requests.
4. Prevent self-approval and unauthorised role changes.
5. Prevent closure without valid approval and final-response send evidence.
6. Invalidate approval when substantive approved content changes.
7. Audit receipt corrections and preserve previous values/deadlines.
8. Send real acknowledgement, updates, unresolved notification and final response only to allowlisted addresses, logging the actual content and results.
9. Support multiple progress updates after the day-40 notification without resetting the original target or closing the case.
10. Keep failed sends visible and avoid completing milestones on queueing or failure.
11. Preserve complaint data across application restart.
12. Recreate the application from a fresh checkout using documented Docker instructions.
13. Run automated tests and retain security-scan findings with remediation/acceptance evidence.
14. Complete the main journey with keyboard navigation and document remaining accessibility issues.
15. At a viewport width of 375 CSS pixels, users can navigate, read a complaint,
    check deadlines, complete essential forms, preview and send correspondence,
    and perform authorised approval actions without page-level horizontal
    scrolling or obscured controls.
16. Mobile layouts preserve the same permissions, mandatory fields, approval
    gates and confirmation steps as desktop layouts; no essential information
    or control is removed solely to fit a smaller screen.
17. Verify the main complaint journey at mobile, tablet and desktop viewport
    sizes, recording the results and any remaining responsive-layout limitations.

Commit this baseline before implementation. Record later changes and reasons rather than silently redefining success to match the finished app.

## 17. Test strategy

- Unit tests: working-day calculations, milestone anchors, repeat updates, state transitions and approval invalidation.
- Integration tests: persistence, permissions, transactional approval/closure and correspondence logging.
- Negative tests: self-approval, unauthorised receipt changes, cross-handler access and non-allowlisted recipients.
- Email tests: success, rejection, timeout/uncertain outcome, retry and duplicate prevention.
- Browser tests: one main end-to-end case and key blocked actions.
- PostgreSQL integration tests before final deployment; SQLite-only success is insufficient evidence for the deployed database.
- Security scans: select tools appropriate to source/dependencies/container/deployed app; triage findings and document fixes or accepted risks.
- Accessibility checks: automated checks plus keyboard/manual review.

Prioritise tests of the key controls over chasing an arbitrary coverage percentage.

## 18. Repository and assessment deliverables

- Source and meaningful incremental commit history.
- Schema migrations and synthetic seed data.
- Working Dockerfile and environment/deployment documentation.
- Example environment file containing placeholders only.
- Automated tests and documented commands.
- Security-scan output and remediation evidence.
- Deployed application with role-specific marker accounts supplied securely.
- Governance policy and operational runbook.
- Architecture/data model and relevant DFD/STRIDE evidence.
- Approximately 2,500-word technical write-up, Harvard references and required cover page.
- AI-usage log and AI Fluency declaration appendix.
- Live Week 12 demonstration and recommendation supported by observed results.

The assessment prohibits AI writing the design-decision analysis, security-findings discussion, accessibility review and limitations section. These assessed judgements must be the student's own work. This planning document is not a substitute for those sections.

## 19. Delivery approach and priorities

1. Commit scope, rule register and initial success criteria.
2. Establish repository, Flask skeleton, authentication and a minimal Docker build.
3. Implement/test receipt and deadline logic.
4. Deliver one persistent case journey with approval and audit.
5. Add outbox, fake email transport and repeated-update scheduling.
6. Integrate real allowlisted email and test failure/retry behaviour.
7. Move to PostgreSQL and prove deployment early.
8. Complete tests, scans, accessibility checks, monitoring and governance evidence.
9. Prepare the student's write-up and live demonstration; reserve contingency.

Actual submission is specified as end of Week 11, with a Week 12 demonstration. Confirm calendar dates against the approved timetable; 8 January is not treated as verified here.

Available hours are not yet confirmed. Plan conservatively around job and family commitments. Earlier effort percentages and precise delivery-risk estimates were informal judgements, not reliable forecasts. Re-estimate after the first working slice.

Protect approval, audit, deadline correctness, correspondence evidence and assessment deliverables. Cut advanced reporting, visual embellishments, configurable template editing and delivery webhooks first.

## 20. Open decisions before implementation

- Exact verified legal provisions and deadline-counting examples.
- Hosting and persistent PostgreSQL service.
- Email provider, controlled recipients and handling of uncertain sends.
- UI framework and visual design.
- Authentication/account recovery approach and optional MFA.
- Approved holiday calendar source and update process.
- Retention requirement and what retention functionality the prototype implements.
- Whether the separate earlier project brief remains an additional checklist alongside CA2.
- Confirmed timetable and sustainable weekly effort.

## 21. Reference and evidence register

Primary coursework source: MCLCD_Oct26_CA2_LowCodeNoCodeAIDev.docx, supplied assessment brief, read 9 November 2026. This specifies repository, testing, Docker, deployment, governance, accessibility, AI declaration and live-demo requirements.

Additional supplied source: Low-Code-No-Code-Project-Brief.pdf. Confirm its status alongside CA2; preserve the earlier ERD, automation, access-control, DFD, STRIDE and GDPR planning where applicable.

Official regulatory sources to verify and record by exact provision:
- Central Bank of Ireland, Consumer Protection Code 2025.
- Central Bank of Ireland, General Consumer Protection Requirements, complaints-handling provisions.
- Central Bank of Ireland, Investment Firm and Intermediary Newsletter, June 2026.

This is a planning baseline, not legal advice or a claim that all regulatory interpretations have already been verified.


## Appendix A - Specification

# Specification

## Purpose

An internal complaints-management application for handlers and compliance reviewers in a small Irish insurance intermediary. It replaces disconnected spreadsheets and email with deadline tracking, independent outcome approval, automatically logged correspondence and an auditable case history.

## Entities

### User
- id (integer, primary key)
- name (text, required)
- email (text, required, unique)
- password_hash (text, required; never store plaintext passwords)
- role (one of: handler, compliance, admin)
- active (boolean, default true)
- created_at (timestamp)

### Complainant
- id (integer, primary key)
- name (text, required)
- email (text, required; controlled test address in the prototype)
- phone (text, optional)
- created_at (timestamp)

### Complaint
- id (integer, primary key)
- reference (text, required, unique, system-generated)
- complainant_id (foreign key to Complainant)
- handler_id (foreign key to User)
- received_date (date, required; locked after creation)
- received_time (time, optional)
- received_channel (one of: email, phone, letter, in_person, other)
- receipt_note (text, required)
- product (text, required)
- category (text, required)
- description (text, required)
- status (one of: logged, investigating, pending_approval,
  approved, closed — default logged)
- acknowledgement_due (date, calculated)
- next_update_due (date, calculated)
- resolution_target_due (date, calculated)
- final_response_due (date, optional, calculated when applicable)
- closed_at (timestamp, optional)
- created_at (timestamp)
- updated_at (timestamp)

### Investigation
- id (integer, primary key)
- complaint_id (foreign key to Complaint, unique)
- findings (text, optional while drafting)
- root_cause_category (text, optional while drafting)
- outcome (one of: upheld, partially_upheld, not_upheld;
  optional while drafting)
- outcome_rationale (text, optional while drafting)
- redress_amount (decimal, non-negative, default 0)
- completed_at (timestamp, optional)
- revision (integer, default 1)
- updated_at (timestamp)

### Approval
- id (integer, primary key)
- complaint_id (foreign key to Complaint)
- investigation_revision (integer, required)
- final_response_id (foreign key to Correspondence)
- reviewer_id (foreign key to User)
- decision (one of: pending, approved, returned — default pending)
- comment (text, required when a decision is recorded)
- decided_at (timestamp, optional)
- invalidated_at (timestamp, optional)
- created_at (timestamp)

### Correspondence
- id (integer, primary key)
- complaint_id (foreign key to Complaint)
- message_type (one of: acknowledgement, progress_update,
  unresolved_notification, final_response)
- recipient_email (text, required before sending)
- subject (text, required before sending)
- body (text, required before sending)
- template_version (text, required)
- status (one of: draft, queued, sending, provider_accepted,
  failed, delivery_unknown — default draft)
- authorised_by_id (foreign key to User, optional until authorised)
- authorised_at (timestamp, optional)
- provider_accepted_at (timestamp, optional)
- created_at (timestamp)
- Content becomes immutable once authorised; revisions require
  a new draft and, for final responses, renewed approval.

### SendAttempt
- id (integer, primary key)
- correspondence_id (foreign key to Correspondence)
- attempted_at (timestamp)
- result (one of: provider_accepted, failed, unknown)
- provider_reference (text, optional)
- error_code (text, optional)
- error_summary (text, optional; exclude secrets)

### AuditEvent
- id (integer, primary key)
- complaint_id (foreign key to Complaint, optional for account/configuration events)
- actor_id (foreign key to User, optional for system actions)
- action (text, required)
- change_details (structured data, optional; minimise personal data)
- created_at (timestamp)
- Append-only through the application.

### PublicHoliday
- id (integer, primary key)
- date (date, required, unique within the supported calendar)
- name (text, required)
- calendar (text, required)

## Routes

| Method | Path | Does |
|---|---|---|
| GET | /login | Show login form |
| POST | /login | Authenticate and start session |
| POST | /logout | End session |
| GET | / | Show role-appropriate dashboard, countdowns and urgent actions |
| GET | /complaints | List and filter authorised complaints |
| GET | /complaints/new | Show complaint intake form |
| POST | /complaints | Create complaint and calculate deadlines |
| GET | /complaints/<id> | Show authorised case details, deadlines, correspondence and audit history |
| POST | /complaints/<id>/investigation | Save investigation draft and begin investigation |
| POST | /complaints/<id>/receipt-correction | Compliance-only receipt correction with reason, audit and deadline recalculation |
| POST | /complaints/<id>/assign | Compliance-only handler reassignment with audit |
| POST | /complaints/<id>/correspondence | Create a controlled correspondence draft |
| POST | /correspondence/<id>/edit | Update an editable draft |
| GET | /correspondence/<id>/preview | Preview recipient, subject, body and authorisation status |
| POST | /complaints/<id>/submit-outcome | Validate investigation and final-response draft; request independent approval |
| GET | /approvals | Show compliance review queue |
| POST | /approvals/<id>/decision | Approve or return the current outcome and final-response package |
| POST | /correspondence/<id>/send | Authorise where permitted, persist outbox record and attempt sending |
| POST | /correspondence/<id>/retry | Retry a failed message where safe, without changing authorised content |
| POST | /complaints/<id>/close | Validate approval and final-response send evidence; close and audit |
| GET | /admin/users | Show account-management screen |
| POST | /admin/users | Create an account |
| POST | /admin/users/<id>/update | Update role or activation status with audit |
| GET | /admin/holidays | Show holiday configuration |
| POST | /admin/holidays | Add a verified holiday entry with audit |
| GET | /health | Return minimal application health status without sensitive information |

## Technical constraints

- Python and Flask, with supported versions pinned in the repository.
- SQLite for initial development; PostgreSQL for integration testing
  and deployment.
- SQLAlchemy/Flask-SQLAlchemy for database access and Alembic-based
  migrations for schema changes.
- Flask application factory with separate business-rule modules.
- Jinja templates; no separate JavaScript frontend framework.
- Responsive, desktop-first interface supporting the main journey
  at 375 CSS pixels without page-level horizontal scrolling.
- Working authentication, password hashing, CSRF protection and
  server-side input validation.
- Role and record permissions enforced on every protected request,
  including direct requests that bypass the UI.
- Handlers access assigned cases only; compliance reviewers cannot
  approve cases they handled.
- Application administrators manage configuration without routine
  access to complaint content.
- Closed case content is read-only; authorised receipt corrections
  preserve previous values and deadline history.
- All final outcomes require independent approval.
- Substantive changes to approved content invalidate approval.
- Closure requires valid approval and provider-accepted final-response
  evidence; provider acceptance must not be labelled as delivery.
- Acknowledgement, progress updates, unresolved notifications and final
  responses are sent through the app and logged automatically.
- Progress updates are repeatable before and after the 40-working-day
  point; they do not reset the original resolution target.
- Deadline calculations use verified regulatory rules and the applicable
  working-day calendar.
- Show separate countdowns, exact due dates and textual urgency indicators
  for active milestones.
- Save outbound message content before attempting real sending.
- Real sending restricted server-side to allowlisted test addresses;
  unrestricted CC/BCC is not supported.
- Failed or uncertain sends remain visible and do not silently complete
  correspondence milestones.
- Synthetic complaint data only; credentials supplied through environment
  configuration and excluded from Git and AI prompts.
- Scheduled deadline checks run through a documented Flask CLI command,
  not an unauthenticated web route.
- Dockerfile, deployment instructions, persistent database configuration,
  automated tests, scan evidence and meaningful Git history required.
- Test deadline boundaries, permissions, approval gates, repeated updates,
  email failures and the main browser journey.
- Maintain AI-use evidence, operational monitoring and a governance policy.
- Exact regulatory interpretations, tool versions and deployment provider
  must be verified or selected before their implementation.

## Out of scope

- Public complaint intake, public registration and complainant accounts.
- Automated inbound email ingestion.
- Attachments and document uploads.
- AI-generated case decisions, classification or summarisation.
- Redress payment processing.
- CRM, policy administration and finance integrations.
- Multi-organisation support.
- Configurable workflows or a full template editor.
- Advanced analytics and bespoke PDF reporting.
- Native mobile applications, offline operation and push notifications.
- Delivery/read tracking webhooks in the initial MVP.
- Routine manual logging of correspondence sent outside the app.
- A general case-reopening workflow.
- Regulatory certification or a guarantee of legal compliance.