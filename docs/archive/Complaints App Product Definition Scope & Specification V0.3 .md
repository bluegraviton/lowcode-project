# Complaints Register and Case Manager
## Product Definition and Scope

Version: 0.3 — 9 November 2026
Status: Minimum assessed release defined; optional enhancements are not delivery commitments.

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

### Release priorities

The minimum assessed release is defined by Section 16.1. It includes the
supporting testing, security, deployment, governance and assessment work,
not just the application features.

Features listed in Section 16.2 are optional enhancements. They must not
delay the minimum release or reduce the time reserved for testing,
security remediation, documentation and demonstration preparation.

Where an earlier description suggests a broader capability, the minimum
release boundary in Section 16 takes precedence. Optional features must
not be represented as implemented until they have been built and tested.

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

| Role                      | Permitted activity                                                                                                              | Restrictions                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Handler                   | Create complaints; read assigned cases; investigate; prepare correspondence and outcomes; send authorised messages              | Cannot approve own cases, alter locked receipt details or bypass closure gates  |
| Compliance reviewer       | Review cases; approve or return outcomes and final responses.<br>Receipt correction and reassignment are optional enhancements. | Cannot approve a case they handled; cannot silently alter the approved package  |
| Application administrator | Manage accounts, roles and approved configuration                                                                               | No routine access to complaint narrative or complainant details through the app |

No public registration. Accounts and roles are provisioned through documented CLI/seed procedures in the minimum release. Browser-based account administration is optional. Use separate test accounts for the roles and two handlers to demonstrate isolation.

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

After saving, the receipt date is read-only in the minimum release.
There is no correction interface or correction endpoint.

An authorised receipt-correction workflow, including reasons, historical
values and deadline recalculation, is an optional enhancement.
The prototype must explicitly disclose this limitation and must not
silently alter receipt dates through ordinary editing.

Reject future receipt dates. Validate contact information and required fields server-side.

## 8. Case lifecycle

### Main states

Logged → Investigating → Pending Approval → Approved/Awaiting Final Response → Closed.

A reviewer may return a proposed outcome to Investigating with a mandatory reason. A returned decision remains in the history.

Acknowledgement and progress updates are correspondence milestones, not separate case states. Deadline status is tracked independently of case state.

### Closure gates

A case may close only when every one of the following gates is satisfied.
This list is the single definition of the closure gates.

1. Findings, root-cause category, outcome, outcome rationale and redress
   amount are recorded for the current investigation revision. This is
   validated when the outcome is submitted and revalidated at closure.

2. A reviewer other than the handler has approved the current investigation
   revision and the exact final-response content now held.

3. That approved final response has reached provider-accepted status, and no
   subsequent change has invalidated the approval.

4. Either the complaint was approved and its final response sent before the
   40-working-day point, or an unresolved-at-40-days notification has reached
   provider-accepted status before closure.

5. The closure is recorded as an audited state transition by a user authorised
   to close the case.

Gate 4 requires a notification only where approval and final-response sending
did not both occur before the 40-working-day point. Where they did, gate 4 is
satisfied without a notification.

Gate 4 does not excuse late notification. A notification sent after the
40-working-day point satisfies the gate but leaves the overdue milestone and
its escalation visible in the case history.

The minimum release models no discretionary closure exception. An exception
field would permit closure without evidence of a required notification and
cannot be validated against a verified rule. If a verified rule later permits
an alternative, it must be added here and to Section 16.1 criterion 5 together.

Consequently, a case that genuinely requires an alternative handling path
cannot be closed in the minimum release. This is a disclosed prototype
limitation, not a gap to be worked around with a free-text field.

A failed final-response send leaves the case awaiting final response. Provider
acceptance is evidence of submission to the email service, not proof of
delivery or legal sufficiency.

Changing the substantive approved outcome, redress, recipient or
final-response content invalidates approval and requires resubmission. Freeze
the approved message content to avoid ambiguity.

Closed case content is read-only. Retention deletion is a separate controlled
operation. Reopening is deferred unless stakeholder validation shows it is
essential; corrections must not silently rewrite history.

### Early resolution

