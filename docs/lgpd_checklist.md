# LGPD Compliance Checklist

## Lei Geral de Proteção de Dados (LGPD) - Brazil

This checklist ensures AutoCash Ultimate complies with Brazilian data protection law (Lei nº 13.709/2018).

---

## ✅ Data Minimization (Art. 6º, III)

- [x] **Collect only necessary data**: System collects minimal data (hashed identifiers, consent flags)
- [x] **No raw IP storage**: IPs are hashed with salt before storage
- [x] **User agents hashed**: UA strings stored as hashes only
- [x] **Email only on consent**: Email addresses stored only when explicitly provided with consent
- [ ] Regular data audit to verify minimization (TODO: Schedule quarterly audits)

---

## ✅ Consent (Art. 7º, I and Art. 8º)

- [x] **Explicit consent required**: `UserConsent` model tracks all consent
- [x] **Granular consent**: Separate consent for analytics, marketing, necessary processing
- [x] **Consent text recorded**: Full text of what user agreed to is stored
- [x] **Consent timestamp**: `granted_at` field tracks when consent was given
- [x] **Withdrawal mechanism**: `consent_status` can be set to `WITHDRAWN`
- [ ] Double opt-in for email (TODO: Implement email verification flow in future PR)
- [ ] Consent UI modal (TODO: Frontend consent modal in Publisher PR)

**Implementation**:
- `app/models.py`: `UserConsent` model
- `app/models.py`: `ConsentType` and `ConsentStatus` enums

---

## ✅ Purpose Limitation (Art. 6º, I and II)

- [x] **Clear purposes defined**: Analytics, marketing, necessary operations
- [x] **No repurposing without consent**: Consent linked to specific purpose
- [x] **Documented purposes**: Privacy policy documentation (see `dpa_template.md`)

---

## ✅ Data Subject Rights (Arts. 17 and 18)

### Right to Access (Art. 18, II)
- [x] **Data export model**: `DataExportRequest` model created
- [ ] **Export endpoint**: `/api/privacy/export` (TODO: Implement in Privacy PR)
- [x] **Verification flow**: `verification_token` field for secure requests

### Right to Deletion (Art. 18, VI)
- [x] **Deletion model**: `DataExportRequest` supports deletion requests
- [ ] **Deletion endpoint**: `/api/privacy/delete` (TODO: Implement in Privacy PR)
- [x] **Cascade deletes**: Foreign key constraints ensure clean deletion

### Right to Consent Withdrawal (Art. 18, IX)
- [x] **Withdrawal tracking**: `withdrawn_at` field in `UserConsent`
- [ ] **Withdrawal endpoint**: `/api/privacy/consent` (TODO: Implement in Privacy PR)

### Right to Information (Art. 18, I)
- [ ] **Privacy policy page**: Document data processing practices (TODO: Create in Publisher PR)
- [ ] **Transparency report**: Annual report on data processing (TODO: Annual task)

---

## ✅ Security Measures (Art. 46)

- [x] **Encryption at rest**: `crypto_utils.py` provides AES-256 encryption
- [x] **Password hashing**: Argon2 used via `security.py`
- [x] **Secure key management**: Environment variables, never in code
- [x] **Access controls**: JWT-based authentication (skeleton in place)
- [x] **Audit logs**: Consent changes tracked with timestamps
- [ ] **Regular security audits**: Schedule penetration testing (TODO: Before production)
- [ ] **Incident response plan**: Document breach procedures (TODO: `docs/incident_response.md`)

---

## ✅ Data Retention (Art. 16)

- [x] **Configurable retention**: `DATA_RETENTION_DAYS` setting (default 365 days)
- [x] **Consent expiration**: `expires_at` field in `UserConsent`
- [x] **Export link expiration**: `expires_at` for data export downloads
- [ ] **Automated deletion**: Scheduled job to purge expired data (TODO: Cron job in Worker PR)
- [ ] **Retention policy docs**: User-facing documentation (TODO: Privacy policy page)

