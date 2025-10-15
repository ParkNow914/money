"""
Publisher routes for static site generation.

Provides endpoints to publish articles as static HTML files.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config import settings
from app.db import get_db
from app.models import Article, ContentStatus
from app.services.publisher import publisher
from app.routes.generate import verify_admin_token

router = APIRouter()


class PublishRequest(BaseModel):
    """Request to publish an article."""
    slug: str
    site_name: Optional[str] = "AutoCash Ultimate"
    base_url: Optional[str] = "https://example.com"


class PublishBatchRequest(BaseModel):
    """Request to publish multiple articles."""
    status: Optional[ContentStatus] = ContentStatus.APPROVED
    site_name: Optional[str] = "AutoCash Ultimate"
    base_url: Optional[str] = "https://example.com"


@router.post("/publish")
async def publish_article(
    request: PublishRequest,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Publish a single article as static HTML.
    
    Admin only endpoint. Requires bearer token authentication.
    """
    # Get article from database
    article = db.query(Article).filter(
        Article.slug == request.slug
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail=f"Article not found: {request.slug}")
    
    # Publish to HTML
    try:
        output_file = publisher.publish_article(
            article,
            site_name=request.site_name,
            base_url=request.base_url
        )
        
        return {
            "success": True,
            "message": f"Article published successfully",
            "article": {
                "slug": article.slug,
                "title": article.title,
                "output_file": str(output_file)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Publishing failed: {str(e)}")


@router.post("/publish-batch")
async def publish_batch(
    request: PublishBatchRequest,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Publish multiple articles as static HTML.
    
    Admin only endpoint. Publishes all articles with specified status.
    """
    # Get articles from database
    query = db.query(Article)
    
    if request.status:
        query = query.filter(Article.status == request.status)
    
    articles = query.all()
    
    if not articles:
        return {
            "success": True,
            "message": "No articles to publish",
            "count": 0
        }
    
    # Publish articles
    published = []
    errors = []
    
    for article in articles:
        try:
            output_file = publisher.publish_article(
                article,
                site_name=request.site_name,
                base_url=request.base_url
            )
            published.append({
                "slug": article.slug,
                "title": article.title,
                "file": str(output_file)
            })
        except Exception as e:
            errors.append({
                "slug": article.slug,
                "error": str(e)
            })
    
    # Publish index page
    try:
        index_file = publisher.publish_index(
            articles,
            site_name=request.site_name,
            base_url=request.base_url
        )
    except Exception as e:
        errors.append({
            "file": "index.html",
            "error": str(e)
        })
    
    return {
        "success": True,
        "message": f"Published {len(published)} articles",
        "published": published,
        "errors": errors,
        "index_file": str(index_file) if 'index_file' in locals() else None
    }


@router.get("/publish/status")
async def publish_status(_: str = Depends(verify_admin_token)):
    """
    Get publishing status (count of published files).
    
    Admin only endpoint.
    """
    count = publisher.get_published_count()
    
    return {
        "published_count": count,
        "output_directory": str(publisher.output_dir)
    }


@router.post("/publish/clean")
async def clean_published(_: str = Depends(verify_admin_token)):
    """
    Clean all published files.
    
    Admin only endpoint. Use with caution.
    """
    try:
        publisher.clean_output_directory()
        return {
            "success": True,
            "message": "Published files cleaned successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning failed: {str(e)}")
