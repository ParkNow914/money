# Always Free Money Stack

Plataforma "always free" com monetização invisível por trás (afiliados, marketplace, dados e API). Todo o stack roda com zero investimento inicial usando apenas free tiers ou fallbacks locais.

## Visão geral

- **Backend**: Node.js + Express em TypeScript com arquitetura modular, ledger append-only, quotas, antifraude, cache (Redis/ memória) e workers (ETL + billing).
- **Frontend**: React + Vite em TypeScript com páginas Home, Demo IA, Marketplace e Admin, incluindo placeholders de anúncios e chamadas reais ao backend.
- **Infra**: Esqueleto Terraform (VPC/RDS/S3/EKS opcionais) pronto para quando você sair do modo free.
- **DevOps**: GitHub Actions para lint, build e testes; script `scripts/start-local.sh` para dev rápido; exemplos de `.env` cobrindo todas as integrações.

## Como rodar gratuitamente (local)

1. **Clone o repo** e acesse a pasta.
2. **Copie variáveis**: `cp .env.example .env` (ou rode `scripts/start-local.sh`).
3. **Instale dependências**: `npm install` (workspace raiz cuida de backend e frontend).
4. **Dev servers**: `npm run dev` levanta backend (porta 4000) e frontend (porta 5173) via `concurrently`.
5. **Health-check**: `curl http://localhost:4000/health` deve retornar `{"status":"ok"...}`.
6. **Frontend**: abra `http://localhost:5173` e navegue pelas páginas.

## Variáveis de ambiente chave

Veja `.env.example`. Todas têm fallback gratuito:

| Variável | Descrição | Fallback quando vazio |
| --- | --- | --- |
| `HF_API_KEY` | Hugging Face Inference | Gerador determinístico local |
| `REDIS_URL` | Cache gerenciado (Upstash) | Map in-memory + TTL |
| `STRIPE_KEY` / `STRIPE_WEBHOOK_SECRET` | Pagamentos automatizados | Faturas JSON locais + fluxo manual |
| `DATABASE_URL` / Supabase | Persistência quotas/marketplace | Arquivos JSON em `data/` |
| `SENTRY_DSN` | Observabilidade | Logs pino + console |
| `AFFILIATE_DEFAULT_TRACKER` | Rastreador padrão | Links estáticos |

## Deploy 100% free

- **Backend**: pode ser publicado no Render free, Railway ou fly.io. Basta apontar `npm run start` e definir as envs desejadas.
- **Frontend**: pronto para Vercel (Vite). Crie `deploy.yml` baseado no stub da pipeline.
- **Banco/Cache**: conecte Supabase free tier e Upstash Redis (grátis) quando precisar de persistência multi-instância.

### Passo a passo (exemplo Vercel)

1. Instale o [Vercel CLI](https://vercel.com/docs/cli) e rode `vercel` no diretório `frontend`.
2. Configure `VITE_API_BASE` para o endpoint do backend.
3. Para backend em Railway: `railway up` com `PORT=4000` e `.env` exportado.

## Monetização embutida

- **Afiliados**: `backend/src/services/affiliate.ts` lê `affiliates.json` e injeta links nas respostas IA + frontend renderiza em `ResultCard`.
- **Marketplace**: upload/purchase registra ledger (`data/ledger.jsonl`). `POST /api/v1/checkout` simula Stripe quando não houver chave.
- **Ads**: backend serve `/api/v1/marketplace/ads/slot` a partir de `adsdb.json`; frontend mostra bloco patrocinado.
- **Dados**: worker `etlWorker` gera `data/telemetry-dataset.json` (consultado em `/api/v1/admin/data/catalog`).
- **API-as-a-product**: parceiros enviam `x-api-key` (mesmo valor de `ADMIN_API_KEY` na demo) e recebem quotas maiores.

## Segurança, fraude e compliance

- Quotas/daily budgets (`middleware/metering.ts` + `services/circuitBreaker.ts`).
- Detecção simples de abuso (`services/fraud.ts`).
- Ledger append-only (`data/ledger.jsonl`) + invoices JSON.
- KYC progressivo via `POST /api/v1/kyc/submit` salvando em `data/kycRequests.json`.
- Fingerprinting básico (hash IP + user-agent) disponível em `req.fingerprint`.

## Testes e CI

- **Unitários**: `tests/backend.test.ts`, `tests/cache.test.ts` rodam com `npm test` (Vitest configurado no monorepo).
- **CI**: `.github/workflows/ci.yml` executa lint, build e testes em cada PR/push.

## Scripts úteis

- `npm run dev` – backend + frontend.
- `npm run build` – transpila backend (`tsc`) e frontend (`vite build`).
- `npm run test` – Vitest em modo `run`.
- `npm run lint` – ESLint (TS + React) em ambos pacotes.
- `scripts/start-local.sh` – instala dependências e sobe tudo automaticamente (Linux/macOS/WSL).

## Integrações opcionais

- **Hugging Face**: crie uma *free API token*, defina `HF_API_KEY` e modelos específicos (ex: `HF_MODEL_LITE`).
- **Stripe**: defina `STRIPE_KEY` + `STRIPE_WEBHOOK_SECRET` para capturar pagamentos reais no `billingWorker` e nas rotas `/webhooks/stripe`.
- **Supabase**: preencha `SUPABASE_URL` + `SUPABASE_SERVICE_KEY` e plugue suas tabelas (arquivo `services/quotas.ts` preparado para estender).
- **Upstash Redis**: defina `REDIS_URL` e `REDIS_TOKEN` para cache e metering distribuídos.

## Estrutura de pastas

```text
backend/          # Express + serviços + workers
frontend/         # React + Vite
infra/terraform/  # IaC skeleton
scripts/          # utilidades de dev
.tests/           # Vitest (unit + integration)
.github/workflows # CI
```

## Roadmap sugerido

Veja `ISSUES_TO_AUTOGENERATE.md` para ideias de issues (Stripe Connect, Upstash, header bidding, cluster privado de inferência).

## Licença

Projeto open-source focado em validação rápida. Ajuste conforme seu modelo de negócio.
