#!/bin/bash
#
# Automated backup script for autocash-ultimate
# Backs up database and configuration files
#

set -e

BACKUP_DIR="${BACKUP_DIR:-/home/ubuntu/backups}"
APP_DIR="${APP_DIR:-/home/ubuntu/autocash-ultimate}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="autocash_backup_${DATE}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log_info "Starting backup: $BACKUP_NAME"

# Backup database
if [ -f "$APP_DIR/autocash.db" ]; then
    log_info "Backing up database..."
    cp "$APP_DIR/autocash.db" "$BACKUP_DIR/${BACKUP_NAME}.db"
    
    # Compress
    gzip "$BACKUP_DIR/${BACKUP_NAME}.db"
    log_info "Database backup created: ${BACKUP_NAME}.db.gz"
else
    log_warn "Database file not found, skipping"
fi

# Backup environment file (without secrets)
if [ -f "$APP_DIR/.env" ]; then
    log_info "Backing up configuration (secrets redacted)..."
    grep -v -E "(SECRET|TOKEN|PASSWORD|KEY)" "$APP_DIR/.env" > "$BACKUP_DIR/${BACKUP_NAME}.env.sample"
    log_info "Configuration backup created: ${BACKUP_NAME}.env.sample"
fi

# Backup generated content samples
if [ -d "$APP_DIR/examples" ]; then
    log_info "Backing up sample content..."
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_examples.tar.gz" -C "$APP_DIR" examples/
    log_info "Sample content backup created: ${BACKUP_NAME}_examples.tar.gz"
fi

# Create backup manifest
cat > "$BACKUP_DIR/${BACKUP_NAME}_manifest.txt" << EOF
Backup created: $(date)
Database: ${BACKUP_NAME}.db.gz
Config: ${BACKUP_NAME}.env.sample
Content: ${BACKUP_NAME}_examples.tar.gz
EOF

log_info "Backup manifest created"

# Clean up old backups
log_info "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "autocash_backup_*" -mtime +$RETENTION_DAYS -delete
DELETED=$(find "$BACKUP_DIR" -name "autocash_backup_*" -mtime +$RETENTION_DAYS 2>/dev/null | wc -l)
log_info "Deleted $DELETED old backup files"

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log_info "Total backup size: $TOTAL_SIZE"

# Optional: Upload to Object Storage
if [ ! -z "$OCI_BUCKET" ]; then
    log_info "Uploading to Oracle Object Storage..."
    # Uncomment and configure OCI CLI
    # oci os object put --bucket-name "$OCI_BUCKET" \
    #   --file "$BACKUP_DIR/${BACKUP_NAME}.db.gz" \
    #   --name "backups/${BACKUP_NAME}.db.gz"
    log_warn "OCI upload not configured - set OCI_BUCKET to enable"
fi

log_info "Backup complete: $BACKUP_NAME"
echo ""
echo "Backup files:"
ls -lh "$BACKUP_DIR"/${BACKUP_NAME}*
