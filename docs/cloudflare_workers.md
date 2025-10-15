# Cloudflare Workers Setup

## Overview
Cloudflare Workers enable serverless automation for autocash-ultimate, including scheduled content generation and edge functions.

## Features
- **Cron Jobs**: Scheduled content generation
- **Edge Computing**: Low-latency request handling
- **Free Tier**: 100,000 requests/day

## Setup

### 1. Install Wrangler CLI
```bash
npm install -g wrangler
```

### 2. Authenticate
```bash
wrangler login
```

### 3. Configure Worker

Create `wrangler.toml`:
```toml
name = "autocash-cron"
main = "workers/cron.js"
compatibility_date = "2024-01-01"

[vars]
API_URL = "https://yourdomain.com"

# Set in dashboard or via secrets
# ADMIN_TOKEN = "your-secret-token"

# Cron trigger - every 12 hours
[triggers]
crons = ["0 */12 * * *"]
```

### 4. Set Secrets
```bash
# Set admin token securely
wrangler secret put ADMIN_TOKEN
```

### 5. Deploy
```bash
wrangler deploy
```

## Cron Schedule Examples

```
"0 */6 * * *"   # Every 6 hours
"0 */12 * * *"  # Every 12 hours
"0 0 * * *"     # Daily at midnight
"0 2 * * *"     # Daily at 2 AM
"0 0 * * 1"     # Weekly on Monday
```

## Testing Locally

```bash
# Test worker locally
wrangler dev

# Trigger cron manually
curl http://localhost:8787/__scheduled
```

## Monitoring

View logs in Cloudflare Dashboard:
1. Go to Workers & Pages
2. Select your worker
3. Click "Logs" tab

## Cost

Free tier includes:
- 100,000 requests/day
- 10ms CPU time per request
- Cron triggers: unlimited

Paid plan ($5/month):
- 10 million requests/month
- 50ms CPU time
- Additional features

## Security

- Store ADMIN_TOKEN as secret (never in code)
- Verify API responses
- Monitor for anomalies
- Rate limit if needed

## Troubleshooting

**Worker not triggering**:
- Check cron syntax
- Verify worker is deployed
- Check Cloudflare dashboard logs

**API authentication failing**:
- Verify ADMIN_TOKEN secret is set
- Check token format in header
- Verify API endpoint URL

**Kill switch preventing execution**:
- Check /health endpoint
- Verify kill_switch flag status
- Disable if appropriate

## Alternative: Systemd Timer

If not using Cloudflare Workers, use systemd timer on Oracle VM:

```bash
# See scripts/generator-timer.service
sudo cp scripts/generator-timer.service /etc/systemd/system/
sudo systemctl enable generator-timer.service
sudo systemctl start generator-timer.service
```

## References
- Cloudflare Workers Docs: https://developers.cloudflare.com/workers/
- Wrangler Docs: https://developers.cloudflare.com/workers/wrangler/
- Cron Trigger Docs: https://developers.cloudflare.com/workers/configuration/cron-triggers/
