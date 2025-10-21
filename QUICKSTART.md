# Quick Start Guide for Reviewers

## Testing PR1 Locally

### Prerequisites
- Docker & Docker Compose installed
- Git
- 10 minutes of your time 😊

### Step-by-Step

```bash
# 1. Clone repository (replace with actual repo URL)
git clone https://github.com/yourusername/autocash-ultimate.git
cd autocash-ultimate

# 2. Checkout PR1 branch
git checkout feature/pr1-mvp-generator

# 3. Create environment file
cp .env.example .env

# Edit .env if needed (defaults work for local testing)
# No need to add real secrets for testing!

# 4. Build and start all services
docker-compose up --build

# Wait for services to be ready (~1-2 minutes)
# You should see: "✅ Database initialized"
```

### Testing the Generator

Open a new terminal while docker-compose is running:

```bash
# Seed keywords from CSV (15 keywords)
docker-compose exec api bash scripts/seed-keywords.sh

# Generate 5 sample articles
docker-compose exec api python -m app.cli generate --count 5

# Export generated articles to JSON
docker-compose exec api python -m app.cli export-posts

# View the results
cat examples/sample_posts.json | jq '.[0]' # View first article (requires jq)
# Or open examples/sample_posts.json in your editor
```

### Running Tests

```bash
# Run all tests with coverage
docker-compose exec api pytest tests/ -v --cov=app --cov-report=term-missing

# Check coverage threshold (must be >= 75%)
docker-compose exec api coverage report --fail-under=75

# View HTML coverage report
docker-compose exec api pytest --cov=app --cov-report=html
# Then open htmlcov/index.html in browser
```

### Testing API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/

# Metrics (Prometheus)
curl http://localhost:8000/metrics
```

### Reviewing Generated Content

1. **Check Quality**:
   - Word count: 700-1200 words ✓
   - Structure: Intro, sections with ##, conclusion ✓
   - SEO: Title, meta description, tags ✓
   - Multi-channel: Video script, X thread ✓

2. **Check Originality**:
   - No duplicate slugs ✓
   - Varied content across articles ✓
   - Similarity check working ✓

3. **Check Compliance**:
   - No raw IPs stored ✓
   - Hashed identifiers only ✓
   - Consent models present ✓

### Cleanup

```bash
# Stop services
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v
```

---

## Expected Output

After running the commands above, you should have:

1. ✅ 15 keywords in database
2. ✅ 5 generated articles
3. ✅ `examples/sample_posts.json` with article data
4. ✅ Test suite passing with >= 75% coverage
5. ✅ All services running healthy

---

## Troubleshooting

**Port conflicts?**
```bash
# Change ports in docker-compose.yml if 8000, 6379, 7700 are taken
```

**Permission errors?**
```bash
# On Linux, might need to adjust file permissions
sudo chown -R $USER:$USER .
```

**Database locked?**
```bash
# Stop and restart
docker-compose restart api
```

---

## What to Review

1. **Code Quality** (`/app`)
   - Clean, readable, well-documented
   - Type hints used
   - Error handling present

2. **Security** (`app/security.py`, `app/crypto_utils.py`)
   - No hardcoded secrets
   - Proper hashing (Argon2, SHA256)
   - Encryption available (AES-256)

3. **Tests** (`/tests`)
   - Comprehensive coverage
   - Clear test names
   - Fixtures used properly

4. **Documentation** (`/docs`, `README.md`)
   - Clear instructions
   - LGPD compliance documented
   - Security measures listed

5. **Generated Content** (`examples/sample_posts.json`)
   - Quality check
   - Originality check
   - Metadata completeness

---

**Questions?** Open a comment on the PR!

**Ready to approve?** Complete the reviewer checklist in PR description.
