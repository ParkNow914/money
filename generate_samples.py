"""
Script to generate sample posts locally (without Docker).
Run this to create examples/sample_posts.json for demonstration.
"""
import asyncio
import json
from pathlib import Path

from app.config import settings
from app.db import AsyncSessionLocal, init_db
from app.models import Keyword
from app.services.generator import generate_batch


async def generate_samples():
    """Generate sample posts for demonstration."""
    print("🚀 AutoCash Ultimate - Sample Post Generator")
    print("=" * 60)
    print()

    # Ensure directories exist
    settings.ensure_directories()
    Path("examples").mkdir(exist_ok=True)

    # Initialize database
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized")
    print()

    # Check for keywords
    async with AsyncSessionLocal() as db:
        # Add sample keywords if none exist
        from sqlalchemy import select

        result = await db.execute(select(Keyword))
        existing = result.scalars().all()

        if not existing:
            print("🌱 No keywords found. Adding sample keywords...")
            sample_keywords = [
                Keyword(
                    keyword="passive income ideas",
                    priority=9,
                    category="finance",
                    search_volume=12000,
                    competition=0.65,
                    cpc_estimate=2.50,
                ),
                Keyword(
                    keyword="affiliate marketing for beginners",
                    priority=8,
                    category="marketing",
                    search_volume=8500,
                    competition=0.72,
                    cpc_estimate=1.85,
                ),
                Keyword(
                    keyword="how to start a blog",
                    priority=9,
                    category="blogging",
                    search_volume=15000,
                    competition=0.68,
                    cpc_estimate=1.95,
                ),
                Keyword(
                    keyword="SEO best practices 2025",
                    priority=9,
                    category="seo",
                    search_volume=11000,
                    competition=0.75,
                    cpc_estimate=3.20,
                ),
                Keyword(
                    keyword="digital marketing strategies",
                    priority=8,
                    category="marketing",
                    search_volume=9800,
                    competition=0.70,
                    cpc_estimate=2.35,
                ),
            ]

            for kw in sample_keywords:
                db.add(kw)
            await db.commit()
            print(f"✅ Added {len(sample_keywords)} sample keywords")
            print()

        # Generate articles
        print("📝 Generating 5 sample articles...")
        print("   (This may take a few seconds)")
        print()

        articles = await generate_batch(db, count=5, review_required=False)

        print(f"✅ Generated {len(articles)} articles!")
        print()

        # Export to JSON
        output_path = Path("examples/sample_posts.json")

        articles_data = []
        for article in articles:
            articles_data.append(
                {
                    "id": article.id,
                    "title": article.title,
                    "slug": article.slug,
                    "meta_description": article.meta_description,
                    "body": article.body,
                    "word_count": article.word_count,
                    "tags": article.tags,
                    "internal_links": article.internal_links,
                    "schema_markup": article.schema_markup,
                    "cta_variants": article.cta_variants,
                    "video_script": article.video_script,
                    "thread_content": article.thread_content,
                    "status": article.status.value,
                    "created_at": article.created_at.isoformat(),
                }
            )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(articles_data, f, indent=2, ensure_ascii=False)

        print(f"📦 Exported to {output_path}")
        print()
        print("=" * 60)
        print("✅ Sample generation complete!")
        print()
        print("Review the generated articles:")
        print(f"   {output_path.absolute()}")
        print()
        print("Article details:")
        for article in articles:
            print(f"   • {article.title}")
            print(f"     Words: {article.word_count}, Slug: {article.slug}")
            print()


if __name__ == "__main__":
    asyncio.run(generate_samples())
