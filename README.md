# autocash-ultimate 🚀

**Privacy-first, LGPD-compliant autonomous content generation and monetization platform**

> ⚖️ **Ethical & Legal**: All practices comply with laws and platform TOS. No fraud, no auto-clicks, no TOS violations.  
> 🔒 **Privacy-first**: LGPD compliant with consent management, data minimization, and hashed identifiers.  
> 📝 **Review Required**: All generated content requires human review by default (`review_required=true`).

## 🎯 Project Overview

autocash-ultimate is an autonomous ecosystem for realistic, scalable revenue generation starting from zero investment. It focuses on:

- **High-quality content generation** from keyword seeds
- **Multi-channel repurposing** (articles, threads, videos, PDFs, emails)
- **Privacy-preserving tracking** for monetization optimization
- **Ethical monetization** through affiliate marketing, ads, and premium content
- **Full compliance** with LGPD and data protection regulations

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.11+) with SQLAlchemy
- **Database**: SQLite (MVP) → PostgreSQL (production-ready)
- **Deployment**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Infrastructure**: Oracle Free Tier, Cloudflare Workers/Pages
- **Privacy**: Hashed identifiers, consent management, LGPD compliance

### Key Features (MVP - v0.1.0)
- ✅ Content generator from keywords (700-1200 words, SEO-optimized)
- ✅ Article validation and quality checks
- ✅ Privacy-preserving tracking with hashed identifiers
- ✅ RESTful API with FastAPI
- ✅ Admin authentication with bearer tokens
- ✅ Metrics and monitoring endpoints
- ✅ Docker development environment
- ✅ Comprehensive test suite (>75% coverage)
- ✅ LGPD and security documentation

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/ParkNow914/money.git
cd money
```

### 2. Environment Setup
Create `.env` file (never commit this!):
```bash
# Copy example and customize
cat > .env << EOF
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-this
ADMIN_TOKEN=your-admin-token-change-this
IP_SALT=your-random-salt-32-chars
REVIEW_REQUIRED=true
KILL_SWITCH_ENABLED=false
EOF
```

### 3. Start with Docker Compose
```bash
# Build and start services
docker-compose -f docker/docker-compose.yml up --build

# The API will be available at http://localhost:8000
```

### 4. Seed Keywords
```bash
# In another terminal, seed initial keywords
./scripts/seed-keywords.sh
```

### 5. Generate Sample Content
```bash
# Generate article from keyword
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: Bearer dev-admin-token-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "digital marketing"}'
```

### 6. View Generated Articles
```bash
# List all articles
curl http://localhost:8000/api/articles

# View specific article by slug
curl http://localhost:8000/api/articles/{slug}
```

## 📚 API Documentation

### Interactive Docs (Development Only)
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Public Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/articles` - List articles
- `GET /api/articles/{slug}` - Get specific article
- `GET /api/metrics` - Prometheus metrics
- `GET /api/stats` - Business statistics

#### Admin Endpoints (Require Authorization)
- `POST /api/generate` - Generate article from keyword
- `POST /api/keywords/seed` - Add keyword to seed list
- `GET /api/keywords` - List keywords

### Authentication
Admin endpoints require Bearer token:
```bash
Authorization: Bearer YOUR_ADMIN_TOKEN
```

## 🧪 Testing

