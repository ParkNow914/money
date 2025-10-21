# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository structure
- MVP Generator Core with ethical content generation
- Database models (Article, Keyword, Consent)
- SQLite database with migration path to PostgreSQL
- Keyword seeding from CSV
- Originality checking with similarity detection
- Unit tests with >= 75% coverage
- Docker Compose setup for local development
- LGPD compliance foundation (consent tracking, DSAR endpoints skeleton)
- Security foundations (Argon2 password hashing, env-based secrets)
- CI/CD skeleton with GitHub Actions
- Comprehensive documentation (README, LGPD checklist, Security checklist)
- Sample posts generation (5 high-quality examples)
- Kill-switch mechanism (file-based and endpoint)

### Security
- Implemented Argon2 password hashing
- Environment-based secret management (no secrets in code)
- Input validation and sanitization
- Rate limiting configuration prepared
- CSP and security headers configured

### Compliance
- LGPD data minimization principles
- Consent tracking database model
- Data retention configuration (12 months default)
- DSAR endpoint skeleton (export, delete, consent)
- DPA template documentation

## [0.1.0] - 2025-10-21

### Added
- Project initialization
- PR1: MVP Generator + Sample Posts + Tests
- Core infrastructure and documentation

---

## Version History

- **0.1.0** (2025-10-21): Initial MVP release - Generator Core
- **Upcoming 0.2.0**: Publisher & Static Site Generation
- **Upcoming 0.3.0**: Tracking & Monetization Layer
- **Upcoming 0.4.0**: Repurposer & Multi-channel
- **Upcoming 0.5.0**: Personalization & Vector Search
- **Upcoming 1.0.0**: Full ecosystem with optimizer & growth tools
