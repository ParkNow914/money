# Oracle Cloud Free Tier Deployment Guide

## Overview
Deploy autocash-ultimate to Oracle Cloud Free Tier (Always Free resources).

## Prerequisites
- Oracle Cloud account (free tier)
- Domain name (optional, can use Cloudflare Pages)
- GitHub account for CI/CD

## Oracle Free Tier Resources
- **Compute**: 2 AMD VM instances (1/8 OCPU, 1 GB RAM each) OR 4 Arm-based Ampere A1 cores and 24 GB RAM
- **Block Storage**: 200 GB total
- **Object Storage**: 10 GB
- **Network**: 10 TB outbound data transfer per month

## Step 1: Create Oracle Cloud VM

### 1.1 Create Compute Instance
```bash
# Via OCI CLI (or use web console)
oci compute instance launch \
  --availability-domain <AD> \
  --compartment-id <compartment-id> \
  --shape VM.Standard.E2.1.Micro \
  --image-id <ubuntu-22.04-image-id> \
  --subnet-id <subnet-id> \
  --display-name autocash-ultimate
```

### 1.2 Configure Security Rules
Allow inbound traffic:
- Port 22 (SSH)
- Port 80 (HTTP)
- Port 443 (HTTPS)

## Step 2: Setup VM

### 2.1 Connect to VM
```bash
ssh -i ~/.ssh/oracle_key ubuntu@<public-ip>
```

### 2.2 Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for docker group to take effect
```

## Step 3: Deploy Application

### 3.1 Clone Repository
```bash
git clone https://github.com/ParkNow914/money.git
cd money
```

### 3.2 Configure Environment
```bash
# Create .env file
cp .env.example .env

# Edit with production values
nano .env

# IMPORTANT: Set strong secrets!
# Generate random values:
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For ADMIN_TOKEN
openssl rand -hex 16  # For IP_SALT
```

### 3.3 Start Services
```bash
# Start with Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Check logs
docker-compose -f docker/docker-compose.yml logs -f

# Verify health
curl http://localhost:8000/health
```

## Step 4: Configure Cloudflare

### 4.1 DNS Setup
Point your domain to Oracle VM IP:
```
A    @              <oracle-vm-ip>
A    www            <oracle-vm-ip>
AAAA @              <oracle-vm-ipv6>  (if available)
```

### 4.2 Enable Cloudflare Proxy
- Orange cloud: ON (proxied)
- SSL/TLS: Full (strict) after configuring Let's Encrypt

### 4.3 Configure Firewall Rules
- Rate limiting: 60 requests/minute per IP
- DDoS protection: Enabled
- Bot fight mode: ON

## Step 5: SSL Certificate

### 5.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 Get Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.3 Auto-renewal
Certbot automatically sets up cron job for renewal.

## Step 6: Configure Backups

### 6.1 Database Backup Script
```bash
# Create backup script
cat > /home/ubuntu/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/home/ubuntu/backups
mkdir -p $BACKUP_DIR

# Backup database
docker exec autocash-app cp /app/autocash.db /tmp/backup.db
docker cp autocash-app:/tmp/backup.db $BACKUP_DIR/autocash_$DATE.db

# Keep only last 30 days
find $BACKUP_DIR -name "autocash_*.db" -mtime +30 -delete

# Upload to Object Storage (optional)
# oci os object put --bucket-name autocash-backups --file $BACKUP_DIR/autocash_$DATE.db
EOF

chmod +x /home/ubuntu/backup.sh
```

### 6.2 Setup Cron
```bash
# Run backup daily at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/backup.sh") | crontab -
```

## Step 7: Monitoring

### 7.1 Health Check Cron
```bash
# Create health check script
cat > /home/ubuntu/health_check.sh << 'EOF'
#!/bin/bash
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Health check failed - restarting services"
    cd /home/ubuntu/money
    docker-compose -f docker/docker-compose.yml restart
fi
EOF

chmod +x /home/ubuntu/health_check.sh

# Run every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/ubuntu/health_check.sh") | crontab -
```

## Step 8: Security Hardening

### 8.1 Firewall
```bash
# UFW firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 8.2 Fail2ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

### 8.3 Automatic Updates
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

## Step 9: Cloudflare Workers (Optional)

### 9.1 Create Worker for Cron
```javascript
// workers/cron.js
export default {
  async scheduled(event, env, ctx) {
    // Call batch generation endpoint
    const response = await fetch('https://yourdomain.com/api/batch-generate', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.ADMIN_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        count: 5
      })
    });
    
    console.log('Batch generation triggered:', response.status);
  }
}
```

### 9.2 Configure Trigger
- Cron schedule: `0 */12 * * *` (every 12 hours)
- Environment variables: Set ADMIN_TOKEN

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check memory
free -h
```

### Database Locked
```bash
# Stop services
docker-compose down

# Remove lock
rm autocash.db-journal

# Restart
docker-compose up -d
```

### High Memory Usage
```bash
# Restart services
docker-compose restart

# Check container stats
docker stats
```

## Cost Optimization
- Use Oracle Free Tier (always free)
- Cloudflare Free plan for CDN/DDoS
- Let's Encrypt for free SSL
- Self-hosted analytics (Matomo/Plausible)

**Total Monthly Cost**: $0 (using free tiers)

## Scaling Path
When outgrowing free tier:
1. Upgrade to larger Oracle VM ($10-20/month)
2. Add PostgreSQL managed database ($15/month)
3. Add Redis cache ($10/month)
4. Cloudflare Pro for advanced DDoS ($20/month)
5. CDN for static assets

## Support
- Oracle Cloud Support: https://cloud.oracle.com/support
- Community: GitHub Issues
- Documentation: /docs folder

---

Last updated: 2025-10-15
