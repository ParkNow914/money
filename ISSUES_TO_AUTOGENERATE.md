# Backlog ready-to-open Issues

Use as copy/paste templates when creating GitHub issues.

## 1. Stripe Connect for marketplace sellers

- **Problem**: payouts today are simulated. Sellers cannot onboard nor receive real transfers.
- **Scope**:
   1. Create onboarding endpoints (`/api/v1/admin/connect/*`) calling Stripe Connect APIs.
   2. Store account IDs in `data/` or Supabase (once available) and expose status via Admin UI.
   3. Update `billingWorker` to create transfer groups and emit real payouts/webhooks.
   4. Expand tests to mock Stripe SDK using fixtures.
- **Definition of done**: seller can onboard with test data, run a purchase, and see a payout registered in the ledger + webhook log.

## 2. Upstash Redis as managed cache/metering

- **Problem**: cache + quota store are in-memory, so multiple instances drift.
- **Scope**:
   1. Add `UPSTASH_REDIS_REST_URL/TOKEN` envs and instantiate ioredis with TLS.
   2. Wrap cache (`services/cache.ts`) and quotas (`services/quotas.ts`) with retry/backoff + circuit breaker metrics.
   3. Emit hit/miss/latency stats to pino and `/api/v1/admin/metrics`.
   4. Provide migration guide in docs (how to warm cache, failure scenarios).
- **Definition of done**: disabling the Redis env reverts to local Map without crashing and admin metrics surface hit rate.

## 3. Header bidding with Prebid.js

- **Problem**: ads slot serves only static JSON. Need dynamic demand to prove monetization uplift.
- **Scope**:
   1. Add Prebid.js loader + bidders (AppNexus/Sharethrough) to `frontend/src/pages/Home.tsx`.
   2. Use `/api/v1/marketplace/ads/slot` as fallback creative when auctions fail.
   3. Track impressions/clicks back to backend via `/api/v1/marketplace/ads/events` (new route).
   4. Document how to configure bidder IDs in `.env.example`.
- **Definition of done**: running locally shows Prebid auction requests in devtools and fallback triggers when bidders time out.

## 4. Private inference cluster (GPU spot)

- **Problem**: IA adapter relies solely on Hugging Face or deterministic fallback.
- **Scope**:
   1. Extend Terraform to create an EC2 g5.xlarge spot ASG + IMDSv2-locked security group.
   2. Publish a container image with the selected open-source model + server (ex: TGI) to ECR and point autoscaling launch template to it.
   3. Update `services/iaAdapter.ts` to add a third provider (`PRIVATE_CLUSTER_URL`) with health checks + circuit breaker budget.
   4. Add runbook section describing warm-up, scaling and failover order.
- **Definition of done**: fallback order HF → Private cluster → deterministic, with metrics recorded per provider.

## 5. Supabase persistence adapters

- **Problem**: marketplace items, quotas and KYC live in JSON files which do not scale nor survive multi-instance deploys.
- **Scope**:
   1. Create SQL schema (items, quotas, kyc_requests, ledger) via Supabase migration scripts and commit under `infra/migrations`.
   2. Implement repository layer using `@supabase/supabase-js` (service key) with graceful fallback to file system when envs missing.
   3. Update tests to run against the file fallback but mock Supabase client to ensure serialization.
   4. Document how to seed the tables and rotate service keys.
- **Definition of done**: setting Supabase envs transparently migrates all CRUD paths without code changes on the caller side.
