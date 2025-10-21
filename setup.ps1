# AutoCash Ultimate - Setup Script
# This script initializes the project, seeds data, and generates sample posts

param(
    [switch]$SkipDocker,
    [switch]$SkipSeed,
    [switch]$GeneratePosts = $true,
    [int]$PostCount = 5
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 AutoCash Ultimate - Setup Script" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file. Please review and update if needed.`n" -ForegroundColor Green
}

# Check Docker
if (-not $SkipDocker) {
    Write-Host "🐳 Checking Docker..." -ForegroundColor Cyan
    try {
        docker --version | Out-Null
        docker-compose --version | Out-Null
        Write-Host "✅ Docker is installed`n" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
        Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        exit 1
    }

    # Build and start services
    Write-Host "🔨 Building Docker containers (this may take a few minutes)..." -ForegroundColor Cyan
    docker-compose build

    Write-Host "`n🚀 Starting services..." -ForegroundColor Cyan
    docker-compose up -d

    Write-Host "`n⏳ Waiting for services to be ready..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10

    # Check health
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
        Write-Host "✅ API is healthy: $($health.status)`n" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  API not responding yet. This is normal on first run." -ForegroundColor Yellow
        Write-Host "   Services are starting in background. Check with: docker-compose logs -f`n" -ForegroundColor Yellow
    }
}

# Seed keywords
if (-not $SkipSeed) {
    Write-Host "🌱 Seeding keywords from CSV..." -ForegroundColor Cyan
    
    if (Test-Path ".\scripts\seed-keywords.ps1") {
        & ".\scripts\seed-keywords.ps1"
    } else {
        Write-Host "⚠️  Seed script not found. Skipping keyword seeding." -ForegroundColor Yellow
    }
}

# Generate sample posts
if ($GeneratePosts) {
    Write-Host "`n📝 Generating $PostCount sample articles..." -ForegroundColor Cyan
    
    try {
        docker-compose exec -T api python -m app.cli generate --count $PostCount --no-review
        Write-Host "✅ Generated articles successfully`n" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Could not generate articles. API may still be starting." -ForegroundColor Yellow
        Write-Host "   You can run this manually later: docker-compose exec api python -m app.cli generate --count 5`n" -ForegroundColor Yellow
    }

    # Export to JSON
    Write-Host "📦 Exporting articles to JSON..." -ForegroundColor Cyan
    try {
        docker-compose exec -T api python -m app.cli export-posts --limit $PostCount
        Write-Host "✅ Exported to examples/sample_posts.json`n" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Could not export. You can run this later: docker-compose exec api python -m app.cli export-posts`n" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "="*60 + "`n" -ForegroundColor Cyan

Write-Host "📍 Services running at:" -ForegroundColor Cyan
Write-Host "   • API:          http://localhost:8000" -ForegroundColor White
Write-Host "   • API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • Health:       http://localhost:8000/health" -ForegroundColor White
Write-Host "   • Metrics:      http://localhost:8000/metrics" -ForegroundColor White
Write-Host "   • MeiliSearch:  http://localhost:7700" -ForegroundColor White
Write-Host "   • Redis:        localhost:6379`n" -ForegroundColor White

Write-Host "🔧 Useful commands:" -ForegroundColor Cyan
Write-Host "   • View logs:        docker-compose logs -f" -ForegroundColor White
Write-Host "   • Stop services:    docker-compose down" -ForegroundColor White
Write-Host "   • Restart:          docker-compose restart" -ForegroundColor White
Write-Host "   • Run tests:        docker-compose exec api pytest tests/ -v" -ForegroundColor White
Write-Host "   • Generate posts:   docker-compose exec api python -m app.cli generate --count 5" -ForegroundColor White
Write-Host "   • List keywords:    docker-compose exec api python -m app.cli list-keywords" -ForegroundColor White
Write-Host "   • Shell access:     docker-compose exec api bash`n" -ForegroundColor White

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • README.md          - Project overview and quick start" -ForegroundColor White
Write-Host "   • QUICKSTART.md      - Step-by-step testing guide" -ForegroundColor White
Write-Host "   • docs/lgpd_checklist.md     - LGPD compliance" -ForegroundColor White
Write-Host "   • docs/security_checklist.md - Security measures" -ForegroundColor White
Write-Host "   • PR1_DESCRIPTION.md - Complete PR1 details`n" -ForegroundColor White

Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review generated articles in examples/sample_posts.json" -ForegroundColor White
Write-Host "   2. Run tests: docker-compose exec api pytest tests/ -v --cov=app" -ForegroundColor White
Write-Host "   3. Check API docs at http://localhost:8000/docs" -ForegroundColor White
Write-Host "   4. Initialize git and push to GitHub" -ForegroundColor White
Write-Host "   5. Review PR1_DESCRIPTION.md and create Pull Request`n" -ForegroundColor White

Write-Host "💡 Tip: Use -SkipDocker to skip Docker setup, -SkipSeed to skip keyword seeding" -ForegroundColor Yellow
Write-Host "`nHappy coding! 🚀`n" -ForegroundColor Green
