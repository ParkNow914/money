#!/bin/bash
#
# Seed keywords from CSV file into database
# Usage: ./seed-keywords.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CSV_FILE="$PROJECT_ROOT/data/keywords_seed.csv"

echo "🌱 Seeding keywords from $CSV_FILE"

# Check if CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ Error: CSV file not found at $CSV_FILE"
    exit 1
fi

# Get admin token from environment or use default
ADMIN_TOKEN="${ADMIN_TOKEN:-dev-admin-token-change-in-production}"
API_URL="${API_URL:-http://localhost:8000}"

echo "📡 Using API URL: $API_URL"
echo "🔑 Using admin token: ${ADMIN_TOKEN:0:10}..."

# Skip header and read CSV
tail -n +2 "$CSV_FILE" | while IFS=',' read -r keyword priority search_volume competition; do
    echo "  Adding keyword: $keyword (priority: $priority)"
    
    response=$(curl -s -X POST "$API_URL/api/keywords/seed" \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"keyword\": \"$keyword\", \"priority\": $priority}" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -eq 200 ]; then
        echo "    ✅ Success"
    else
        echo "    ⚠️  Failed (HTTP $http_code): $body"
    fi
    
    # Small delay to avoid rate limiting
    sleep 0.1
done

echo "✅ Keyword seeding complete!"
