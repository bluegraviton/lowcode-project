# Build Addendum and Plan — A1.1

**Applies to:** Complaints App Product Definition, Scope & Specification **V0.8** (frozen).
**Version:** A1.1 — 11 November 2026
_ARCHIVED. Superseded by Core Spec V1.0 and Build Plan V1.0. Retained only as a design reference for stretch items. Do not edit and do not give to the builder in full.”_ Archive Addendum A1.1 the same way.

## 0. How to use this document

1. **Precedence.** Where this document and V0.8 disagree, **this document wins**. Where it is silent, V0.8 applies unchanged.
2. **V0.8 is frozen.** Never edit, rewrite or "reconcile" V0.8. All later decisions are recorded here (Section 5 change log), in the decision log and in the limitations register.
3. **Reading order for the builder.** Read this document first, then use V0.8 as the reference for rules, entities, routes and tests. Rule IDs (R-…), permission IDs (P-…) and entity IDs (E-…) in V0.8 remain the identifiers to use.
4. **Stop and ask.** If this document and V0.8 conflict in a way not covered here, or a rule is ambiguous, stop and ask the project owner. Do not guess, and do not change V0.8.
5. **Size limit.** If this document grows beyond about six pages, the project is being re-specified. Cut it back or move content into the limitations register.

The purpose of the project is to show that the app is built, works, has working automations, is tested, and has its security and data protection evidence. Edge cases beyond the rules below are handled by being disclosed, not by more specification.

---

## Part A. Addendum (overrides V0.8)

**A-01 Day-40 meaning.** Gate 4(a) in R-CLOSE-01 stays as written: the case is answered in time only if the final response reaches `provider_accepted` on or before the 40-working-day due date. This is a deliberately conservative reading of "resolve" and is stricter than the final-response milestone, whose due date (`completed_at` plus five working days) can fall after day 40. No gate logic changes. The countdown display must show both dates, and where the final-response due date falls after the unresolved-notification due date it must add the text: "Day-40 notification still required unless the final response is accepted by day 40."

