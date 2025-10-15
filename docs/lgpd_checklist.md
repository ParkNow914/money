# LGPD Compliance Checklist

## Overview
This checklist ensures compliance with Brazil's Lei Geral de Proteção de Dados (LGPD) - General Data Protection Law.

## ✅ Data Minimization
- [x] Only collect data absolutely necessary for functionality
- [x] Use hashed identifiers instead of raw PII
- [x] No storage of raw IP addresses (only salted hashes)
- [x] No storage of raw user agents (only hashes)
- [x] Session identifiers are hashed

## ✅ Lawful Basis for Processing
- [x] Consent mechanism implemented (`UserConsent` model)
- [x] Multiple consent types supported (analytics, marketing, required)
- [x] Consent timestamp recorded
- [x] Audit trail maintained (`AuditLog` model)

## ✅ Transparency
- [ ] Privacy policy published (TODO: create and publish)
- [ ] Cookie consent banner implemented (TODO: frontend)
- [ ] Clear explanation of data usage (TODO: frontend)
- [x] API endpoints for data access

## ✅ Data Subject Rights (DSARs)
- [ ] Right to access: `/privacy/export` endpoint (TODO: implement)
- [ ] Right to deletion: `/privacy/delete` endpoint (TODO: implement)
- [ ] Right to rectification: Update endpoints (TODO: implement)
- [ ] Right to data portability: Export in standard format (TODO: implement)
- [ ] Right to withdraw consent: `/privacy/consent` endpoint (TODO: implement)

## ✅ Data Security
- [x] Passwords hashed with Argon2 (configured in dependencies)
- [x] Database encryption ready (SQLAlchemy supports encryption)
- [x] Secrets managed via environment variables (not committed)
- [x] HTTPS recommended for production
- [x] Security headers implemented (CSP, HSTS, etc.)
- [x] Rate limiting capability

## ✅ Data Retention
- [x] Configurable retention period (`DATA_RETENTION_DAYS`)
- [ ] Automated data deletion after retention period (TODO: implement cron job)
- [x] Consent expiration tracking (`expires_at` field)

## ✅ Data Processing Records
- [x] Audit log for all data operations (`AuditLog` model)
- [x] Timestamps on all records
- [x] User actions tracked (consent grants, data exports, deletions)

## ✅ International Data Transfers
- [x] Data stored locally by default (SQLite/PostgreSQL)
- [ ] If using cloud services, ensure LGPD-compliant DPA (TODO: document)
- [ ] Document any third-party data processors

## ✅ Data Protection Officer (DPO)
- [ ] Designate DPO for production deployment
- [ ] Publish DPO contact information
- [ ] Document DPO responsibilities

## ✅ Data Breach Response
- [ ] Incident response plan (TODO: create in operations runbook)
- [ ] Notification procedures (ANPD within 72h, affected users)
- [ ] Breach logging and documentation

## ✅ Child Protection
- [ ] Age verification mechanism if applicable (TODO: if targeting minors)
- [x] Parental consent flow ready to implement if needed

## 🔄 Regular Compliance Activities

### Monthly
- [ ] Review consent records
- [ ] Audit data retention compliance
- [ ] Check for orphaned data

### Quarterly
- [ ] Security audit
- [ ] Update privacy documentation
- [ ] Review third-party processors

### Annually
- [ ] Full LGPD compliance audit
- [ ] Update Data Processing Impact Assessment (DPIA)
- [ ] Review and update DPAs with processors

## Implementation Priorities

### Phase 1 (MVP - Current)
- [x] Data minimization
- [x] Hashed identifiers
- [x] Consent model
- [x] Audit logging

### Phase 2 (Next)
- [ ] DSAR endpoints
- [ ] Privacy policy
- [ ] Cookie consent UI
- [ ] Automated data deletion

### Phase 3 (Production-ready)
- [ ] DPO designation
- [ ] Incident response plan
- [ ] Full documentation
- [ ] Third-party audit

## Resources
- LGPD Official Text: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- ANPD (National Data Protection Authority): https://www.gov.br/anpd/
- LGPD Guidance: https://www.gov.br/anpd/pt-br/assuntos/noticias

## Notes
- This is a living document - update as implementation progresses
- Consult with legal counsel before production deployment
- LGPD applies to any processing of personal data in Brazil, regardless of where the company is located
