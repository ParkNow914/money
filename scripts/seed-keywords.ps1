# PowerShell version of seed-keywords script
# Usage: powershell -ExecutionPolicy Bypass -File scripts\seed-keywords.ps1

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$CSV_FILE = Join-Path $PROJECT_ROOT "data\keywords_seed.csv"

Write-Host "🌱 Seeding keywords from $CSV_FILE" -ForegroundColor Green

# Check if CSV exists
if (-not (Test-Path $CSV_FILE)) {
    Write-Host "❌ Error: CSV file not found at $CSV_FILE" -ForegroundColor Red
    exit 1
}

# Run Python seeding script
$pythonScript = @"
import asyncio
import csv
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, r'$PROJECT_ROOT')

from app.db import AsyncSessionLocal
from app.models import Keyword
from sqlalchemy import select


async def seed_keywords():
    csv_path = Path(r'$CSV_FILE')
    
    async with AsyncSessionLocal() as db:
        # Read CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            keywords_data = list(reader)
        
        print(f'📋 Found {len(keywords_data)} keywords in CSV')
        
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
                print(f'⏭️  Skipping existing keyword: {keyword_text}')
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
            print(f'✅ Added: {keyword_text} (priority: {kw.priority})')
        
        await db.commit()
        
        print(f'\n📊 Summary:')
        print(f'   Added: {added}')
        print(f'   Skipped: {skipped}')
        print(f'   Total: {len(keywords_data)}')


if __name__ == '__main__':
    asyncio.run(seed_keywords())
"@

python -c $pythonScript

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Seeding complete!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Seeding failed!" -ForegroundColor Red
    exit 1
}
