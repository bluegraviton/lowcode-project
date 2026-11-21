# Limitations register

Format: `L-nn | what is missing or simplified | why | effect on the user or compliance position | source`. Entries are factual. Source references are to Core Spec V1.3 (CS) and Build Plan V1.3 (BP).

| ID | What is missing or simplified | Why | Effect | Source |
|---|---|---|---|---|
| L-01 | No stakeholder validation has taken place | No review with a complaints handler or similar has been held yet | Requirements and workflow are unconfirmed by a user. Replace this entry if a real review happens | CS 1.1; BP 9.3 |
| L-02 | Day-of-receipt exclusion and first-submission completion proxy are adopted conventions | Not yet confirmed against the regulation (verification rows V-09 and V-10) | Calculated deadlines may differ from the regulatory reading if either convention is wrong | CS 4, 5 (R-DATE-02), 11 |
| L-03 | Only the log-only transport exists unless ST-4 is built | Real email is a stretch item | "Sent" means recorded in the outbox. Nothing is emailed, delivered or read | CS 6, 12 |
| L-04 | Receipt date cannot be corrected in the application unless ST-1 is built | The receipt date is locked after intake (SC-03); correction is a stretch item | A mistyped receipt date stays wrong, and deadlines calculated from it stay wrong | CS 7, 12 |
| L-05 | Reviewer-shopping: any compliance user may decide a resubmission | Decisions are not tied to the reviewer who returned the case | The reviewer who returned a package can also approve its resubmission | CS 4 |
| L-06 | No reviewer cover; single-value roles | Each user holds exactly one role | Approval cannot proceed while no reviewer is available | CS 3 |
| L-07 | Handler absence leaves no cover unless ST-7 is built | Reassignment is a stretch item | Cases assigned to an absent handler cannot be reassigned in the application | CS 12 |
| L-08 | Inbound correspondence is not captured | Inbound email is out of scope | Complainant replies are not part of the case record or outbox | CS 1.6, 6 |
| L-09 | Ombudsman referral status is not modelled | It is not in the data model | The case record cannot show whether a complainant has referred the complaint | CS 7 |
| L-10 | Regulation 107 analysis is out of scope | Six-monthly pattern analysis is excluded from the core build | No pattern analysis is available | CS 1.6 |
| L-11 | Retention period unverified; no deletion feature | Six years from closure is proposed (V-12 unverified) and automated deletion is out of scope | Records are kept with no deletion; the period is not confirmed | CS 1.6, 10.3, 11 |
| L-12 | Correction and erasure conflict with immutable messages, approval hashes and the audit table | Sent messages, approved content and audit entries are immutable by design | Correction and erasure are manual operator actions that conflict with those records | CS 10.3 |
| L-13 | Day-40 outcome (a) is stricter than the final-response milestone due date; outcome (b) is an ordering outcome and lateness is a derived indicator | The final-response due date can fall after day 40 | Outcome (b) does not show the notification was on time; the case page shows a separate lateness indicator | CS 4 (R-CLOSE-02) |
| L-14 | No password reset or MFA; login throttling only if ST-2 is built | Listed as not planned or stretch | Forgotten passwords need operator action; repeated login attempts are not throttled | CS 12 |
| L-15 | Anyone with database or hosting credentials can read data outside the application | The CLI and operator access run outside the application permission model | Application role checks do not limit operators | CS 3.2, 10.1 |
| L-16 | Closed cases cannot be reopened and no discretionary closure exists | Reopening is out of scope; closure only through the gates | A case closed in error cannot be reopened in the application | CS 1.6, 4 |
| L-17 | Template wording is short placeholder text and has not had legal or compliance review | Templates are deliberately short and generic | Letters are marked "DEMONSTRATION — wording not legally reviewed" and are not fit for real use | CS 6 |
| L-18 | Until M1, audit entries are protected by application code only; database-level revocation exists from M1. Delete this entry when M1 is done | SQLite has no roles or privilege revocation | SC-06 is not met until M1. Not a limitation of the delivered build | CS 9.1; BP 7.3 |
