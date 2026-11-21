# Decision log

Format: `date | decision | reason | consequence`.

| Date | Decision | Reason | Consequence |
|---|---|---|---|
| 11 November 2026 | Database staged: sample data (S0), then SQLite (S1 to S2b), then PostgreSQL at M1 | Follows the lecturer's instruction to start with SQLite; the delivered build needs PostgreSQL | Three data stages; the suite is re-run unchanged on PostgreSQL at M1 |
| 11 November 2026 | Repository layer chosen so each switch of data store changes one file per feature | Keeps routes, services and templates unchanged between stages | Only `repository.py` files import the data store; a test enforces this for the sample data in S0 |
| 11 November 2026 | PostgreSQL required for the delivered build | SQLite has no database roles or privilege revocation, and ignores row locks | SC-06 and R-SEC-03 can only be built and proven at M1; M1 cannot be cut or pushed past S3 |
| 11 November 2026 | Deployment deferred from S0 to D1, and D1 moved to after M1 | Local-first development; the hosted database test needs PostgreSQL | S0 deploys nothing; hosting is researched in S0 and deployed at D1 in week 8 |
| 11 November 2026 | AWS adopted as the working hosting assumption pending the lecturer's hosting sessions; claims to verify before M1 | The course is expected to cover hosting later; AWS is the provider researched in S0 | Claims listed in `evidence/deployment/hosting-options.md` must be checked by the end of week 7; no AWS account until about week 7 |
