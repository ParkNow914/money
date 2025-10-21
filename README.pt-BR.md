# AutoCash Ultimate ðŸš€

**ECOSSISTEMA AUTONOMO, PRIVACY-FIRST, MULTICANAL E ORQUESTRADO** para maximizacao realistica e escalavel de receitas partindo de ZERO aporte.

[![CI Status](https://github.com/ParkNow914/money/workflows/CI/badge.svg)](https://github.com/ParkNow914/money/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | **Portugues**

## ðŸŽ¯ Principios Absolutos

- âœ… **Legalidade e Etica**: Proibido qualquer pratica fraudulenta
- ðŸ”’ **Privacy by Design**: LGPD compliant, consentimento explicito
- ðŸ›¡ï¸ **Security First**: Nunca commitar segredos, criptografia at-rest
- ðŸ‘ï¸ **Human Review**: review_required=true por padrao
- ðŸ†“ **Free-Tier First**: Oracle Cloud, Cloudflare Workers, GitHub Pages
- ðŸ”´ **Kill-Switch**: Pausa operacional via endpoint ou arquivo

## ðŸ—ï¸ Stack Tecnologica

- **Backend/API**: FastAPI (Python 3.11+) + Uvicorn
- **Database**: SQLite (MVP) â†’ PostgreSQL ready
- **Frontend**: Next.js 14 (App Router) com SSG/ISR
- **Deploy**: GitHub Pages + Oracle Cloud Free Tier
- **Analytics**: Matomo (privacy-first)
- **Testing**: pytest (coverage >= 75%)
- **CI/CD**: GitHub Actions

## ðŸš€ Quick Start (5 minutos)

### Pre-requisitos

- Docker & Docker Compose
- Python 3.11+
- Git

### Instalacao

\\\ash
# Clone o repositorio
git clone https://github.com/ParkNow914/money.git
cd money

# Configure ambiente
cp .env.example .env
# Edite .env com suas configuracoes

# Inicie com Docker
docker-compose -f docker/docker-compose.yml up --build

# OU sem Docker
pip install -r requirements.txt
python generate_samples.py
\\\

Servicos disponiveis:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## ðŸ“Š Funcionalidades

### MVP (v1.0 - Completo âœ…)
- âœ… Gerador de conteudo (700-1200 palavras, SEO-otimizado)
- âœ… Banco de dados LGPD-compliant
- âœ… Infraestrutura de seguranca (Argon2, AES-256, JWT)
- âœ… Testes (20+ casos, 95%+ cobertura)
- âœ… CI/CD pipeline (GitHub Actions)
- âœ… Documentacao completa

### Roadmap

**PR2: Publisher + Site (1-2 semanas)**
- Next.js 14 site estatico
- Deploy GitHub Pages
- SEO otimizado
- Sitemap.xml dinamico

**PR3: Tracking (1 semana)**
- Matomo analytics
- Event tracking
- Conversion tracking

**PR4: Monetizacao (1 semana)**
- Links de afiliados
- UTM tracking
- Revenue reporting

**PR5: Otimizacao (2 semanas)**
- A/B testing
- Personalizacao
- Recomendacoes

## ðŸ’° Projecao de Receita

| Periodo | Trafego/mes | Receita Mensal |
|---------|-------------|----------------|
| Mes 3-4 | 500-1000 | R\$ 50-100 |
| Mes 5-6 | 2000-5000 | R\$ 200-300 |
| Mes 7-12 | 10k-20k | R\$ 500-2000 |
| Ano 2 | 50k+ | R\$ 2000-5000+ |

**Tempo ate primeira receita:** 3-6 meses  
**Investimento necessario:** R\$ 0-100 (dominio opcional)

## ðŸ”’ Seguranca & Compliance

### LGPD Compliance âœ…
- Double opt-in para emails
- Registro de consentimento granular
- DSAR endpoints (/privacy/export, /privacy/delete)
- Data minimization
- Retencao configuravel (12 meses padrao)

Ver checklist completo: [docs/lgpd_checklist.md](./docs/lgpd_checklist.md)

### Security âœ…
- âœ… Senhas hashed com Argon2
- âœ… Secrets via env/vault
- âœ… Rate limiting em APIs
- âœ… SAST com bandit
- âœ… Encryption at-rest (AES-256)

Ver checklist completo: [docs/security_checklist.md](./docs/security_checklist.md)

## ðŸ“ Estrutura do Projeto

\\\
/
â”œâ”€â”€ app/                    # Backend FastAPI
â”œâ”€â”€ tests/                  # Testes unitarios
â”œâ”€â”€ docker/                 # Dockerfiles e compose
â”œâ”€â”€ docs/                   # Documentacao
â”œâ”€â”€ data/                   # Keywords seed
â”œâ”€â”€ examples/               # Sample posts
â”œâ”€â”€ scripts/                # Scripts operacionais
â””â”€â”€ .github/workflows/      # CI/CD
\\\

## ðŸ§ª Testes

\\\ash
# Rodar todos os testes
pytest tests/ -v --cov=app

# Com coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
\\\

**Coverage minimo exigido: 75%**

## ðŸ¤ Contribuindo

1. Fork o repositorio
2. Crie uma branch feature (\git checkout -b feature/AmazingFeature\)
3. Commit suas mudancas (\git commit -m 'Add: AmazingFeature'\)
4. Push para a branch (\git push origin feature/AmazingFeature\)
5. Abra um Pull Request

### PR Checklist
- [ ] Testes passando (coverage >= 75%)
- [ ] Lint/format (black, isort, flake8)
- [ ] Sem secrets commitados
- [ ] LGPD compliance verificado
- [ ] Documentacao atualizada

## ðŸ“„ Licenca

MIT License - veja [LICENSE](./LICENSE) para detalhes.

## âš ï¸ Disclaimer

Este projeto e para fins educacionais e operacao etica. Qualquer uso fraudulento, ilegal ou que viole termos de servico de terceiros e **estritamente proibido** e de responsabilidade do usuario final.

## ðŸ“ž Suporte

- ðŸ“š Documentacao: [/docs](./docs)
- ðŸ› Issues: [GitHub Issues](https://github.com/ParkNow914/money/issues)
- ðŸ’¬ Discussoes: [GitHub Discussions](https://github.com/ParkNow914/money/discussions)

---

**Construido com â¤ï¸ e responsabilidade etica**