The minimum release uses the normal investigation, independent approval
and final-response journey even when a complaint is resolved quickly.

It records the outcome and evidence of satisfaction where relevant.
A separate expedited workflow is optional.

Regulatory exceptions must still be understood and documented; deferring
a separate interface does not justify making inaccurate compliance claims.
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

Minimum implementation: attempt sending through one provider, record the
result, allow controlled retries for definite failures and require manual
review of uncertain outcomes.

Background workers, automated retry scheduling, delivery webhooks and
provider reconciliation are optional. No separate queue infrastructure
is required for the minimum release.

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

Validate the current state and approval on the server inside the relevant
database transaction. Lock proposal fields during review and after approval.

Use a simple revision/version check to reject stale updates that could
overwrite a newer proposal or bypass approval. A sophisticated merge or
editing-conflict interface is not required.

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

The model records the evidence each closure gate requires. It deliberately
contains no discretionary closure-exception field.
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

The minimum release has no browser-based configuration screens.

Provision users through documented CLI/seed commands, store templates in
version control and load a verified holiday dataset through a documented
procedure. Keep secrets in environment configuration.

Browser-based user, holiday and template management are optional enhancements.

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

## 16. Success criteria and release priorities

### 16.1 Minimum assessed release — committed scope

These criteria define the smallest complete application intended for submission.
They are established before implementation and must be supported by test
results, demonstration evidence or documented operational procedures.

#### A. Complete complaint journey

1. Using separate handler and compliance accounts, complete:
   intake → investigation → outcome submission → independent approval
   → final-response sending → closure.

2. Record the actual receipt date and channel separately from the
   system-generated creation timestamp. Reject future receipt dates.
   The receipt date is read-only after creation in the minimum release.

3. Record findings, a root-cause category, an outcome, an outcome rationale
   and any proposed redress. Validate required information before submission.

4. Allow the reviewer to approve or return the proposal with a comment.
   A returned proposal becomes editable by the handler again.

5. Enforce every closure gate defined in Section 8. Refuse closure with a
   specific, visible reason for each unmet gate. Evidence must show the
   refusal when any single gate fails. A failed or uncertain send must not
   close the complaint.

#### B. Authentication, permissions and record integrity

6. Provide working authentication and server-side permissions.
   Handler A must not read or modify Handler B's complaint through either
   the interface or a direct request.

7. Prevent self-approval. Provide no public registration or user-accessible
   route for changing one's own role.

8. Lock the proposed outcome and final-response content while awaiting
   approval and after approval. Changes require an explicit return to
   investigation, invalidation of the approval and resubmission.
   Closed case content is read-only.

9. Automatically record case creation, state transitions, approval decisions
   and correspondence attempts in an audit history that cannot be edited
   through the application.

#### C. Deadlines and countdowns

10. Calculate acknowledgement, progress-update, unresolved-complaint and
    final-response milestones using verified rules. Pass a documented set
    of independently checked examples covering ordinary dates, weekends,
    applicable holidays and a year boundary.

11. Display the applicable milestones on the complaint detail page with
    their exact dates and working days remaining, due-today or overdue
    status. Do not rely on colour alone.

12. Support repeated progress updates before and after the 40-working-day
    notification. Updating the next progress-update deadline must not
    reset the original receipt date or resolution target.
    Test a synthetic prolonged case with at least two further updates
    after the unresolved notification.

#### D. Real, automatically logged correspondence

13. Prepare, preview and send acknowledgement, progress-update,
    unresolved-notification and final-response messages through the app.
    Use fixed, version-controlled templates rather than a template editor.

14. Restrict all real sends to server-side allowlisted test addresses.
    Log the recipient, actual subject/body, authorising user, timestamps
    and send result. Store the outbound record before attempting sending.

15. Distinguish provider acceptance, definite failure and uncertain outcome.
    Do not describe provider acceptance as delivery.
    Failed or uncertain sends remain visible and do not complete milestones.

16. Provide a controlled retry for definite failures using unchanged
    authorised content. Do not automatically retry uncertain sends.
    Test failure behaviour using a fake email provider and demonstrate
    real sending separately to controlled addresses.

