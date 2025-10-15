# Production Deployment Checklist

## Pre-Deployment

### 1. Environment Configuration
- [ ] Copy `.env.production` to `.env`
- [ ] Generate strong secrets with `openssl rand -hex 32`
- [ ] Update `SECRET_KEY`, `ADMIN_TOKEN`, `IP_SALT`
- [ ] Configure database connection (PostgreSQL recommended)
- [ ] Set `ALLOWED_ORIGINS` to your domain(s)
- [ ] Review and adjust `DATA_RETENTION_DAYS`

### 2. Infrastructure Setup
- [ ] Provision Oracle Cloud VM (or alternative)
- [ ] Configure security groups (ports 22, 80, 443)
- [ ] Set up domain DNS records
- [ ] Configure Cloudflare (optional but recommended)

### 3. Server Preparation
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Install Docker: `curl -fsSL https://get.docker.com | sh`
- [ ] Install Docker Compose
- [ ] Install Nginx: `sudo apt install nginx -y`
- [ ] Install Certbot: `sudo apt install certbot python3-certbot-nginx -y`

## Deployment

### 4. Application Deployment
```bash
# Clone repository
git clone https://github.com/ParkNow914/money.git /home/ubuntu/autocash-ultimate
cd /home/ubuntu/autocash-ultimate

# Configure environment
cp .env.production .env
nano .env  # Edit with production values

# Build and start
docker-compose -f docker/docker-compose.yml up -d --build

# Verify
curl http://localhost:8000/health
```

### 5. SSL/HTTPS Setup
```bash
# Copy nginx configuration
sudo cp nginx/autocash.conf /etc/nginx/sites-available/autocash

# Edit domain name in config
sudo nano /etc/nginx/sites-available/autocash

# Enable site
sudo ln -s /etc/nginx/sites-available/autocash /etc/nginx/sites-enabled/

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 6. Automated Backups
```bash
# Setup backup cron job
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/autocash-ultimate/scripts/backup.sh") | crontab -

# Test backup
./scripts/backup.sh
```

### 7. Monitoring Setup
```bash
# Install monitoring tools (optional)
sudo apt install htop nethogs iotop -y

# Check logs
docker-compose -f docker/docker-compose.yml logs -f
```

## Post-Deployment

### 8. Security Hardening
- [ ] Configure firewall: `sudo ufw allow 22,80,443/tcp && sudo ufw enable`
- [ ] Install fail2ban: `sudo apt install fail2ban -y`
- [ ] Enable automatic security updates
- [ ] Set up SSH key authentication (disable password auth)
- [ ] Review security checklist: `docs/security_checklist.md`

### 9. LGPD Compliance
- [ ] Review LGPD checklist: `docs/lgpd_checklist.md`
- [ ] Publish privacy policy
- [ ] Configure cookie consent (if using frontend)
- [ ] Test DSAR endpoints
- [ ] Document data processing activities

### 10. Content Generation
```bash
# Seed keywords
./scripts/seed-keywords.sh

# Test generation
curl -X POST https://yourdomain.com/api/generate \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "test keyword"}'

# View generated content
curl https://yourdomain.com/api/articles
```

### 11. Automation Setup

#### Option A: Cloudflare Workers
```bash
cd workers
wrangler login
wrangler deploy
```

#### Option B: Systemd Timer
```bash
sudo cp scripts/systemd/generator.service /etc/systemd/system/
sudo cp scripts/systemd/generator.timer /etc/systemd/system/
sudo systemctl enable generator.timer
sudo systemctl start generator.timer
sudo systemctl status generator.timer
```

### 12. Monitoring & Alerts
- [ ] Configure uptime monitoring (UptimeRobot, etc.)
- [ ] Set up log rotation
- [ ] Configure alerts for errors
- [ ] Monitor disk space
- [ ] Monitor API response times

## Ongoing Maintenance

### Daily
- [ ] Check health endpoint
- [ ] Review error logs
- [ ] Monitor disk space

### Weekly
- [ ] Review generated content quality
- [ ] Check backup integrity
- [ ] Review security logs
- [ ] Monitor traffic and performance

### Monthly
- [ ] Update dependencies
- [ ] Security audit
- [ ] Review LGPD compliance
- [ ] Optimize database
- [ ] Review and rotate logs

## Rollback Procedure

If issues occur:

```bash
# Stop services
docker-compose -f docker/docker-compose.yml down

# Restore from backup
cp /var/backups/autocash/autocash_backup_YYYYMMDD_HHMMSS.db.gz .
gunzip autocash_backup_YYYYMMDD_HHMMSS.db.gz
mv autocash_backup_YYYYMMDD_HHMMSS.db autocash.db

# Restart services
docker-compose -f docker/docker-compose.yml up -d

# Check logs
docker-compose -f docker/docker-compose.yml logs -f
```

## Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs

# Check environment
docker-compose config

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database issues
```bash
# Check database file
ls -lh autocash.db

# Check connections
docker-compose exec app python -c "from app.db import engine; print(engine.pool.status())"
```

### SSL issues
```bash
# Renew certificate
sudo certbot renew

# Check nginx
sudo nginx -t
sudo systemctl status nginx
```

## Performance Optimization

### Database
```bash
# Optimize SQLite
sqlite3 autocash.db "VACUUM;"
sqlite3 autocash.db "ANALYZE;"

# Or migrate to PostgreSQL for better performance
```

### Caching
- Enable Redis for caching (optional)
- Configure Cloudflare page rules
- Use CDN for static assets

### Scaling
- Increase Docker container resources
- Add read replicas for database
- Use load balancer for multiple instances
- Enable horizontal pod autoscaling

## Success Criteria

✅ System is running and accessible via HTTPS
✅ Health check returns 200 OK
✅ SSL certificate is valid
✅ Backups are running daily
✅ Content generation works
✅ All LGPD endpoints functional
✅ Monitoring is active
✅ Logs are accessible and rotated
✅ Security headers are present
✅ Kill switch is tested and working

## Support

- Documentation: `/docs` directory
- Health check: `https://yourdomain.com/health`
- API docs: `https://yourdomain.com/docs` (disable in production)
- Logs: `docker-compose logs -f`

---

Last updated: 2025-10-15
