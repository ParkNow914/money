"""
Tracking routes for privacy-preserving analytics.

Handles click tracking, conversions, and UTM parameters with LGPD compliance.
"""

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib
from datetime import datetime
from typing import Optional

from app.config import settings
from app.db import get_db
from app.models import TrackingEvent, Article

router = APIRouter()


class TrackEvent(BaseModel):
    """Track an event."""
    event_type: str
    article_slug: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    revenue: Optional[float] = None


@router.get("/out")
async def track_click(
    aid: str,  # Article ID or affiliate link ID
    post: Optional[str] = None,
    utm_source: Optional[str] = None,
    utm_medium: Optional[str] = None,
    utm_campaign: Optional[str] = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    Track affiliate click and redirect.
    
    Privacy-preserving: stores only hashed identifiers.
    
    Example: /api/tracking/out?aid=amazon123&post=article-slug&utm_source=google
    """
    # Get article if post slug provided
    article = None
    if post:
        article = db.query(Article).filter(Article.slug == post).first()
    
    # Generate session hash from request
    session_data = f"{request.client.host}{request.headers.get('user-agent', '')}{datetime.utcnow().date()}"
    session_hash = hashlib.sha256(session_data.encode()).hexdigest()
    
    # Hash IP with salt for privacy
    ip_hash = hashlib.sha256(
        f"{request.client.host}{settings.IP_SALT}".encode()
    ).hexdigest()
    
    # Hash user agent
    ua_hash = hashlib.sha256(
        request.headers.get('user-agent', '').encode()
    ).hexdigest()
    
    # Create tracking event
    event = TrackingEvent(
        event_type="click",
        article_id=article.id if article else None,
        session_hash=session_hash,
        ip_hash=ip_hash,
        ua_hash=ua_hash,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        created_at=datetime.utcnow()
    )
    
    db.add(event)
    db.commit()
    
    # TODO: Get actual redirect URL from affiliate link database
    redirect_url = f"https://example.com/affiliate/{aid}"
    
    return RedirectResponse(url=redirect_url, status_code=302)


@router.post("/event")
async def track_event(
    event: TrackEvent,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Track custom event (view, conversion, etc).
    
    Used for client-side tracking via JavaScript.
    """
    # Get article if slug provided
    article = None
    if event.article_slug:
        article = db.query(Article).filter(Article.slug == event.article_slug).first()
    
    # Generate session hash
    session_data = f"{request.client.host}{request.headers.get('user-agent', '')}{datetime.utcnow().date()}"
    session_hash = hashlib.sha256(session_data.encode()).hexdigest()
    
    # Hash IP with salt
    ip_hash = hashlib.sha256(
        f"{request.client.host}{settings.IP_SALT}".encode()
    ).hexdigest()
    
    # Hash user agent
    ua_hash = hashlib.sha256(
        request.headers.get('user-agent', '').encode()
    ).hexdigest()
    
    # Create tracking event
    tracking = TrackingEvent(
        event_type=event.event_type,
        article_id=article.id if article else None,
        session_hash=session_hash,
        ip_hash=ip_hash,
        ua_hash=ua_hash,
        utm_source=event.utm_source,
        utm_medium=event.utm_medium,
        utm_campaign=event.utm_campaign,
        revenue=event.revenue,
        created_at=datetime.utcnow()
    )
    
    db.add(tracking)
    db.commit()
    
    return {
        "success": True,
        "event_type": event.event_type,
        "tracked_at": datetime.utcnow().isoformat()
    }


@router.get("/stats/{slug}")
async def get_article_stats(slug: str, db: Session = Depends(get_db)):
    """
    Get tracking statistics for an article.
    
    Public endpoint - shows aggregated anonymous data only.
    """
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Article not found")
    
    from sqlalchemy import func
    
    # Count events by type
    views = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.article_id == article.id,
        TrackingEvent.event_type == "view"
    ).scalar() or 0
    
    clicks = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.article_id == article.id,
        TrackingEvent.event_type == "click"
    ).scalar() or 0
    
    conversions = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.article_id == article.id,
        TrackingEvent.event_type == "conversion"
    ).scalar() or 0
    
    revenue = db.query(func.sum(TrackingEvent.revenue)).filter(
        TrackingEvent.article_id == article.id,
        TrackingEvent.revenue.isnot(None)
    ).scalar() or 0.0
    
    return {
        "article": {
            "slug": article.slug,
            "title": article.title
        },
        "stats": {
            "views": views,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": round((clicks / views * 100) if views > 0 else 0, 2),
            "conversion_rate": round((conversions / clicks * 100) if clicks > 0 else 0, 2),
            "revenue": round(revenue, 2),
            "epc": round(revenue / clicks, 2) if clicks > 0 else 0
        }
    }
