# Hosting options (slice S0)

Purpose: record the working hosting assumption and the claims still to verify before step M1 (end of week 7). Nothing is deployed, no account exists and no infrastructure code has been written.

**Method.** Notes were gathered on 11 November 2026 from secondary sources. On 18 November 2026 the AWS pages listed under "Sources" were opened and checked. Every statement below is labelled **verified in source** (read on an AWS page, URL given) or **unverified** (everything else, including the secondary-source notes). Prices and limits not on those pages are deliberately not stated.

## 1. Working assumption

AWS, pending the lecturer's hosting sessions. Provisional shape (unverified as a whole):

| Need (Build Plan 3.1; Core Spec 9.1, 10.1) | Option under consideration |
|---|---|
| Run a Docker container of the Flask app | Amazon ECS Express Mode, image pushed to Amazon ECR |
| PostgreSQL with an owner role and a restricted application role | Amazon RDS for PostgreSQL, or Amazon Aurora PostgreSQL serverless |
| Scheduled CLI job (daily `deadline-check`) | Amazon EventBridge Scheduler starting an ECS task |
| Monitor logs and health | Amazon CloudWatch Logs; load balancer health check on `/health` |

AWS App Runner is not an option: it is closed to new customers. Other providers have not been researched. If AWS fails any claim below, Build Plan 3.1 says to stop and choose another host before building S3.

## 2. What is already known

- App Runner is closed to new customers, and AWS recommends ECS Express Mode instead. **Verified in source** [1]. The date 30 April 2026 is **unverified** (not on that page).
- Express Mode deploys a container image from a registry such as Amazon ECR, and creates an ECS service on Fargate, an Application Load Balancer with health checks, auto scaling and networking. **Verified in source** [1]. There is no extra charge for Express Mode itself; the underlying resources are charged. **Verified in source** [1].
- Express Mode sends container logs to CloudWatch Logs, and its log groups never expire and survive deletion of the service unless changed. **Verified in source** [2]. The health check path can be set to `/health`. **Verified in source** [2].
- Express Mode provides HTTPS on its default URL. **Unverified.** (A custom domain needs a certificate in AWS Certificate Manager. **Verified in source** [1].)
- New accounts (activated on or after 15 July 2025) get up to $100 in credits at sign-up and can earn up to $100 more, and the Free plan runs for up to 6 months. **Verified in source** [3]. That the extra $100 is earned by using Amazon RDS: **verified in source** [4].
- Aurora PostgreSQL serverless is on the Free plan (up to 4 ACU and 1 GiB storage per cluster) [3], announced 25 March 2026 [4]. RDS for PostgreSQL on db.t3.micro and db.t4g.micro is on the Free plan. All **verified in source**.
- On RDS and Aurora PostgreSQL the master user can create roles and use GRANT and REVOKE. **Verified in source** [5]. That this supports our exact need (application role denied UPDATE and DELETE on the audit table) is **unverified**; it is tested at M1 and again at D1.
- EventBridge Scheduler has a templated target for ECS RunTask, supports the Fargate launch type, and a schedule can have a time zone. **Verified in source** [6]. That it can run the Express Mode service's image as a one-off task: **unverified**.
- Fargate does not scale to zero, so an always-running service has a monthly cost floor. **Unverified** (from notes).
- Advice: do not create the AWS account until about week 7, because the Free plan is time-limited [3] and credits could run out before marking. The Free plan limit is **verified in source**; the risk to marking is **unverified**.

## 3. Claims still to verify in AWS's own documentation

