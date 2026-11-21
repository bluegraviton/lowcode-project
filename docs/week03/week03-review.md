


# Week 3 — AI Code Review

Reviewed by: ChatGPT - GPT-6.2 Sol  Date: 18/11/2026

## Findings

The existing test suite passed all 34 tests. I found one current usability issue, two gaps in the test suite, and two security limitations relevant to deployment. I made no source changes.


| #   | Priority             | Location                                                                                                                                                                                                 | Finding                                                                                                                                                                                                                                                                                                                                        |
| --- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Medium · Security    | [complaints/routes.py (line 10)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/routes.py:10)                                                                   | Anyone who can reach `/` can view every complaint row, including complainant names. This is intentional for S0’s synthetic data. Connecting the route to real records as written would expose them without authentication or authorization.                                                                                                    |
| 2   | Medium · Correctness | [complaints/services.py (line 33)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/services.py:33)                                                               | A single unrecognized product, category, or status raises `KeyError` and causes the entire complaints page to return HTTP 500. The checked-in fixtures contain valid values. The failure becomes relevant when the repository starts reading persisted records.                                                                                |
| 3   | Low · Usability      | [base.html (line 7)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/templates/base.html:7)                                                                                          | The locally served app depends on jsDelivr for all styling. When the CDN is blocked or unreachable, the page loses its styling and the table loses its narrow-screen scrolling behavior. The integrity hash matches the Bootstrap 5.3.8 stylesheet. [Bootstrap CDN documentation](https://getbootstrap.com/docs/5.3/getting-started/download/) |
| 4   | Low · Security       | [README.md (line 13)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/README.md:13), [README.md (line 41)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/README.md:41) | Both run commands enable Flask’s interactive debugger. The Windows instructions point to loopback. Reusing either command on a network-facing server would make the debugger reachable from outside the machine.                                                                                                                               |
| 5   | Low · Structure      | [test_complaints_services.py (line 11)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/app/features/complaints/tests/test_complaints_services.py:11)                                    | The test checks that each label belongs to the right set of labels. It would still pass if the service displayed “Closed” for every complaint. It never checks the label against the corresponding record.                                                                                                                                     |
| 6   | Low · Test coverage  | [test_no_get_writes.py (line 9)](C:/Users/blueg/lowcode-project/complaints-app/complaints-app-S0/tests/test_no_get_writes.py:9)                                                                          | The no-write test silently skips every GET route with a path parameter. It covers the current complaint index and health check, but a future route such as `/complaints/<id>` could mutate data without failing this test.                                                                                                                     |


## What I fixed, and why

- **#4 — Debug mode.** I added a README note that says `--debug` is for local use only. This makes clear that the run command is for development, since exposing Flask’s interactive debugger on a network-facing server is a security risk.
- **#5 — Complaint labels.** I updated the test to check the product, category, and status labels against each complaint’s record. The old test could pass even if every complaint was shown as “Closed,” because “Closed” is a valid label.
- **#6 — GET route coverage.** I added a test that fails if a GET route with a path parameter is added without updating the no-write check. This makes the coverage gap visible when a route like `/complaints/<id>` is added.

## What I am knowingly leaving, and why

- **#1 — Public complaints list.** S0 uses made-up complaints, so the public list exposes no real complaint data. Login is planned for S1.
- **#2 — Unknown labels.** All S0 sample records use valid product, category, and status values. I’ll revisit how to handle unknown values when the app starts reading stored records.
- **#3 — CDN dependency.** The S0 brief calls for a pinned Bootstrap CDN URL. If the CDN is unavailable, the complaint data still shows, but the page loses its styling and the table may overflow on small screens. That trade-off is acceptable for S0.

## What the reviewer got wrong

To be honest, I am later in the course than expected when running this. There are several reasons for this; one was settling on a project and the other was a lack of time as I started a new job. When I did settle on a project (the complaints app) I went through significant iterations scoping it out. In the end I had a massive prescriptive document that tried to cover every edge case that might arise in my app. This before building anything. Thankfully, I realised this was over-scoped and well beyond the limits of what could be done with the available time in this course. I then cut the scope of the project significantly. 

However, I still had a very detailed Scope and staged Build Plan. At this point we had already started to cover some SQL in the course and it was obvious that the initial build, suitable for Week 3 should avoid SQL. As a result, when I finally came to building my initial build, I gave Claude a comprehensive, though reduced spec, a comprehensive stagged build plan and a detailed prompt asking Claude to build stage zero (S0) avoiding databases and just using synthetic data. 

The result of this, I believe, was a tightly controlled S0 which ran first time successfully and required minor adjustment before moving to S1.