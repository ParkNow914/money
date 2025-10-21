"""
CLI tool for content generation and management.

Usage:
    python -m app.cli generate --count 5
    python -m app.cli list-keywords
    python -m app.cli export-posts --output examples/sample_posts.json
"""
import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from sqlalchemy import select

from app.config import settings
from app.db import AsyncSessionLocal
from app.models import Article, Keyword
from app.services.generator import generate_batch

app = typer.Typer(
    name="autocash-cli",
    help="AutoCash Ultimate CLI for content generation and management",
)


@app.command()
def generate(
    count: int = typer.Option(5, "--count", "-c", help="Number of articles to generate"),
    review_required: bool = typer.Option(
        True, "--review/--no-review", help="Whether articles require review"
    ),
):
    """Generate articles from keywords."""
    typer.echo(f"🚀 Generating {count} articles...")
    typer.echo(f"📋 Review required: {review_required}")

    async def _generate():
        async with AsyncSessionLocal() as db:
            try:
                articles = await generate_batch(db, count, review_required)
                typer.echo(f"✅ Generated {len(articles)} articles successfully!")
                for article in articles:
                    typer.echo(f"  - {article.title} (ID: {article.id}, Status: {article.status})")
            except Exception as e:
                typer.echo(f"❌ Error: {e}", err=True)
                raise typer.Exit(code=1)

    asyncio.run(_generate())


@app.command()
def list_keywords():
    """List all active keywords."""
    async def _list():
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Keyword).where(Keyword.is_active == True).order_by(Keyword.priority.desc())
            )
            keywords = result.scalars().all()

            if not keywords:
                typer.echo("No active keywords found.")
                return

            typer.echo(f"📋 Found {len(keywords)} active keywords:\n")
            for kw in keywords:
                typer.echo(
                    f"  ID: {kw.id:3d} | Priority: {kw.priority} | Keyword: {kw.keyword}"
                )

    asyncio.run(_list())


@app.command()
def export_posts(
    output: Path = typer.Option(
        Path("examples/sample_posts.json"),
        "--output",
        "-o",
        help="Output file path",
    ),
    limit: int = typer.Option(5, "--limit", "-l", help="Max number of posts to export"),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (draft/review/approved/published)"
    ),
):
    """Export articles to JSON file."""
    async def _export():
        async with AsyncSessionLocal() as db:
            query = select(Article).order_by(Article.created_at.desc()).limit(limit)

            if status:
                from app.models import ArticleStatus

                try:
                    status_enum = ArticleStatus(status.lower())
                    query = query.where(Article.status == status_enum)
                except ValueError:
                    typer.echo(f"❌ Invalid status: {status}", err=True)
                    raise typer.Exit(code=1)

            result = await db.execute(query)
            articles = result.scalars().all()

            if not articles:
                typer.echo("No articles found.")
                return

            # Convert to dict
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

            # Ensure output directory exists
            output.parent.mkdir(parents=True, exist_ok=True)

            # Write to file
            with open(output, "w", encoding="utf-8") as f:
                json.dump(articles_data, f, indent=2, ensure_ascii=False)

            typer.echo(f"✅ Exported {len(articles_data)} articles to {output}")

    asyncio.run(_export())


@app.command()
def seed_keyword(
    keyword: str = typer.Argument(..., help="Keyword to add"),
    priority: int = typer.Option(5, "--priority", "-p", help="Priority (1-10)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Category"),
):
    """Add a single keyword to database."""
    async def _seed():
        async with AsyncSessionLocal() as db:
            kw = Keyword(keyword=keyword, priority=priority, category=category)
            db.add(kw)
            await db.commit()
            await db.refresh(kw)
            typer.echo(f"✅ Added keyword '{keyword}' with ID {kw.id}")

    asyncio.run(_seed())


if __name__ == "__main__":
    app()
