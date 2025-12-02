# Always Free Money Stack

> 🇧🇷 Precisa da versão em português? [Leia o README.pt-BR](README.pt-BR.md).

This monorepo ships a zero-cost stack where the end user never pays but you still monetize through affiliates, marketplace fees, datasets, and API quotas. Everything runs with free tiers or local fallbacks so you can validate without upfront spend.

## Overview

- **Backend** – TypeScript + Express with modular services (ledger, quotas, antifraud, cache, workers, IA adapter) and optional Sentry instrumentation.
- **Frontend** – React + Vite + Tailwind with Home, IA Demo, Marketplace, and Admin pages that hit real endpoints and render affiliate/ads blocks.
- **Infra** – Terraform ready for AWS (VPC, Fargate/ECS, RDS, S3, CloudWatch). You can deploy the same code paths used locally.
- **DevOps** – GitHub Actions for lint/build/test, Vitest suites, and `scripts/start-local.sh` for one-line onboarding.

## Quick start (local, free)

1. `git clone` then `cd money`.
2. Copy envs: `cp .env.example .env` (or run `scripts/start-local.sh`).
3. `npm install` at the repo root (workspaces install backend + frontend together).
4. `npm run dev` to boot backend (4000) and frontend (5173) simultaneously.
5. `curl http://localhost:4000/health` → `{"status":"ok"...}` proves the API is live.
6. Open `http://localhost:5173` and play with the flows.

## Critical environment variables

All keys live in `.env.example` and have zero-cost fallbacks when empty.

| Variable | Purpose | Fallback |
| --- | --- | --- |
| `HF_API_KEY` | Hugging Face Inference | Deterministic offline model |
| `REDIS_URL` / `REDIS_TOKEN` | Cache + metering store | In-memory Map with TTL |
| `STRIPE_KEY` / `STRIPE_WEBHOOK_SECRET` | Real billing/webhooks | JSON invoices + manual checkout |
| `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` | Managed Postgres | Local JSON stores under `data/` |
| `SENTRY_DSN` | Observability | Pino logs + console error handler |
| `AFFILIATE_DEFAULT_TRACKER` | Tracking fallback | Static UTM links |

## Deploy on free tiers

- **Backend** – Works on Render, Railway, Fly.io or any Node host (`npm run start`). Configure envs and optional Redis/Supabase endpoints.
- **Frontend** – Vite output ready for Vercel/Netlify. Sample workflow lives in `.github/workflows/ci.yml`.
- **Data plane** – Adopt Supabase (Postgres) and Upstash Redis when you need shared state; both have permanent free plans.

### Example: Vercel + Railway

1. Deploy frontend with `vercel` inside `/frontend` and set `VITE_API_BASE` to your backend URL.
2. Deploy backend with `railway up`, exposing port 4000 and copying the `.env` you validated locally.

## Built-in monetization paths

- **Affiliates** – `backend/src/services/affiliate.ts` injects partner links in IA responses; `frontend/src/components/ResultCard.tsx` renders the CTAs.
- **Marketplace** – Uploads/purchases hit `/api/v1/marketplace` routes, append to `data/ledger.jsonl`, and simulate Stripe payouts when no key exists.
- **Ads** – `/api/v1/marketplace/ads/slot` serves from `adsdb.json` and the Home page shows the sponsored card.
- **Datasets** – `etlWorker` aggregates telemetry into `data/telemetry-dataset.json` showcased in `/api/v1/admin/data/catalog`.
- **API product** – Partners send `x-api-key` (same value as `ADMIN_API_KEY` during tests) to unlock higher quotas tracked by the ledger.

## Safety, fraud & compliance

- Daily quotas + credit metering (`middleware/metering.ts`, `services/circuitBreaker.ts`).
- Simple fraud heuristics (`services/fraud.ts`) plus append-only ledger + JSON invoices.
- Progressive KYC: `POST /api/v1/kyc/submit` persists to `data/kycRequests.json` and surfaces via admin endpoints.
- Basic fingerprint (IP + user-agent hash) stored on `req.fingerprint` for downstream services.
- Compliance artifacts live under `docs/`: `lgpd_checklist.md`, `security_checklist.md`, and the partner-facing `dpa_template.md`.

## Observability & monitoring

- Enable Sentry by setting `SENTRY_DSN`, `SENTRY_ENVIRONMENT`, and `SENTRY_TRACES_SAMPLE_RATE` (see `docs/monitoring.md`).
- Provisioned AWS stack already streams logs/metrics to CloudWatch; follow the dashboard/alarm recipes in `docs/monitoring.md`.

## Tests & CI

- `npm test` runs Vitest across integration suites (`tests/*.test.ts`).
- `.github/workflows/ci.yml` installs, lints, builds, and executes tests on every push/PR.

## Handy scripts

- `npm run dev` – Hot reload backend + frontend.
- `npm run build` – `tsc` backend + `vite build` frontend.
- `npm run lint` – ESLint for both workspaces.
- `npm run test` – Vitest run mode.
- `scripts/start-local.sh` – Auto install + run (Linux/macOS/WSL).

## Optional integrations

- **Hugging Face** – Provide `HF_API_KEY` and override `HF_MODEL_LITE`/`HF_MODEL_PRO` envs.
- **Stripe** – Populate `STRIPE_KEY`/`STRIPE_WEBHOOK_SECRET`; `billingWorker` creates real invoices and `/webhooks/stripe` validates signatures.
- **Supabase** – Fill Supabase envs and extend `services/quotas.ts` + `services/marketplace.ts` to persist there.
- **Upstash Redis** – Drop your `REDIS_URL` and `REDIS_TOKEN` for shared cache/metering.

## Folder structure

```text
backend/          # Express + services + workers
frontend/         # React + Vite + Tailwind
infra/terraform/  # AWS IaC (VPC, ECS, RDS, S3, CloudWatch)
scripts/          # Local helpers
tests/            # Vitest suites
.github/workflows # CI pipeline
```

## Roadmap

See `ISSUES_TO_AUTOGENERATE.md` for ready-to-open issues (Stripe Connect, Upstash scaling, header bidding, inference cluster, Supabase persistence).

## License

Released under the [MIT License](LICENSE).
