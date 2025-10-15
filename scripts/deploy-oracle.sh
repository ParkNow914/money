#!/bin/bash
#
# Deployment script for Oracle Cloud VM
# Automates the setup and deployment process
#

set -e

echo "🚀 autocash-ultimate Deployment Script"
echo "======================================="
echo ""

# Configuration
REPO_URL="${REPO_URL:-https://github.com/ParkNow914/money.git}"
APP_DIR="${APP_DIR:-/home/ubuntu/autocash-ultimate}"
BRANCH="${BRANCH:-main}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    log_info "$1 is installed"
    return 0
}

# Main deployment steps
main() {
    log_info "Starting deployment..."
    
    # Check prerequisites
    log_info "Checking prerequisites..."
    check_command git || exit 1
    check_command docker || exit 1
    check_command docker-compose || log_warn "docker-compose not found, will use 'docker compose'"
    
    # Clone or update repository
    if [ -d "$APP_DIR" ]; then
        log_info "Updating repository..."
        cd "$APP_DIR"
        git pull origin "$BRANCH"
    else
        log_info "Cloning repository..."
        git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
        cd "$APP_DIR"
    fi
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        log_warn ".env file not found"
        log_info "Creating .env from template..."
        cp .env.example .env
        log_warn "⚠️  IMPORTANT: Edit .env file with your production values!"
        log_warn "⚠️  Generate secrets with: openssl rand -hex 32"
        echo ""
        read -p "Press enter to continue after editing .env..."
    fi
    
    # Build and start containers
    log_info "Building Docker containers..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f docker/docker-compose.yml build
    else
        docker compose -f docker/docker-compose.yml build
    fi
    
    log_info "Starting services..."
    if command -v docker-compose &> /dev/null; then
        docker-compose -f docker/docker-compose.yml up -d
    else
        docker compose -f docker/docker-compose.yml up -d
    fi
    
    # Wait for services to start
    log_info "Waiting for services to start..."
    sleep 10
    
    # Health check
    log_info "Performing health check..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "✅ Service is healthy!"
    else
        log_error "❌ Health check failed"
        log_info "Check logs with: docker-compose -f docker/docker-compose.yml logs"
        exit 1
    fi
    
    # Setup backups
    log_info "Setting up backup cron job..."
    BACKUP_SCRIPT="$APP_DIR/scripts/backup.sh"
    if [ -f "$BACKUP_SCRIPT" ]; then
        (crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT"; echo "0 2 * * * $BACKUP_SCRIPT") | crontab -
        log_info "✅ Backup cron job installed (daily at 2 AM)"
    else
        log_warn "Backup script not found, skipping cron setup"
    fi
    
    # Display info
    echo ""
    echo "======================================="
    log_info "✅ Deployment complete!"
    echo "======================================="
    echo ""
    echo "Service URL: http://$(curl -s ifconfig.me):8000"
    echo "Health check: http://localhost:8000/health"
    echo "API docs: http://localhost:8000/docs"
    echo ""
    echo "Next steps:"
    echo "1. Configure Cloudflare DNS to point to this VM"
    echo "2. Setup SSL with Let's Encrypt (see docs/deploy_oracle.md)"
    echo "3. Seed keywords: ./scripts/seed-keywords.sh"
    echo "4. Monitor logs: docker-compose -f docker/docker-compose.yml logs -f"
    echo ""
}

# Run main function
main