#### E. Usable interface and scheduled monitoring

17. Provide a dashboard, authorised complaint list, intake form,
    complaint-detail view and approval queue.
    Use basic counts and deadline indicators rather than advanced reports.

18. Make the main complaint journey usable by keyboard and at a mobile
    viewport width of 375 CSS pixels, without page-level horizontal
    scrolling or hidden essential controls.
    Retain identical permission and approval rules across screen sizes.
    Record observed accessibility or layout failures honestly.

19. Provide a documented scheduled deadline check that generates a staff
    digest containing case references and links rather than narratives.
    Record successful execution and failures. Re-running the check must
    not send duplicate digests for the same scheduled period.

#### F. Persistence, deployment and assessment evidence

20. Preserve data across application restarts. Run the deployed application
    with PostgreSQL and demonstrate a documented Docker-based setup from
    a fresh repository checkout.

21. Supply passing automated tests covering deadline rules, permissions,
    self-approval prevention, closure gating and correspondence failures.
    Test the main journey against PostgreSQL before submission.

22. Run appropriate security scanning, retain the results and record the
    response to findings. Keep secrets out of source control and AI prompts.

23. Provide the required repository, deployment instructions, governance
    policy, operational monitoring evidence, privacy/accessibility review,
    AI-use log, declaration, technical write-up and live demonstration.
    These are minimum delivery commitments, not optional enhancements.

### 16.2 Optional enhancements — only after the minimum release is stable

The following are not required to declare the minimum application complete:

- A receipt-correction interface with authorisation, reasons, historical
  deadline preservation and recalculation.
- Handler reassignment with an audit trail and historical conflict checks.
- Browser-based account and role administration.
- Browser-based holiday-calendar administration.
- A dedicated early-resolution workflow.
- Delivery/bounce webhooks and reconciliation with the email provider.
- Automated retry queues, background workers and provider idempotency integration.
- Advanced search, reporting, charts and exports.
- Editable correspondence-template administration.
- Broader automated browser coverage and additional device/browser testing.
- Additional responsive optimisation beyond the core complaint journey.

Optional status does not remove a security requirement. If an enhancement
is implemented, its permissions, validation, audit behaviour and tests
must be included.

### 16.3 Minimum-release implementation choices

- Provision users and roles through documented CLI/seed procedures.
- Use a verified holiday dataset covering the declared test and demonstration
  period, including dates needed for deadlines that extend into the next year.
- Keep templates in version control.
- Use a simple email-send service without a background queue.
- Use the normal approval journey for early-resolved complaints; do not
  implement a separate expedited workflow in the minimum release.
- Provide no receipt-edit or reassignment route in the minimum release.
- Correct erroneous synthetic test cases by creating a new case through
  the documented test procedure, not by silently rewriting history.
- Preserve the approved message and outcome; do not implement unrestricted
  editing followed by automatic detection of substantive changes.

### 16.4 Baseline and change control

Commit this revised baseline before implementation and retain the previous
version in Git. Explain that the revision reduces scope to protect delivery
of a complete assessed application.

Later changes must record the reason, impact and priority. Do not silently
redefine success criteria to match whichever features happen to be finished.

Begin optional enhancements only after the minimum journey is deployed,
its key tests pass, correspondence works, and time has been reserved for
the remaining assessment deliverables.

## 17. Test strategy

- Unit tests: working-day calculations, milestone anchors, repeat updates, state transitions and approval invalidation.
- Integration tests: persistence, permissions, transactional approval/closure and correspondence logging.
- Closure-gate tests: one negative test for each unmet gate in Section 8 —
  missing findings, missing or stale approval, missing final-response send,
  unauthorised closure — plus a missing-notification test where approval and
  final-response sending did not both occur before the 40-working-day point.
- Closure success tests: one positive closure after all gates pass, and one
  case approved and closed before day 40 with no notification sent.
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


# Appendix A - Specification

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
- The admin role is retained for provisioning and future configuration. The minimum release provides no browser-based administration interface.

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
- received_date (date, required; read-only after creation in the minimum
  release; audited correction is an optional enhancement)
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
- queued and sending are transient states within a single request;
  no background worker is part of the minimum release.

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

