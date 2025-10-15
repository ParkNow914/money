# Changelog

All notable changes to the autocash-ultimate project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-10-15

### Added
- **Content Repurposer Service**: Transform articles into multiple formats
  - Twitter/X threads with engagement hooks
  - Video scripts with timestamps and b-roll suggestions
  - Email newsletters with CTAs
  - PDF document outlines
- **Static Site Publisher**: Generate SEO-optimized HTML files
  - Jinja2 template system
  - Batch publishing capabilities
  - Index page generation
- **DSAR Endpoints**: Complete LGPD compliance implementation
  - Full data export in JSON format
  - Right to deletion with audit trail
  - Consent management
- **API Routes**:
  - `/api/publish` - Publish single article
  - `/api/publish-batch` - Batch publish multiple articles
  - `/api/publish/status` - Get publishing status
  - `/api/repurpose` - Repurpose content to different formats
  - `/api/repurpose/{slug}` - Get repurposed content
  - `/api/repurpose/formats` - List supported formats
  - `/api/privacy/export` - Complete data export
  - `/api/privacy/delete` - Delete user data
- **Tests**: Added 19 new tests (publisher, repurposer, privacy)
  - Total test count: 41 tests
  - Test coverage maintained >75%

### Changed
- Content generator now produces 1 paragraph per section (700-1200 words)
- Updated requirements.txt with email-validator dependency
- README updated with Phase 2 completion status

### Fixed
- Word count validation in content generator
- All tests now passing (41/41)

## [0.1.0] - 2025-10-15

### Added
- Initial repository structure
- MVP content generator service
- FastAPI backend with basic routes
- SQLite database with core models
- Privacy-first tracking with LGPD compliance
- Docker development environment
- Unit tests with pytest
- CI/CD workflows with GitHub Actions
- LGPD and security documentation
- Sample keyword seeds for content generation
- Example generated content (5 posts)

### Security
- No secrets committed (using environment variables)
- Privacy-by-design with consent management
- Hashed identifiers for analytics
- review_required=true by default for all generated content

## [0.1.0] - 2025-10-15

### Added
- Project initialization
- Core directory structure
- Basic documentation
