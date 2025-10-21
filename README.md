# AutoCash Ultimate 🚀

**ECOSSISTEMA AUTÔNOMO, PRIVACY-FIRST, MULTICANAL E ORQUESTRADO** para maximização realista e escalável de receitas partindo de ZERO aporte.

[![CI Status](https://github.com/yourusername/autocash-ultimate/workflows/CI/badge.svg)](https://github.com/yourusername/autocash-ultimate/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-75%25-green.svg)](./tests)

## 🎯 Princípios Absolutos

- ✅ **Legalidade e Ética**: Proibido qualquer prática fraudulenta
- 🔒 **Privacy by Design**: LGPD compliant, consentimento explícito
- 🛡️ **Security First**: Nunca commitar segredos, criptografia at-rest
- 👁️ **Human Review**: `review_required=true` por padrão
- 🆓 **Free-Tier First**: Oracle Cloud, Cloudflare Workers, GitHub Pages
- 🔴 **Kill-Switch**: Pausa operacional via endpoint ou arquivo

## 🏗️ Stack Tecnológica

- **Backend/API**: FastAPI (Python 3.11+) + Uvicorn
- **Database**: SQLite (MVP) → PostgreSQL ready
- **Search**: MeiliSearch (OSS) para indexação textual
- **Vector DB**: Chroma (local) para embeddings e personalização
- **Cache/Queue**: Redis (docker) ou RQ
- **Edge**: Cloudflare Workers + Pages
- **Frontend**: Next.js (App Router) com SSG/ISR
- **Analytics**: Matomo (privacy-first) + Prometheus/Grafana
- **Testing**: pytest (coverage >= 75%), bandit (SAST)
- **CI/CD**: GitHub Actions
- **IaC**: Terraform (Oracle + Cloudflare)

## 🚀 Quick Start (Local Development)

### Pré-requisitos

- Docker & Docker Compose
- Python 3.11+
- Git

### Passo 1: Clone e Configure

```bash
git clone https://github.com/yourusername/autocash-ultimate.git
cd autocash-ultimate
cp .env.example .env
# Edite .env com suas configurações (sem segredos reais!)
```

### Passo 2: Build e Start

```bash
docker-compose up --build
```

Serviços disponíveis:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- MeiliSearch: http://localhost:7700
- Redis: localhost:6379

### Passo 3: Seed Keywords e Gerar Posts

```bash
# Carregar keywords iniciais
bash scripts/seed-keywords.sh

# Gerar 5 posts de exemplo
docker-compose exec api python -m app.cli generate --count 5
```

Os posts gerados estarão em `examples/sample_posts.json` e no banco de dados.

## 📁 Estrutura do Repositório

```
/
├── app/                    # Backend FastAPI
│   ├── main.py            # Entry point
│   ├── config.py          # Configurações centralizadas
│   ├── db.py              # Database setup
│   ├── models.py          # SQLAlchemy models
│   ├── routes/            # API endpoints
│   └── services/          # Business logic
├── data/                  # Dados seed
├── docker/                # Dockerfiles e compose
├── docs/                  # Documentação detalhada
├── scripts/               # Scripts operacionais
├── terraform/             # Infrastructure as Code
├── tests/                 # Testes unitários e E2E
└── tools/                 # Ferramentas auxiliares
```

## 🔐 Configuração de Segredos (GitHub Secrets)

⚠️ **NUNCA commite segredos no código!**

Configure os seguintes secrets no GitHub:

```
OPENAI_API_KEY          # (opcional) Para geração avançada
CLOUDFLARE_API_TOKEN    # Para deploy Workers
ORACLE_CREDENTIALS      # JSON com credenciais Oracle Cloud
SMTP_PASSWORD           # Para envio de emails
MATOMO_AUTH_TOKEN       # Para analytics
```

### Como adicionar:
1. Vá em Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Adicione cada secret acima

## 🧪 Testes

```bash
# Rodar todos os testes
pytest tests/ -v --cov=app --cov-report=html

# Apenas testes do generator
pytest tests/test_generator.py -v

# Com coverage report
pytest --cov=app --cov-report=term-missing
```

**Coverage mínimo exigido: 75% (core modules)**

## 📊 Funcionalidades MVP (PR1)

- ✅ Generator Core: Gera artigos de 700-1200 palavras com SEO
- ✅ Keyword Seeding: Importa keywords de CSV
- ✅ Originalidade: Check de similaridade antes de criar
- ✅ Database: SQLite com models completos
- ✅ Tests: Cobertura >= 75% em services/generator.py
- ✅ Sample Posts: 5 posts de alta qualidade gerados

## 🛣️ Roadmap (90 dias)

### Semana 1-2: MVP Generator ✅
- [x] Setup repositório
- [x] Generator core
- [x] Tests e CI
- [x] Docker compose

### Semana 3-4: Publisher & Site
- [ ] Static site generation (Next.js)
- [ ] SEO otimizado (JSON-LD, sitemap)
- [ ] Deploy para GitHub Pages

### Semana 5-6: Tracking & Monetization
- [ ] Affiliate tracking com privacy
- [ ] UTM auto-injection
- [ ] EPC estimator

### Semana 7-8: Repurposer & Multi-canal
- [ ] Thread X generator
- [ ] Video scripts
- [ ] Email sequences
- [ ] PDF lead magnets

### Semana 9-10: Personalization & Vector Search
- [ ] Embeddings pipeline
- [ ] Vector store integration
- [ ] Recommendation engine

### Semana 11-12: Optimizer & Growth
- [ ] A/B testing framework
- [ ] Multi-armed bandits
- [ ] Auto-optimizer

## 📋 Compliance & Segurança

### LGPD Compliance ✅
- Double opt-in para emails
- Registro de consentimento granular
- DSAR endpoints (/privacy/export, /privacy/delete)
- Data minimization (apenas dados necessários)
- Retenção configurável (12 meses padrão)
- DPA templates em `/docs/dpa_template.md`

Ver checklist completo: [docs/lgpd_checklist.md](./docs/lgpd_checklist.md)

### Security Checklist ✅
- ✅ Senhas hashed com Argon2
- ✅ Secrets via env/vault (nunca em código)
- ✅ Rate limiting em APIs
- ✅ SAST com bandit
- ✅ Dependency scanning
- ✅ CSP, HSTS, security headers
- ✅ Encryption at-rest (AES-256)

Ver checklist completo: [docs/security_checklist.md](./docs/security_checklist.md)

## 🚨 Kill-Switch

Para pausar todas as operações automatizadas:

```bash
# Método 1: Via endpoint (requer auth)
curl -X POST http://localhost:8000/api/admin/killswitch \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Método 2: Via arquivo
touch /tmp/killswitch.lock
```

## 📈 Projeções e Simulações

```bash
# Gerar projeções de receita (4 cenários)
python tools/projections.py --output data/projections.csv

# Simular tráfego para testes
python tools/simulate_traffic.py --visitors 1000 --duration 3600
```

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças atômicas (`git commit -m 'Add: AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request com checklist de revisão

### PR Checklist
- [ ] Testes passando (coverage >= 75%)
- [ ] Lint/format (black, isort, flake8, mypy)
- [ ] Sem secrets commitados
- [ ] LGPD compliance verificado
- [ ] Security checklist aplicado
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado

## 📄 Licença

MIT License - veja [LICENSE](./LICENSE) para detalhes.

## ⚠️ Disclaimer

Este projeto é para fins educacionais e operação ética. Qualquer uso fraudulento, ilegal ou que viole termos de serviço de terceiros é **estritamente proibido** e de responsabilidade do usuário final.

## 📞 Suporte

- 📚 Documentação: [/docs](./docs)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/autocash-ultimate/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/yourusername/autocash-ultimate/discussions)

---

**Construído com ❤️ e responsabilidade ética**
