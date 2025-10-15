#!/bin/bash
#
# Monitoring script for autocash-ultimate
# Checks system health and sends alerts if needed
#

set -e

API_URL="${API_URL:-http://localhost:8000}"
ALERT_EMAIL="${ALERT_EMAIL:-}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

send_alert() {
    local message="$1"
    
    # Send to Telegram if configured
    if [ ! -z "$TELEGRAM_BOT_TOKEN" ] && [ ! -z "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=🚨 autocash-ultimate Alert: ${message}" \
            > /dev/null 2>&1
    fi
    
    # Send email if configured
    if [ ! -z "$ALERT_EMAIL" ]; then
        echo "$message" | mail -s "autocash-ultimate Alert" "$ALERT_EMAIL" 2>/dev/null || true
    fi
}

check_health() {
    log_info "Checking API health..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" || echo "000")
    
    if [ "$response" = "200" ]; then
        log_info "✅ API is healthy (HTTP $response)"
        return 0
    else
        log_error "❌ API health check failed (HTTP $response)"
        send_alert "API health check failed with HTTP $response"
        return 1
    fi
}

check_disk_space() {
    log_info "Checking disk space..."
    
    usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$usage" -gt 90 ]; then
        log_error "❌ Disk usage critical: ${usage}%"
        send_alert "Disk usage is at ${usage}%"
        return 1
    elif [ "$usage" -gt 80 ]; then
        log_warn "⚠️  Disk usage warning: ${usage}%"
        return 0
    else
        log_info "✅ Disk usage OK: ${usage}%"
        return 0
    fi
}

check_memory() {
    log_info "Checking memory usage..."
    
    mem_usage=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
    
    if [ "$mem_usage" -gt 90 ]; then
        log_error "❌ Memory usage critical: ${mem_usage}%"
        send_alert "Memory usage is at ${mem_usage}%"
        return 1
    elif [ "$mem_usage" -gt 80 ]; then
        log_warn "⚠️  Memory usage warning: ${mem_usage}%"
        return 0
    else
        log_info "✅ Memory usage OK: ${mem_usage}%"
        return 0
    fi
}

check_docker_containers() {
    log_info "Checking Docker containers..."
    
    if ! command -v docker &> /dev/null; then
        log_warn "Docker not found, skipping container check"
        return 0
    fi
    
    running=$(docker ps --filter "name=autocash" --format "{{.Names}}" | wc -l)
    
    if [ "$running" -eq 0 ]; then
        log_error "❌ No autocash containers running"
        send_alert "No autocash Docker containers are running"
        return 1
    else
        log_info "✅ $running autocash container(s) running"
        return 0
    fi
}

check_database() {
    log_info "Checking database..."
    
    if [ -f "autocash.db" ]; then
        size=$(du -h autocash.db | cut -f1)
        log_info "✅ Database file exists (size: $size)"
        return 0
    else
        log_warn "⚠️  Database file not found"
        return 0
    fi
}

check_killswitch() {
    log_info "Checking kill switch status..."
    
    health_response=$(curl -s "$API_URL/health" || echo "{}")
    kill_switch=$(echo "$health_response" | jq -r '.kill_switch // false' 2>/dev/null || echo "false")
    
    if [ "$kill_switch" = "true" ]; then
        log_warn "⚠️  Kill switch is ENABLED"
        return 0
    else
        log_info "✅ Kill switch is disabled"
        return 0
    fi
}

generate_report() {
    cat << EOF

==============================================================================
                    autocash-ultimate Health Report
==============================================================================
Generated: $(date)

System Status:
EOF

    check_health && echo "  [✓] API Health" || echo "  [✗] API Health"
    check_disk_space && echo "  [✓] Disk Space" || echo "  [✗] Disk Space"
    check_memory && echo "  [✓] Memory" || echo "  [✗] Memory"
    check_docker_containers && echo "  [✓] Docker Containers" || echo "  [✗] Docker Containers"
    check_database && echo "  [✓] Database" || echo "  [✗] Database"
    check_killswitch && echo "  [✓] Kill Switch Check" || echo "  [✗] Kill Switch Check"

    echo ""
    echo "=============================================================================="
}

main() {
    if [ "$1" = "--report" ]; then
        generate_report
    else
        check_health
        check_disk_space
        check_memory
        check_docker_containers
        check_database
        check_killswitch
        
        echo ""
        log_info "Monitoring complete"
    fi
}

main "$@"
