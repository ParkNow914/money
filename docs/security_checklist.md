# Security Checklist

Use this before every release or infrastructure change.

## Application surface

- [ ] **Authentication flow**: confirm `authMiddleware` properly rejects requests without `x-admin-key` for admin routes.
- [ ] **Rate limiting**: validate `meteringMiddleware` thresholds and ensure `CIRCUIT_BREAKER_DAILY_BUDGET` matches the environment budget.
- [ ] **Dependency audit**: run `npm audit` + `npm outdated` monthly; upgrade high severity packages.
- [ ] **Secrets**: never commit `.env`; store production secrets in AWS Secrets Manager or Railway variables.

## Infrastructure

- [ ] **Terraform plan review**: require pull request approval before `terraform apply`.
- [ ] **IAM least privilege**: scope ECS task role to the exact AWS services needed (S3 read/write, SSM if required).
- [ ] **Network segmentation**: confirm ECS tasks and RDS live in private subnets; only ALB is public.
- [ ] **Backups**: enable RDS automated backups (already 7 days) and enable S3 versioning if storing critical datasets.

## Monitoring & logging

- [ ] Sentry DSN configured with environment/release tags.
- [ ] CloudWatch dashboards + alarms created (see `docs/monitoring.md`).
- [ ] Log retention > 14 days or exported to long-term storage.

## Operational readiness

- [ ] Runbook updated (incident response contacts, on-call rotations).
- [ ] Disaster recovery test performed at least once per quarter (restore RDS snapshot + replay ledger).
- [ ] Stripe/Supabase credentials rotated every 90 days.

Keep evidence (screenshots, CLI output) for audits or investor due diligence.
