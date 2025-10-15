# Operations Runbook

## Overview
This runbook provides operational procedures for managing the autocash-ultimate platform.

## 🚀 Deployment

### Local Development
```bash
# Start services
docker-compose -f docker/docker-compose.yml up --build

# Check logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Production Deployment
See [deploy_oracle.md](deploy_oracle.md) for Oracle Cloud deployment.

## 🔍 Monitoring

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# Metrics (Prometheus format)
curl http://localhost:8000/api/metrics

# Business stats
curl http://localhost:8000/api/stats
```

### Log Files
- Application logs: `logs/app.log`
- Access logs: `logs/access.log`
- Error logs: `logs/error.log`

## 🛡️ Security Operations

### Kill Switch Activation
When emergency stop is needed:

1. **Via Environment Variable**:
   ```bash
   export KILL_SWITCH_ENABLED=true
   # Restart application
   docker-compose restart
   ```

2. **Via Admin Endpoint** (Future implementation):
   ```bash
   # TODO: Implement admin killswitch endpoint
   # curl -X POST http://localhost:8000/admin/killswitch \
   #   -H "Authorization: Bearer $ADMIN_TOKEN"
   ```

3. **Verify Kill Switch**:
   ```bash
   curl http://localhost:8000/health | jq .kill_switch
   ```

### Incident Response

#### Security Breach
1. **Immediate**: Activate kill switch
2. **Assess**: Check logs for suspicious activity
3. **Contain**: Isolate affected systems
4. **Notify**: Contact DPO and legal team
5. **Document**: Log all actions in audit trail
6. **Report**: File ANPD notification within 72h if PII exposed

#### Performance Issues
1. Check metrics: `curl http://localhost:8000/api/stats`
2. Review logs: `docker-compose logs -f`
3. Check database size: `ls -lh *.db`
4. Monitor resource usage: `docker stats`

## 📊 Routine Operations

### Daily
- [ ] Check health endpoints
- [ ] Review error logs
- [ ] Monitor disk space
- [ ] Check kill switch status

### Weekly
- [ ] Review generated content quality
- [ ] Analyze traffic and engagement metrics
- [ ] Check for failed jobs
- [ ] Review security logs

### Monthly
- [ ] Full security audit
- [ ] Update dependencies
- [ ] Review LGPD compliance
- [ ] Backup verification
- [ ] Performance optimization

## 💾 Backup & Recovery

### Manual Backup
```bash
# Backup database
cp autocash.db backups/autocash_$(date +%Y%m%d_%H%M%S).db

# Backup generated content
tar -czf backups/content_$(date +%Y%m%d).tar.gz examples/ site-out/

# Backup configuration
tar -czf backups/config_$(date +%Y%m%d).tar.gz .env docker/ scripts/
```

### Restore from Backup
```bash
# Stop services
docker-compose down

# Restore database
cp backups/autocash_YYYYMMDD_HHMMSS.db autocash.db

# Restore content
tar -xzf backups/content_YYYYMMDD.tar.gz

# Restart services
docker-compose up -d
```

## 🔧 Maintenance Tasks

### Clear Old Data (LGPD Retention)
```python
# TODO: Implement data retention cleanup script
# python scripts/cleanup_old_data.py --days 365

# Manual cleanup for now:
# Delete old tracking events
# DELETE FROM tracking_events WHERE created_at < date('now', '-365 days');
```

### Regenerate Content
```bash
# Regenerate specific article
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"keyword": "your keyword"}'
```

### Database Optimization
```bash
# SQLite vacuum
sqlite3 autocash.db "VACUUM;"

# Analyze for query optimization
sqlite3 autocash.db "ANALYZE;"
```

## 📈 Scaling Operations

### Horizontal Scaling
1. Deploy multiple instances behind load balancer
2. Use shared PostgreSQL database
3. Configure Redis for distributed cache
4. Use object storage for generated content

### Vertical Scaling
1. Increase container resources in docker-compose.yml
2. Optimize database queries
3. Add database indexes
4. Enable caching

## 🚨 Alerts & Notifications

### Critical Alerts (Immediate Action)
- Kill switch activated
- Database errors
- Security breach detected
- API downtime > 5 minutes

### Warning Alerts (Review within 24h)
- High error rate (>5%)
- Disk space > 80%
- Memory usage > 90%
- Failed backup

### Info Alerts (Review weekly)
- New content generated
- Traffic milestones
- Update available

## 📞 Contact Information

### Emergency Contacts
- **Technical Lead**: [Contact Info]
- **Security Officer**: [Contact Info]
- **DPO (LGPD)**: [Contact Info]
- **Legal**: [Contact Info]

### External Services
- **Oracle Cloud Support**: [Link]
- **Cloudflare Support**: [Link]
- **DNS Provider**: [Link]

## 📚 Additional Resources
- [LGPD Checklist](lgpd_checklist.md)
- [Security Checklist](security_checklist.md)
- [Deployment Guide](deploy_oracle.md)
- [API Documentation](http://localhost:8000/docs)

## 🔄 Change Log
Track all operational changes in this section:

- **2025-10-15**: Initial runbook created