| Method | Path                            | Does                                                                          |
| ------ | ------------------------------- | ----------------------------------------------------------------------------- |
| GET    | /login                          | Show login form                                                               |
| POST   | /login                          | Authenticate and start session                                                |
| POST   | /logout                         | End session                                                                   |
| GET    | /                               | Show role-appropriate dashboard, countdowns and urgent actions                |
| GET    | /complaints                     | List and filter authorised complaints                                         |
| GET    | /complaints/new                 | Show complaint intake form                                                    |
| POST   | /complaints                     | Create complaint and calculate deadlines                                      |
| GET    | /complaints/<id>                | Show authorised case details, deadlines, correspondence and audit history     |
| POST   | /complaints/<id>/investigation  | Save investigation draft; reused after a reviewer return                      |
| POST   | /complaints/<id>/correspondence | Create a controlled correspondence draft                                      |
| POST   | /correspondence/<id>/edit       | Update an editable draft                                                      |
| GET    | /correspondence/<id>/preview    | Preview recipient, subject, body and authorisation status                     |
| POST   | /complaints/<id>/submit-outcome | Validate investigation and final-response draft; request independent approval |
| GET    | /approvals                      | Show compliance review queue                                                  |
| POST   | /approvals/<id>/decision        | Approve or return the current outcome and final-response package              |
| POST   | /correspondence/<id>/send       | Authorise where permitted, persist outbox record and attempt sending          |
| POST   | /correspondence/<id>/retry      | Retry a failed message where safe, without changing authorised content        |
| POST   | /complaints/<id>/close          | Enforce every closure gate in Section 8; close and audit                      |
| GET    | /health                         | Return minimal application health status without sensitive information        |

### Optional routes

Receipt correction, handler reassignment and browser-based account/holiday
administration are deferred. Their proposed routes are not part of the
minimum implementation.

| Method | Path                                | Does                                                                             |
| ------ | ----------------------------------- | -------------------------------------------------------------------------------- |
| POST   | /complaints/<id>/receipt-correction | Compliance-only receipt correction with reason, audit and deadline recalculation |
| POST   | /complaints/<id>/assign             | Compliance-only handler reassignment with audit                                  |
| GET    | /admin/users                        | Show account-management screen                                                   |
| POST   | /admin/users                        | Create an account                                                                |
| POST   | /admin/users/<id>/update            | Update role or activation status with audit                                      |
| GET    | /admin/holidays                     | Show holiday configuration                                                       |
| POST   | /admin/holidays                     | Add a verified holiday entry with audit                                          |



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
- Reject future receipt dates and validate all required intake fields
  server-side.
- Role and record permissions enforced on every protected request,
  including direct requests that bypass the UI.
- Handlers access assigned cases only; compliance reviewers cannot
  approve cases they handled.
- Users and roles are provisioned through documented CLI/seed procedures.
  Administrative credentials do not grant complaint access through the app.
- Receipt dates and closed case content are read-only in the minimum release. An audited receipt-correction workflow is optional.
- All final outcomes require independent approval.
- Proposed content is locked while pending approval and after approval.
  Editing requires an explicit return to investigation, invalidation of
  approval and resubmission.
- Closure requires every gate in Section 8, including recorded findings and,
  where the complaint remained unresolved at the 40-working-day point, an
  unresolved-notification with provider-accepted status. Provider acceptance
  must not be labelled as delivery.
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
- Users are provisioned through CLI/seed procedures; holidays are loaded
  from a verified dataset and templates are version-controlled.
- The minimum implementation uses one email provider without a background queue. Definite failures support controlled retry; uncertain outcomes require review before any resend.
- No separate expedited early-resolution workflow is provided; early-resolved
  complaints use the normal investigation, approval and final-response journey.
- Section 16.1 defines the committed release. Entity definitions may support
  future enhancements without committing their interfaces to this release.

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
- - Optional enhancements listed in Section 16.2 are conditional, not committed scope. Their absence from this release is a documented limitation, not a claim that they are unnecessary in production.