# Sugestões de issues para Copilot / backlog

1. **Integração Stripe Connect End-to-End**
   - Ativar contas conectadas para vendedores do marketplace.
   - Automatizar payouts e reconciliar ledger com webhooks reais.

1. **Migrar cache para Upstash Redis**
   - Adicionar client autenticado via `REDIS_URL` + `REDIS_TOKEN`.
   - Incluir métricas de latência e fallback automático.

1. **Header bidding / Prebid.js**
   - Implementar slots no frontend com adaptadores open-source.
   - Conectar ao backend `/api/v1/marketplace/ads/slot` como fallback.

1. **Cluster privado de inferência**
   - Provisionar GPU spot (ex: AWS g5) via Terraform.
   - Atualizar `iaAdapter` para fazer failover entre Hugging Face, cluster privado e fallback determinístico.

1. **Persistência Supabase**
   - Escrever adapter para quotas, marketplace items e KYC usando Postgres.
   - Adicionar migrações e seeds iniciais (0 custo no free tier).
