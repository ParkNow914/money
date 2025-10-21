# Installation Guide

## Quick Install (Recommended)

### Windows (PowerShell)

```powershell
# Run automated setup
.\setup.ps1
```

### Linux/Mac (Bash)

```bash
# Make executable and run
chmod +x setup.sh
./setup.sh
```

The setup script will:
1. Create `.env` from template
2. Build Docker containers
3. Start all services
4. Seed 15 keywords
5. Generate 5 sample articles
6. Export to `examples/sample_posts.json`

---

## Manual Installation

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- Git
- Python 3.11+ (for local development without Docker)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/autocash-ultimate.git
cd autocash-ultimate
```

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your preferred editor
# IMPORTANT: Change SECRET_KEY and ENCRYPTION_KEY in production!
```

### Step 3: Start Services with Docker

```bash
# Build containers
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Step 4: Seed Keywords

**Windows:**
```powershell
docker-compose exec api powershell -ExecutionPolicy Bypass -File scripts/seed-keywords.ps1
```

**Linux/Mac:**
```bash
docker-compose exec api bash scripts/seed-keywords.sh
```

### Step 5: Generate Sample Content

```bash
# Generate 5 articles
docker-compose exec api python -m app.cli generate --count 5

# Export to JSON
docker-compose exec api python -m app.cli export-posts
```

### Step 6: Verify Installation

```bash
# Run health check
curl http://localhost:8000/health

# Run tests
docker-compose exec api pytest tests/ -v --cov=app

# Check coverage (should be >= 75%)
docker-compose exec api coverage report
```

---

## Local Development (Without Docker)

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env
cp .env.example .env

# Initialize database
python -c "import asyncio; from app.db import init_db; asyncio.run(init_db())"

# Seed keywords
python scripts/seed-keywords.ps1  # Windows
# OR
bash scripts/seed-keywords.sh     # Linux/Mac

# Start application
python -m app.main
```

### Running Tests Locally

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Troubleshooting

### Docker Build Fails

```bash
# Clean build
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Port Conflicts

Edit `docker-compose.yml` to change ports:
- API: 8000 → your port
- Redis: 6379 → your port
- MeiliSearch: 7700 → your port

### Permission Errors (Linux)

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run Docker commands with sudo
sudo docker-compose up -d
```

### Database Locked

```bash
# Restart API service
docker-compose restart api
```

### Services Won't Start

```bash
# Check Docker status
docker ps

# Check logs for errors
docker-compose logs api
docker-compose logs redis
docker-compose logs meilisearch
```

---

## Monitoring Services

### Access Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Prometheus Metrics**: http://localhost:8000/metrics
- **MeiliSearch**: http://localhost:7700
- **Grafana** (optional): http://localhost:3000
- **Prometheus** (optional): http://localhost:9090

### Enable Monitoring Stack

```bash
# Start with monitoring services
docker-compose --profile monitoring up -d
```

---

## Production Deployment

### Before Deploying

1. **Change Secrets**:
   ```bash
   # Generate new SECRET_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Generate new ENCRYPTION_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update .env**:
   ```
   ENVIRONMENT=production
   DEBUG=false
   SECRET_KEY=<new-secret>
   ENCRYPTION_KEY=<new-encryption-key>
   DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
   ```

3. **Security Checklist**:
   - [ ] All secrets changed from defaults
   - [ ] HTTPS enabled (Nginx/Cloudflare)
   - [ ] Firewall configured
   - [ ] Rate limiting enabled
   - [ ] Backups configured
   - [ ] Monitoring active

4. **Run Security Scans**:
   ```bash
   # SAST
   docker-compose exec api bandit -r app/
   
   # Dependency check
   docker-compose exec api safety check
   ```

---

## Uninstallation

### Stop and Remove Services

```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data!)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Remove Local Files

```bash
# Remove all generated data
rm -rf data/ logs/ chroma_data/ storage/ examples/sample_posts.json

# Keep source code, remove everything else
git clean -fdx  # WARNING: removes all untracked files!
```

---

## Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: [GitHub Issues](https://github.com/yourusername/autocash-ultimate/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autocash-ultimate/discussions)

---

**Next**: See [QUICKSTART.md](./QUICKSTART.md) for testing guide
