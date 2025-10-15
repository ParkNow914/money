# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will have you running autocash-ultimate locally in 5 minutes.

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- 5 minutes of your time

### Step 1: Clone & Setup (1 minute)

```bash
# Clone the repository
git clone https://github.com/ParkNow914/money.git
cd money

# Create environment file
cp .env.example .env
```

### Step 2: Generate Secrets (1 minute)

```bash
# Generate secrets
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "ADMIN_TOKEN=$(openssl rand -hex 32)" >> .env
echo "IP_SALT=$(openssl rand -hex 32)" >> .env
```

### Step 3: Start Services (2 minutes)

```bash
# Build and start
docker-compose -f docker/docker-compose.yml up --build -d

# Wait for services to start
sleep 10

# Check health
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T...",
  "version": "0.1.0"
}
```

### Step 4: Seed Keywords (30 seconds)

```bash
# Make script executable
chmod +x scripts/seed-keywords.sh

# Run it
./scripts/seed-keywords.sh
```

### Step 5: Generate Your First Article (30 seconds)

```bash
# Get your admin token from .env
ADMIN_TOKEN=$(grep ADMIN_TOKEN .env | cut -d'=' -f2)

# Generate an article
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: ****** ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "digital marketing"}'
```

### 🎉 Success!

You now have:
- ✅ autocash-ultimate running locally
- ✅ Database initialized
- ✅ Keywords loaded
- ✅ First article generated

## 📋 What's Next?

### View Your Content

```bash
# List all articles
curl http://localhost:8000/api/articles | jq .

# View specific article
curl http://localhost:8000/api/articles/digital-marketing-... | jq .
```

### Generate More Content

```bash
# Batch generate 5 articles
curl -X POST http://localhost:8000/api/batch-generate \
  -H "Authorization: ****** ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count": 5}'
```

### Check System Status

```bash
# Admin dashboard
curl -H "Authorization: ****** ${ADMIN_TOKEN}" \
  http://localhost:8000/api/admin/status | jq .

# Business metrics
curl http://localhost:8000/api/stats | jq .
```

### Run Revenue Projections

```bash
python3 tools/projections.py
```

## 🔧 Common Operations

### View Logs
```bash
docker-compose -f docker/docker-compose.yml logs -f
```

### Stop Services
```bash
docker-compose -f docker/docker-compose.yml down
```

### Restart Services
```bash
docker-compose -f docker/docker-compose.yml restart
```

### Access Database
```bash
sqlite3 autocash.db
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **Health**: http://localhost:8000/health
- **Docs**: http://localhost:8000/docs (interactive API documentation)
- **Metrics**: http://localhost:8000/api/metrics (Prometheus format)
- **Admin**: http://localhost:8000/api/admin/status (requires auth)

## 📊 Test the Full Stack

### 1. Content Generation
```bash
# Generate article
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: ****** ${ADMIN_TOKEN}" \
  -d '{"keyword": "productivity tips"}' | jq .
```

### 2. Privacy/LGPD Features
```bash
# Grant consent
curl -X POST http://localhost:8000/api/privacy/consent \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "consent_type": "analytics", "granted": true}' | jq .

# View consents
curl http://localhost:8000/api/privacy/consents/user@example.com | jq .
```

### 3. Tracking & Analytics
```bash
# Track an event
curl -X POST http://localhost:8000/api/tracking/event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "view", "article_slug": "your-slug"}' | jq .

# Get article stats
curl http://localhost:8000/api/tracking/stats/your-slug | jq .
```

### 4. Admin Operations
```bash
# Get system status
curl -H "Authorization: ****** ${ADMIN_TOKEN}" \
  http://localhost:8000/api/admin/status | jq .

# Cleanup old data (90 days)
curl -X POST -H "Authorization: ****** ${ADMIN_TOKEN}" \
  "http://localhost:8000/api/admin/cleanup?days=90" | jq .
```

## 🎯 Next Steps

1. **Review Generated Content**: Check `examples/sample_posts.json`
2. **Customize Configuration**: Edit `.env` file
3. **Add More Keywords**: Edit `data/keywords_seed.csv`
4. **Setup Monitoring**: Run `./scripts/monitor.sh`
5. **Plan Deployment**: Read `docs/production_checklist.md`

## 🆘 Troubleshooting

### Services won't start
```bash
# Check Docker
docker --version
docker-compose --version

# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Can't generate content
```bash
# Check kill switch
curl http://localhost:8000/health | jq '.kill_switch'

# Check keywords
curl http://localhost:8000/api/keywords | jq .

# Check logs
docker-compose logs app
```

### Database issues
```bash
# Check database file
ls -lh autocash.db

# Recreate database
rm autocash.db
docker-compose restart
```

## 📚 Learn More

- [Full README](README.md) - Complete documentation
- [LGPD Checklist](docs/lgpd_checklist.md) - Privacy compliance
- [Security Guide](docs/security_checklist.md) - Security best practices
- [Production Deployment](docs/production_checklist.md) - Deploy to production
- [Operations Runbook](docs/operations_runbook.md) - Day-to-day operations

## 💡 Pro Tips

1. **Enable JSON Logs**: Set `DEBUG=false` in `.env` for production-ready JSON logs
2. **Use PostgreSQL**: For production, migrate to PostgreSQL for better performance
3. **Setup Backups**: Run `./scripts/backup.sh` to test backup functionality
4. **Monitor Health**: Setup a cron job for `./scripts/monitor.sh`
5. **Review Content**: All content has `review_required=true` by default - review before publishing!

## ⚖️ Remember

- ✅ This is an **ethical, legal platform**
- ✅ **No fraudulent practices** - ever
- ✅ **Review content** before publication
- ✅ **LGPD compliant** by design
- ✅ **Privacy-first** always

---

**Ready to deploy?** See [Production Checklist](docs/production_checklist.md)

**Need help?** Check [Operations Runbook](docs/operations_runbook.md)
