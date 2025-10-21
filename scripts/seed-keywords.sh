#!/bin/bash
#
# Seed keywords from CSV into database
# Usage: bash scripts/seed-keywords.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CSV_FILE="$PROJECT_ROOT/data/keywords_seed.csv"

echo "🌱 Seeding keywords from $CSV_FILE"

# Check if CSV exists
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ Error: CSV file not found at $CSV_FILE"
    exit 1
fi

# Python script to load CSV
python3 << EOF
import asyncio
import csv
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, "$PROJECT_ROOT")

from app.db import AsyncSessionLocal
from app.models import Keyword
from sqlalchemy import select


async def seed_keywords():
    """Load keywords from CSV into database."""
    csv_path = Path("$CSV_FILE")
    
    async with AsyncSessionLocal() as db:
        # Read CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            keywords_data = list(reader)
        
        print(f"📋 Found {len(keywords_data)} keywords in CSV")
        
        added = 0
        skipped = 0
        
        for row in keywords_data:
            keyword_text = row['keyword'].strip()
            
            # Check if keyword already exists
            result = await db.execute(
                select(Keyword).where(Keyword.keyword == keyword_text)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"⏭️  Skipping existing keyword: {keyword_text}")
                skipped += 1
                continue
            
            # Create new keyword
            kw = Keyword(
                keyword=keyword_text,
                priority=int(row['priority']),
                category=row['category'] if row['category'] else None,
                search_volume=int(row['search_volume']) if row['search_volume'] else None,
                competition=float(row['competition']) if row['competition'] else None,
                cpc_estimate=float(row['cpc_estimate']) if row['cpc_estimate'] else None,
            )
            
            db.add(kw)
            added += 1
            print(f"✅ Added: {keyword_text} (priority: {kw.priority})")
        
        await db.commit()
        
        print(f"\n📊 Summary:")
        print(f"   Added: {added}")
        print(f"   Skipped: {skipped}")
        print(f"   Total: {len(keywords_data)}")


if __name__ == "__main__":
    asyncio.run(seed_keywords())
EOF

echo "✅ Seeding complete!"
