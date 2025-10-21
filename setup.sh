#!/bin/bash
# AutoCash Ultimate - Setup Script (Bash version)
# This script initializes the project, seeds data, and generates sample posts

set -e

SKIP_DOCKER=false
SKIP_SEED=false
GENERATE_POSTS=true
POST_COUNT=5

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-docker)
            SKIP_DOCKER=true
            shift
            ;;
        --skip-seed)
            SKIP_SEED=true
            shift
            ;;
        --count)
            POST_COUNT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "🚀 AutoCash Ultimate - Setup Script"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and update if needed."
    echo ""
fi

# Check Docker
if [ "$SKIP_DOCKER" = false ]; then
    echo "🐳 Checking Docker..."
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker."
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found. Please install Docker Compose."
        exit 1
    fi
    echo "✅ Docker is installed"
    echo ""

    # Build and start
    echo "🔨 Building Docker containers..."
    docker-compose build

    echo ""
    echo "🚀 Starting services..."
    docker-compose up -d

    echo ""
    echo "⏳ Waiting for services to be ready..."
    sleep 10

    # Health check
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "✅ API is healthy"
    else
        echo "⚠️  API not responding yet. Services are starting in background."
    fi
    echo ""
fi

# Seed keywords
if [ "$SKIP_SEED" = false ]; then
    echo "🌱 Seeding keywords from CSV..."
    if [ -f "./scripts/seed-keywords.sh" ]; then
        bash ./scripts/seed-keywords.sh
    else
        echo "⚠️  Seed script not found. Skipping."
    fi
fi

# Generate posts
if [ "$GENERATE_POSTS" = true ]; then
    echo ""
    echo "📝 Generating $POST_COUNT sample articles..."
    docker-compose exec -T api python -m app.cli generate --count "$POST_COUNT" --no-review || \
        echo "⚠️  Could not generate articles. Run manually later."

    echo ""
    echo "📦 Exporting articles to JSON..."
    docker-compose exec -T api python -m app.cli export-posts --limit "$POST_COUNT" || \
        echo "⚠️  Could not export. Run manually later."
fi

# Summary
echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""

echo "📍 Services running at:"
echo "   • API:          http://localhost:8000"
echo "   • API Docs:     http://localhost:8000/docs"
echo "   • Health:       http://localhost:8000/health"
echo "   • Metrics:      http://localhost:8000/metrics"
echo "   • MeiliSearch:  http://localhost:7700"
echo "   • Redis:        localhost:6379"
echo ""

echo "🔧 Useful commands:"
echo "   • View logs:        docker-compose logs -f"
echo "   • Stop services:    docker-compose down"
echo "   • Restart:          docker-compose restart"
echo "   • Run tests:        docker-compose exec api pytest tests/ -v"
echo "   • Generate posts:   docker-compose exec api python -m app.cli generate --count 5"
echo "   • List keywords:    docker-compose exec api python -m app.cli list-keywords"
echo ""

echo "🎯 Next steps:"
echo "   1. Review generated articles in examples/sample_posts.json"
echo "   2. Run tests: docker-compose exec api pytest tests/ -v --cov=app"
echo "   3. Check API docs at http://localhost:8000/docs"
echo "   4. Initialize git and push to GitHub"
echo ""

echo "Happy coding! 🚀"
echo ""
