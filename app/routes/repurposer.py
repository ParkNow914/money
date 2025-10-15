"""
Repurposer routes for content transformation.

Provides endpoints to repurpose articles into various formats.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.config import settings
from app.db import get_db
from app.models import Article, RepurposedContent
from app.services.repurposer import repurposer
from app.routes.generate import verify_admin_token

router = APIRouter()


class RepurposeRequest(BaseModel):
    """Request to repurpose an article."""
    slug: str
    format: str  # thread, video_script, email, pdf
    # Optional format-specific parameters
    max_tweets: Optional[int] = 10
    duration_minutes: Optional[int] = 5
    email_type: Optional[str] = "newsletter"


@router.post("/repurpose")
async def repurpose_article(
    request: RepurposeRequest,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Repurpose an article into different format.
    
    Admin only endpoint. Supports: thread, video_script, email, pdf.
    """
    # Get article from database
    article = db.query(Article).filter(
        Article.slug == request.slug
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail=f"Article not found: {request.slug}")
    
    # Prepare kwargs based on format
    kwargs = {}
    if request.format == 'thread':
        kwargs['max_tweets'] = request.max_tweets
    elif request.format == 'video_script':
        kwargs['duration_minutes'] = request.duration_minutes
    elif request.format == 'email':
        kwargs['email_type'] = request.email_type
    
    # Repurpose content
    try:
        content_data = repurposer.create_repurposed_content(
            article,
            request.format,
            **kwargs
        )
        
        # Save repurposed content to database
        repurposed = RepurposedContent(
            article_id=article.id,
            content_type=request.format,
            content_data=content_data,
            created_at=datetime.utcnow()
        )
        db.add(repurposed)
        db.commit()
        db.refresh(repurposed)
        
        return {
            "success": True,
            "message": f"Article repurposed to {request.format}",
            "repurposed_id": repurposed.id,
            "content": content_data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Repurposing failed: {str(e)}")


@router.get("/repurpose/{slug}")
async def get_repurposed_content(
    slug: str,
    format: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get repurposed content for an article.
    
    Public endpoint. Returns all repurposed versions or specific format.
    """
    # Get article
    article = db.query(Article).filter(
        Article.slug == slug
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail=f"Article not found: {slug}")
    
    # Query repurposed content
    query = db.query(RepurposedContent).filter(
        RepurposedContent.article_id == article.id
    )
    
    if format:
        query = query.filter(RepurposedContent.content_type == format)
    
    repurposed_items = query.all()
    
    return {
        "article_slug": slug,
        "article_title": article.title,
        "repurposed_count": len(repurposed_items),
        "items": [
            {
                "id": item.id,
                "format": item.content_type,
                "created_at": item.created_at.isoformat(),
                "content": item.content_data
            }
            for item in repurposed_items
        ]
    }


@router.get("/repurpose/formats")
async def get_supported_formats():
    """
    Get list of supported repurposing formats.
    
    Public endpoint.
    """
    return {
        "formats": [
            {
                "type": "thread",
                "name": "Twitter/X Thread",
                "description": "Convert article into a tweet thread",
                "parameters": ["max_tweets"]
            },
            {
                "type": "video_script",
                "name": "Video Script",
                "description": "Create a video script with timestamps",
                "parameters": ["duration_minutes"]
            },
            {
                "type": "email",
                "name": "Email Newsletter",
                "description": "Format as email newsletter",
                "parameters": ["email_type"]
            },
            {
                "type": "pdf",
                "name": "PDF Outline",
                "description": "Create PDF document structure",
                "parameters": []
            }
        ]
    }