- [ ] **Free plan scope.** Which services the Free plan allows: ECS Fargate, Application Load Balancer, ECR, RDS or Aurora, EventBridge Scheduler, CloudWatch. What happens when credits run out or at 6 months (does the account close or convert). Check https://aws.amazon.com/free/free-tier-faqs/.
- [ ] **Two database roles.** On the chosen database, as the master user create an owner role and an application role; `REVOKE UPDATE, DELETE` on a table from the application role; confirm the application role gets "permission denied". Confirm the application role cannot create or alter schema objects (the DDL test), including the default privileges on the public schema for the PostgreSQL version chosen.
- [ ] **Database choice.** RDS db.t4g.micro versus Aurora serverless: supported PostgreSQL versions, whether Aurora pauses when idle, and the cost once credits end.
- [ ] **Scheduled job.** EventBridge Scheduler starting an ECS task from the same image with a command override for `deadline-check`; whether Express Mode's task definition can be reused or a separate one is needed; the IAM role Scheduler needs; time zone set to Europe/Dublin; retry settings.
- [ ] **Logs and health.** Where the web service's and the scheduled task's logs appear in CloudWatch Logs; a retention period chosen for the log groups; a CloudWatch alarm on unhealthy targets for `/health`.
- [ ] **HTTPS and URL.** Whether the default Express Mode URL is HTTPS; whether the marker can reach it without a custom domain.
- [ ] **Secrets.** How the database credentials are passed to the container (environment, Secrets Manager) without entering Git or logs.
- [ ] **Cost floor.** Minimum task count for Express Mode, hourly cost of the load balancer, database cost after credits, using https://calculator.aws/; whether the stack can be stopped or deleted between demos.
- [ ] **Region.** An EU region offering ECS Express Mode, the database option and EventBridge Scheduler (relevant to the GDPR write-up, although all data is synthetic).
- [ ] **Student credits.** Whether the lecturer or college provides AWS credits or a student programme.
- [ ] **Billing alerts.** A budget and alert configured before anything is deployed.

## 4. Risks and costs

- Credits and the 6-month Free plan may run out before marking (the limit is verified [3]; the amount of spend is unknown). Mitigation: create the account late.
- Always-on resources (task, load balancer, database) cost money until deleted; Express Mode log groups never expire by default [2]. No figures are stated here because none were verified.
- AWS services change: App Runner closed to new customers [1]. Re-check the console and documentation at M1 and D1.
- Complexity: container registry, IAM roles, networking, database, scheduler and logs must all work, and D1 is budgeted at one hour in the Build Plan. Risk of overrun; if M1 or D1 passes 125% of estimate, run the pace test.
- Personal data: all data is synthetic, but the log retention and database access settings still belong in the GDPR write-up.

## 5. Open questions for the lecturer

1. Will the hosting sessions cover AWS or another provider, and should the build wait for them?
2. Does the college provide AWS credits or student accounts, so a personal card is not needed?
3. Is a personal AWS account acceptable for the deployed app, and how long must it stay up for marking?
4. Is stopping the app between demos acceptable, if the marker can be given a start-up note?
5. Is there a preferred host known to support a scheduled job and two database roles?

## 6. Decision needed and by when

Confirm AWS (or name an alternative) as the host, once the claims in Section 3 are checked. By the end of week 7, before M1 starts (Build Plan 9.3). Record the outcome in `docs/decision-log.md`. Create the AWS account no earlier than about week 7.

## Sources (all opened 18 November 2026)

1. AWS App Runner availability change: https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html
2. Best practices for Amazon ECS Express Mode services: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-best-practices.html
3. AWS Free Tier with Amazon Aurora and RDS: https://aws.amazon.com/rds/free
4. Amazon Aurora PostgreSQL now available with the AWS Free Tier (posted 25 March 2026): https://aws.amazon.com/about-aws/whats-new/2026/03/amazon-aurora-postgresql-aws-free-tier/
5. Understanding the rds_superuser role (RDS for PostgreSQL): https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Roles.rds_superuser.html
6. EventBridge Scheduler `update-schedule` reference (ECS RunTask target, Fargate launch type, time zone): https://docs.aws.amazon.com/cli/latest/reference/scheduler/update-schedule.html

Not opened, still unverified: the secondary article at https://oneuptime.com/blog/post/2026-02-12-use-aws-free-tier-effectively/markdown.