**A-02 Meaning of "breach" and late notification.** "Breach" in V0.8 Section 2.3 and criterion 4 means gate 4(c) only. Outcome (b) means "notification accepted before the outcome" (an ordering outcome); it does not mean the notification was on time. Add a **derived** `notification_late` indicator (Europe/Dublin date of the notification's `completed_at` is after its `due_date`), shown on the case page and, if CSV export is built, as a CSV column. It is not stored, so no schema change.

**A-03 Return sets `invalidated_at`.** A reviewer return (`decision = returned`) also sets `invalidated_at` on that Approval in the same transaction. A *live* approval is one that is pending or approved with `invalidated_at` null. A returned approval is therefore not live, the never-authorised final-response draft is editable again under V0.8 Section 6.5, and the return-edit-resubmit loop works.

**A-04 Resend route.** `POST /correspondence/<id>/retry` accepts either (i) a definite failure, or (ii) the latest uncertain attempt carrying an unconsumed `resend_authorised` resolution (Tier 2). Both pass through the same send service, approval check and ordering checks. `/send` is for the initial send only.

**A-05 Final-response draft before submission.** The final-response draft (complainant-addressed) must exist before `submit-outcome`. It is created with `POST /complaints/<id>/correspondence`, and the investigation screen links to the composer. Submission validation adds: "an unauthorised complainant-addressed final-response draft exists for this case". On resubmission after a return the same draft is edited; if the earlier record was authorised, a new record is created (V0.8 Section 6.5).

**A-06 Closure and corrective updates.** Closure does not require a corrective update to have been sent. A corrective update not yet due at closure is waived as `not_applicable` under V0.8 Section 4.4. This is accepted as a disclosed limitation (L-18).

**A-07 Simplified send flow (Tier 1).** Keep: the committed `pending` SendAttempt before the provider call; the result recorded afterwards on the same row, only if it is still pending (R-SEND-06); complaint-then-correspondence row locking; the stale-send check turning stale `sending` into `acceptance_unknown` without resending; the allowlist; the ordering rule R-ORDER-01; retry of definite failures only.
Defer to Tier 2: `resend_authorised` and the permission-consumption logic.
Tier 1 resolution supports **`confirmed_accepted` only**, by a compliance reviewer on any type. Handler resolution of non-final types is Tier 3.

**A-08 Routine progress-update generation.** Generation entry points are **message completion and the scheduled check only**. Page-render catch-up (R-MILESTONE-05) is Tier 3. No GET request writes data. The generation function itself is unchanged, including the stop-at-answer rule (R-MILESTONE-03) and catch-up for obligations that fell due before the answer. Accepted limitation: between scheduled runs a successor routine milestone may not yet exist (L-16). The demonstration triggers the scheduled check to show later updates (day 80 and beyond) being created.

**A-09 Receipt correction (Tier 2, first item).** Minimal version: reviewer-only preview and apply; mandatory reason; audit of old and new values; supersede and recreate receipt-derived milestones; carry over completion; refuse on a closed case; final-response milestone untouched. **Corrective-update creation is Tier 3.** Until it is built, the preview and case page display a notice: "The acknowledgement already sent quotes the original receipt date; send a progress update with the corrected date." The handler then sends an ordinary progress update. Demonstration steps 2–3 use this manual update.

**A-10 Criteria are met "to the extent built".** A criterion element that depends on a Tier 2 or Tier 3 item not built is recorded in the limitations register and the write-up rather than delivered. Criteria 2 and 6 are the most affected. Criteria 7 to 14 are Tier 1 and are not to be traded away.

**A-11 Tests follow the build.** Write tests only for what is built. Do not leave skipped or failing tests for unbuilt features. Delete the corresponding parts of the V0.8 test groups. Every test names the rule ID it verifies.

**A-12 STRIDE.** The STRIDE table is completed with real threat IDs (S-01, S-02, …) by the end of slice S5 at the latest, one row per boundary-crossing flow in the DFD. Tests that implement a code mitigation carry the threat ID (suggested: `@pytest.mark.stride("S-03")`). Policy or configuration controls carry no tag and are listed against the control instead.

**A-13 Descoping procedure replaces V0.8 Section 11.6.** The V0.8 ladder (D-01 to D-04) is superseded by the tiers in Part B. The V0.8 requirement to reconcile a descope "throughout the specification" is **waived**. A descope is recorded by one decision-log line and one limitations-register entry (Part C), nothing more.

**A-14 Internal recipient type is Tier 3.** Build recipient types `complainant` and, in Tier 2, `provider`. The `internal` recipient type and its templates are not built unless time allows. The staff digest is separate and remains Tier 1.

---

## Part B. Build plan

### B.1 Tiers

| Tier | Items | Rule |
|---|---|---|
| **1 — Must build** | Auth, roles, CSRF, sessions; audit with database revocation; working-day module and holiday calendar; intake, milestones, countdown; investigation, final-response draft, snapshot approval, return and resubmission; correspondence with templates, allowlist, simplified send flow, milestone completion, ordering rule, stale-send check; closure gates, day-40 outcome, waivers; scheduled check, digest and `ScheduledRun`; dashboard and complaint list; ERD, role table, DFD, STRIDE, GDPR write-up, tests, scans, Docker, accessibility review, demo | Code slices S0 to S5 complete before any Tier 2 work starts; S6 is evidence work and does not block Tier 2 |
| **2 — Build in this order if time allows** | (1) Receipt correction, minimal (A-09). (2) CSV export. (3) `resend_authorised` and resend via `/retry`. (4) Provider recipient type and templates | Start only when the S0 to S5 checklists in B.3 are fully ticked; must be finished by the feature freeze |
| **3 — Skip unless well ahead** | Corrective updates; internal recipient type; page-render catch-up; handler resolution of non-final messages; approval recommendations; any Optional item in V0.8 Section 11.3 | Each needs the owner's decision |

**Time-box rule.** If a slice or Tier 2 item overruns its share of the time, do not extend it. Move it down a tier, record the limitation (Part C) and carry on.

### B.2 Tier 1 build slices

Build in this order. Do not start a slice until the previous one's "done" checklist is ticked. **S0 to S5 are code slices. S6 is evidence and documentation and runs after the feature freeze.**

**Join-point rule.** Each slice adds new feature folders. It may edit earlier code only at the defined join points: `config.py`, the FEATURES list, new migrations, and calls to another feature's public service functions. A slice must not restructure or rewrite an earlier slice's folders. If it appears to need that, stop and ask.

| Slice | Content |
|---|---|
| **S0 Baseline** | Hosting decision and monitoring tool recorded; decision log started; DFD draft; STRIDE skeleton; repository, Flask application factory, Docker Compose with PostgreSQL owner and application roles; single configuration module for enumerations and tunables; test runner; first scan |
| **S1 Foundations** | User model; login, logout, CSRF, secure cookies, idle expiry; role checks in services; audit service; revocation of UPDATE and DELETE on the audit table with its test; `provision-user` CLI |
| **S2 Deadlines and intake** | Holiday calendar dataset (Good Friday and Easter Monday per seeded year, with the test); pure working-day module with both Appendix B.2 worked examples; Milestone model; **Correspondence model (draft state only, no sending) and the acknowledgement draft created at intake**; intake route and form; complaint list and detail; countdown display per A-01 |
| **S3 Investigation and approval** | Investigation save; final-response draft (A-05, using the Correspondence model from S2); `submit-outcome` with snapshot and hash; first submission sets `completed_at` and creates the final-response milestone once; approval queue and decision; return and invalidation (A-03); state transitions; investigation locked outside `logged` and `investigating` |
| **S4a Sending core** | Templates keyed by type and recipient; composer and preview; allowlist; fake transport; SendAttempt and the simplified send flow (A-07); milestone completion on acceptance (R-MILESTONE-01, -02) |
| **S4b Send safeguards** | Ordering rule (R-ORDER-01); retry of definite failures; stale-send check; `confirmed_accepted` resolution |
| **S5 Closure and automations** | Closure service with gates, day-40 outcome and waivers (R-CLOSE-01 to -03); routine generation per A-08; scheduled check CLI, `ScheduledRun` and idempotent digest; dashboard; STRIDE table completed (A-12) |
| **S6 Evidence** | ERD and data dictionary generated from the models; role table; DFD final; scans re-run and findings recorded; accessibility review; 375 px check; GDPR write-up; limitations register final; demo video; submission pack |

### B.3 "Done" checklist for every slice

- [ ] Tests for the slice pass against PostgreSQL.
- [ ] Every rule ID touched has a test that names it.
- [ ] Every state change, denial and send writes an audit event.
- [ ] New boundary-crossing flows have STRIDE rows (from S2 onward).
- [ ] Limitations register and decision log updated (Part C routine).
- [ ] Committed in small commits; AI-assisted code flagged in the commit message.
- [ ] Application starts from a clean checkout with Docker Compose.

### B.4 Mapping to V0.8 checkpoints

The V0.8 course-week checkpoints (Section 11.5) stand; confirm the actual dates against the timetable.

- **Baseline commit:** S0 complete.
- **Week 9:** S0 to S5 complete (Tier 1 code demonstrable end to end), real sending proven or sandbox fallback adopted. Tier 2 starts here, with receipt correction first, or is consciously dropped.
- **Week 10, feature freeze:** Tier 2 work ends, finished or not. Whatever is unfinished becomes a limitation. Tests and scans are green. Regenerate the ERD and data dictionary after the last migration.
- **Week 11:** S6 evidence and documentation complete, submission pack finished.
- **Week 12:** demonstration.

---

## Part C. Maintaining the limitations register

### C.1 Routine (two minutes at the end of every slice)

1. Did I skip, simplify or defer anything from V0.8 or this document? If yes, add a register entry.
2. Did I make a decision a marker would ask about (an interpretation, a trade-off, a tier change)? If yes, add one decision-log line.
3. Re-read the open entries: is any now wrong because I built the thing after all? If yes, delete or amend it.

### C.2 Entry format (one line each)

`L-nn | What is missing or simplified | Why | Effect on the user or the compliance position | Source (V0.8 section, addendum item or tier)`

Keep entries **factual**. Do not analyse them. The analysis of limitations is the student's own work for the write-up and must not be written by the AI.

Decision-log line format: `Date | Decision | Reason | Consequence`.

### C.3 Numbering and pre-filled entries

V0.8 Section 10.4 items 1 to 11 stand. New entries are numbered from **L-12**.

**Certain from the start (add now):**

| ID | Entry |
|---|---|
| L-12 | Gate 4(a) (answered by day 40) is stricter than the final-response milestone due date, which can fall after day 40 (A-01). |
| L-13 | A late unresolved notification accepted before the final response is outcome (b), not a breach; lateness is shown by a derived indicator (A-02). |
| L-14 | V0.8 is frozen and amended by Addendum A-n; the descope reconciliation requirement was waived (A-13). |
| L-15 | Only `confirmed_accepted` resolution exists in Tier 1; an uncertain message waits for a compliance reviewer. |
| L-16 | Later routine progress-update milestones are created on message completion and by the scheduled check, not on page render (A-08). |
| L-17 | Day-40 and final-response clocks are driven by the adopted, unverified conventions in V0.8 Section 11.11. |
| L-18 | Closing before a corrective update falls due waives it as `not_applicable` (A-06). |

**Add only if the item is not built:**

| If this is not built | Add an entry stating |
|---|---|
| Receipt correction | Receipt dates cannot be corrected in the application; a mistyped date can only be fixed by the operator, outside the permission model |
| Corrective update (Tier 3) | No corrective update is generated after a correction; the handler sends an ordinary progress update after reading the notice |
| CSV export | The Regulation 106 log fields are viewable on screen only; no export |
| `resend_authorised` | An uncertain message cannot be resent through the application; it can only be confirmed accepted |
| Provider recipient type | No correspondence is sent to the insurer; any insurer contact happens outside the application; the insurer remains in the DFD as a considered external entity with no application flow |
| Internal recipient type | No internal staff notices are sent through the outbox; only the staff digest exists |
| Handler resolution of non-final messages | An uncertain acknowledgement waits for a compliance reviewer |
| Approval recommendations | A return carries only the mandatory comment |
| Page-render catch-up | (Already covered by L-16) |

If an item is built, no entry is needed. If it is built only in part, describe the missing part.

---

## Part D. Rules for the AI builder

### D.1 Principle

Build so that a feature can be added, changed or removed later by touching **one folder and one registration line**. Achieve this with plain structure, not frameworks. V0.8's over-engineering guardrail still applies: **no plugin registry, no dependency-injection container, no event bus, no configuration-driven workflow, and no abstraction before two call sites.**

### D.2 Structure: one folder per feature

```
app/
  __init__.py        # application factory; ONE explicit FEATURES list
  config.py          # all enumerations, status values, tunables
  core/              # database setup, authentication helpers, audit service,
                     # permission helpers, clock, shared errors
  deadlines/         # pure functions only; no database access
  features/
    auth/
    complaints/      # intake, list, detail
    investigation/
    approvals/       # submission, queue, decision, return
    correspondence/  # templates, composer, send service
    milestones/
    closure/
    automations/     # scheduled check, digest, ScheduledRun
    export/          # Tier 2
  cli.py             # provision-user, deactivate-user, reassign-handler, deadline-check
migrations/
tests/               # cross-cutting tests only (security, PostgreSQL, negative access)
```

Each feature folder contains `routes.py`, `services.py`, `models.py`, `templates/`, `tests/` and a `register(app)` function. The factory calls each feature's `register`. **Removing a feature means deleting its folder and its line in the FEATURES list.**

### D.3 Dependency rules

1. Dependencies run **routes → services → models**. Routes validate input and delegate. Services hold business rules and transactions. Models hold persistence. No rule logic in routes or templates.
2. A feature may call another feature only through that feature's public `services` module, never its models or internals. Shared code lives in `core/`.
3. No circular imports. If two features need each other, move the shared piece into `core/` or the owning feature's services.
4. `deadlines/` takes dates and returns dates. It never touches the database or the clock.
5. Routes never write an entity directly. The named service writes inside a transaction (V0.8 Section 3.2).
6. **No GET request writes data.**
7. One configuration module holds every enumeration and tunable. No string literals for statuses, types or roles in logic.

### D.4 Schema and data rules

1. **Every schema change goes through an Alembic migration.** Generate, then review by hand. No manual DDL against any database.
2. The **models and migrations are the single source of truth.** The ERD and a data dictionary (table, column, type, constraint, purpose) are **generated** from the models and regenerated whenever a migration is added. Do not draw them by hand.
3. Enumerations are validated text columns (V0.8 Section 7), validated in the service layer; CHECK constraints are encouraged where cheap.
4. Foreign keys, uniqueness and NOT NULL rules are expressed in the database, not only in code.
5. Seed data is synthetic, versioned and loaded by a documented command.
6. The audit table revocation is applied through the owner role in the migration or setup script, and has a test.

### D.5 Code quality rules

- Small functions with one job; type hints on public functions; short docstrings that cite the rule ID they implement (for example `# R-ORDER-01`).
- A single `now()` function in `core/` (the clock) used everywhere, so tests can set the time. This is the only permitted clock mechanism.
- Services own the transaction boundary: one commit point per service call; the send service's two-transaction pattern is the only exception.
- Explicit, specific errors; no silent `except`; denials raise a typed error that the route maps to the right response **and** writes an audit event.
- No secrets in code, logs, tests or prompts. Credentials come from the environment.
- No dead code, no speculative hooks, no features "for later". Delete rather than comment out.
- Dependencies: add one only if it removes more code than it adds.

### D.6 Checklist: adding a feature

1. Confirm it is in the current tier and slice; if not, ask the owner.
2. Create `features/<name>/` with routes, services, models, templates and tests.
3. Add its migration; regenerate the ERD and data dictionary.
4. Add its permission rows to the role table and enforce them in the service.
5. Add its audit events.
6. Add STRIDE rows for any new boundary-crossing flow.
7. Add its test(s), naming the rule IDs.
8. Add its single line to the FEATURES list.
9. Update the limitations register and decision log (Part C).

### D.7 Checklist: removing a feature

1. Delete the feature folder and its line in the FEATURES list.
2. Add a migration only if data or columns must go; otherwise leave the schema alone and note it.
3. Remove its tests, permission rows, STRIDE rows and screens.
4. Add the register entry from C.3 and a decision-log line.
5. Run the full test suite. Do not edit V0.8.

### D.8 Testing and Git

- Write tests **alongside** each slice, not afterwards. Fake email transport in automated tests; one separate controlled real-send check.
- The full suite runs against PostgreSQL.
- Small commits; one slice per branch; commit messages say what changed and flag AI-assisted code ("AI-assisted").
- Do not weaken or delete a test to make a build pass; raise it instead.

### D.9 Prompt header (paste at the start of every build session)

> You are building the Complaints App. Read **Build-Addendum-and-Plan** (latest version) first, then use **Specification V0.8** as reference. The addendum overrides V0.8. Do not edit V0.8. Work only on the current slice: **[slice]**. Follow Part D: one folder per feature, routes → services → models, deadline functions pure, all enumerations in `config.py`, migrations for every schema change, no GET writes, tests alongside, rule IDs cited in tests and comments. Do not add features outside the current tier. If anything is ambiguous or the documents conflict, stop and ask me. At the end, list: what you built, what you skipped or simplified, and any limitation or decision I should record.

---

## 5. Change log

| Version | Date | Change |
|---|---|---|
| A1 | 11 November 2026 | Initial addendum, build plan, limitations routine and builder rules. V0.8 frozen. |
| A1.1 | 11 November 2026 | Tier 2 now starts after code slice S5 (S6 is post-freeze evidence work); Correspondence model and acknowledgement draft moved into S2; S4 split into S4a and S4b; join-point rule added. |