### Run All Tests
```bash
# Using Docker
docker-compose -f docker/docker-compose.yml run app pytest

# Local development
pip install -r requirements.txt
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### View Coverage Report
```bash
# Open htmlcov/index.html in browser
open htmlcov/index.html
```

## 🔒 Security & Compliance

### LGPD Compliance
See [docs/lgpd_checklist.md](docs/lgpd_checklist.md) for complete checklist.

Key features:
- ✅ Data minimization (hashed identifiers only)
- ✅ Consent management
- ✅ Audit logging
- ✅ Configurable data retention
- 🔄 DSAR endpoints (TODO: next phase)

### Security
See [docs/security_checklist.md](docs/security_checklist.md) for complete checklist.

Key features:
- ✅ No secrets in repository
- ✅ Security headers (CSP, HSTS, X-Frame-Options)
- ✅ Rate limiting capability
- ✅ Kill switch for emergencies
- ✅ Argon2 password hashing
- ✅ SAST with Bandit
- ✅ Dependency scanning with Safety

## 📁 Project Structure

```
/
├── app/                      # Main application code
│   ├── config.py            # Configuration management
│   ├── db.py                # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── main.py              # FastAPI application
│   ├── routes/              # API routes
│   │   ├── generate.py      # Content generation endpoints
│   │   └── metrics.py       # Monitoring endpoints
│   └── services/            # Business logic
│       ├── generator.py     # Content generator
│       └── paraphrase.py    # Content variation
├── data/                    # Data files
│   └── keywords_seed.csv    # Initial keywords
├── docker/                  # Docker configuration
│   ├── Dockerfile           # Application container
│   └── docker-compose.yml   # Multi-container setup
├── docs/                    # Documentation
│   ├── lgpd_checklist.md    # LGPD compliance guide
│   └── security_checklist.md # Security best practices
├── scripts/                 # Utility scripts
│   └── seed-keywords.sh     # Keyword seeding script
├── tests/                   # Test suite
│   ├── test_generator.py    # Generator tests
│   └── test_tracking.py     # Privacy/tracking tests
├── templates/               # Content templates (TODO)
├── site-out/                # Generated static site (TODO)
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
├── .gitignore              # Git ignore patterns
├── LICENSE                 # MIT License
└── README.md               # This file
```

## 🗺️ Roadmap

### Phase 1: MVP (Current - v0.1.0)
- [x] Content generator service
- [x] REST API with FastAPI
- [x] Database models and migrations
- [x] Privacy-preserving tracking models
- [x] Docker development environment
- [x] Basic tests and documentation
- [x] LGPD/security checklists

### Phase 2: Content Pipeline (v0.2.0)
- [ ] Repurposer service (threads, videos, PDFs, emails)
- [ ] Publisher service (static site generation)
- [ ] Template system (Jinja2)
- [ ] Image generation pipeline
- [ ] DSAR endpoints (data export, deletion)

### Phase 3: Monetization (v0.3.0)
- [ ] Affiliate link tracking
- [ ] Click tracking with privacy compliance
- [ ] UTM parameter handling
- [ ] EPC (Earnings Per Click) calculator
- [ ] Revenue reporting

### Phase 4: Optimization (v0.4.0)
- [ ] A/B testing framework
- [ ] Multi-armed bandit optimizer
- [ ] Personalization engine
- [ ] Vector embeddings (Chroma/Qdrant)
- [ ] Recommendation system

### Phase 5: Automation (v0.5.0)
- [ ] Cloudflare Workers cron
- [ ] Batch generation
- [ ] Email funnels
- [ ] Auto-publisher (with review)
- [ ] Monitoring and alerting

### Phase 6: Scale (v1.0.0)
- [ ] PostgreSQL migration
- [ ] Redis cache/queue
- [ ] MeiliSearch integration
- [ ] CI/CD with GitHub Actions
- [ ] Infrastructure as Code (Terraform)
- [ ] Production deployment guides

## 🚀 Deployment

### Development
```bash
docker-compose -f docker/docker-compose.yml up
```

### Production (Oracle Cloud Free Tier)
Documentation coming in Phase 6. See [docs/deploy_oracle.md](docs/deploy_oracle.md) (TODO).

Key steps:
1. Provision Oracle Free Tier VM
2. Configure firewall and security groups
3. Install Docker on VM
4. Set up environment variables (use Oracle Vault)
5. Deploy with docker-compose
6. Configure Cloudflare for CDN/DDoS protection
7. Set up SSL with Let's Encrypt
8. Configure automated backups

## 🤝 Contributing

This is currently a private project. Contributions will be opened in future phases.

### Development Guidelines
1. **Ethical principles**: No fraud, no TOS violations, no manipulation
2. **Privacy-first**: Always use hashed identifiers, never store raw PII
3. **Review required**: All generated content must be reviewed
4. **Test coverage**: Maintain >75% coverage
5. **Security**: Follow security checklist
6. **LGPD**: Ensure compliance with all changes

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for legal and ethical use only. Users are responsible for:
- Complying with all applicable laws and regulations
- Respecting platform Terms of Service
- Obtaining proper consents for data processing
- Not engaging in fraudulent or deceptive practices
- Reviewing all generated content before publication

The authors assume no liability for misuse of this software.

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Review documentation in `/docs`
- Check LGPD checklist for privacy questions
- Check security checklist for security questions

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Docker](https://www.docker.com/) - Containerization
- [pytest](https://pytest.org/) - Testing framework

---

**Remember**: `review_required=true` by default. Always review generated content before publication. Privacy and ethics are non-negotiable.