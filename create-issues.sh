# Script para criar issues via GitHub CLI (gh)
# Instale: winget install --id GitHub.cli

# Issue 1: Adicionar GitHub Secrets
gh issue create \
  --title "ðŸ” Adicionar GitHub Secrets para CI/CD" \
  --body "Adicionar os 4 secrets necessarios para o CI/CD funcionar:

- [ ] SECRET_KEY
- [ ] ENCRYPTION_KEY
- [ ] ADMIN_TOKEN
- [ ] IP_SALT

Ver arquivo .secrets-generated.txt para valores.

Link: https://github.com/ParkNow914/money/settings/secrets/actions/new" \
  --label "configuration,priority-high"

# Issue 2: Configurar Repository Settings
gh issue create \
  --title "âš™ï¸ Configurar Repository Settings" \
  --body "Configurar settings do repositorio:

- [ ] Description
- [ ] Topics: python, fastapi, content-generation, lgpd, privacy-first
- [ ] Enable Issues, Discussions, Projects
- [ ] Enable Dependabot
- [ ] Configure branch protection

Link: https://github.com/ParkNow914/money/settings" \
  --label "configuration,documentation"

# Issue 3: Implementar PR2 - Publisher
gh issue create \
  --title "ðŸš€ PR2: Publisher + Static Site Generation" \
  --body "Implementar sistema de publicacao conforme PR2_PLAN.md:

- [ ] Setup Next.js 14
- [ ] Implementar componentes React
- [ ] Publisher service Python
- [ ] GitHub Actions deploy workflow
- [ ] SEO optimization
- [ ] Testes E2E

Tempo estimado: 1-2 semanas
Ver: PR2_PLAN.md" \
  --label "enhancement,pr2,publisher"

# Issue 4: Setup Monetizacao
gh issue create \
  --title "ðŸ’° Setup de Monetizacao - Afiliados" \
  --body "Configurar contas de afiliados:

- [ ] Amazon Associates
- [ ] Hotmart
- [ ] Lomadee
- [ ] Awin
- [ ] Implementar tracking
- [ ] Documentar processo

Tempo estimado: 3-5 dias" \
  --label "enhancement,monetization"