**Default Retention**:
- User data: 12 months
- Logs: 90 days
- Export links: 7 days
- Analytics (hashed): 12 months

---

## ✅ International Data Transfer (Arts. 33-36)

- [x] **Data localization preference**: Designed for Brazil-hosted infrastructure (Oracle São Paulo)
- [ ] **DPA for processors**: If using third-party services, execute DPAs (see `dpa_template.md`)
- [ ] **Adequacy assessment**: Document if transferring data outside Brazil (TODO: If applicable)

---

## ✅ Data Processing Records (Art. 37)

- [x] **Processing activities documented**: This checklist + DPA template
- [x] **Legal basis documented**: Consent (Art. 7º, I) for analytics/marketing
- [x] **Data categories documented**: Hashed identifiers, emails (with consent), behavioral data
- [ ] **ROPA (Record of Processing Activities)**: Maintain current ROPA (TODO: Annual update)

---

## ✅ Data Protection Officer (DPO) - If Required (Arts. 41-42)

**Note**: DPO is mandatory only for:
- Public administration
- Large-scale data processing
- Sensitive data as core activity

For small/medium operations:
- [ ] **Designate responsible contact**: Add email/contact to privacy policy
- [ ] **Monitor for threshold**: If reaching large-scale, appoint DPO

---

## ✅ Privacy by Design (Art. 46, §2º)

- [x] **Designed with privacy first**: Hashing, minimal collection, consent-first
- [x] **Default privacy settings**: `review_required=true`, analytics opt-in
- [x] **Regular reviews**: Security and privacy code reviews in CI

---

## 🔄 Ongoing Compliance Tasks

### Monthly
- [ ] Review consent withdrawal requests
- [ ] Check DSAR queue and processing times (target: < 7 days)
- [ ] Audit access logs for anomalies

### Quarterly
- [ ] Data minimization audit (remove unnecessary fields)
- [ ] Review third-party processors and DPAs
- [ ] Update privacy policy if practices change

### Annually
- [ ] Full LGPD compliance audit
- [ ] Update ROPA
- [ ] Review and test incident response plan
- [ ] Data retention policy review

---

## 📋 Implementation Roadmap

### ✅ Phase 1: Foundation (Current - PR1)
- [x] Database models with consent tracking
- [x] Privacy-preserving identifiers
- [x] Security utilities (hashing, encryption)

### Phase 2: Privacy APIs (Future PRs)
- [ ] `/api/privacy/export` endpoint
- [ ] `/api/privacy/delete` endpoint
- [ ] `/api/privacy/consent` management
- [ ] Email verification flow

### Phase 3: User Interfaces
- [ ] Consent modal on site
- [ ] Privacy dashboard for users
- [ ] Cookie preferences UI

### Phase 4: Automation
- [ ] Scheduled data purging
- [ ] Automated consent expiration
- [ ] DSAR fulfillment automation

---

## 📄 Related Documents

- [DPA Template](./dpa_template.md) - For third-party processors
- [Security Checklist](./security_checklist.md) - Technical security measures
- [Operations Runbook](./operations_runbook.md) - Incident response procedures

---

## ⚖️ Legal Basis Reference

**Article 7º, LGPD** - Data processing is lawful when:
- **I - Consent**: Explicit, informed, unambiguous (our primary basis)
- **II - Legal obligation**: Compliance with laws
- **IX - Legitimate interest**: Where balanced with data subject rights

AutoCash Ultimate primarily relies on **Article 7º, I (Consent)** for analytics and marketing, and **Article 7º, IX (Legitimate Interest)** for necessary operational processing (fraud prevention, security).

---

**Last Updated**: 2025-10-21  
**Next Review**: 2026-01-21 (Quarterly)  
**Owner**: Project Maintainer / DPO (if appointed)
