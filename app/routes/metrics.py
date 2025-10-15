"""
Metrics and monitoring API routes.

Provides Prometheus-compatible metrics and business KPIs.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models import Article, TrackingEvent, ContentStatus

router = APIRouter()


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Get Prometheus-compatible metrics.
    
    Public endpoint for monitoring systems.
    """
    # Article counts by status
    article_stats = db.query(
        Article.status,
        func.count(Article.id).label('count')
    ).group_by(Article.status).all()
    
    # Total articles
    total_articles = db.query(func.count(Article.id)).scalar() or 0
    
    # Tracking events count
    total_events = db.query(func.count(TrackingEvent.id)).scalar() or 0
    
    # Format as Prometheus metrics
    metrics = []
    
    # Article metrics
    metrics.append(f"# HELP articles_total Total number of articles")
    metrics.append(f"# TYPE articles_total gauge")
    metrics.append(f"articles_total {total_articles}")
    
    for status, count in article_stats:
        metrics.append(f"# HELP articles_by_status Number of articles by status")
        metrics.append(f"# TYPE articles_by_status gauge")
        metrics.append(f'articles_by_status{{status="{status.value}"}} {count}')
    
    # Event metrics
    metrics.append(f"# HELP tracking_events_total Total number of tracking events")
    metrics.append(f"# TYPE tracking_events_total counter")
    metrics.append(f"tracking_events_total {total_events}")
    
    return "\n".join(metrics)


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get business statistics and KPIs.
    
    Returns JSON with aggregated metrics.
    """
    # Article stats
    total_articles = db.query(func.count(Article.id)).scalar() or 0
    draft_articles = db.query(func.count(Article.id)).filter(
        Article.status == ContentStatus.DRAFT
    ).scalar() or 0
    review_pending = db.query(func.count(Article.id)).filter(
        Article.status == ContentStatus.REVIEW_PENDING
    ).scalar() or 0
    published_articles = db.query(func.count(Article.id)).filter(
        Article.status == ContentStatus.PUBLISHED
    ).scalar() or 0
    
    # Total word count
    total_words = db.query(func.sum(Article.word_count)).scalar() or 0
    avg_words = db.query(func.avg(Article.word_count)).scalar() or 0
    
    # Tracking stats
    total_views = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.event_type == "view"
    ).scalar() or 0
    total_clicks = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.event_type == "click"
    ).scalar() or 0
    total_conversions = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.event_type == "conversion"
    ).scalar() or 0
    
    # Calculate CTR and conversion rate
    ctr = (total_clicks / total_views * 100) if total_views > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    # Revenue (if tracked)
    total_revenue = db.query(func.sum(TrackingEvent.revenue)).filter(
        TrackingEvent.revenue.isnot(None)
    ).scalar() or 0.0
    
    return {
        "articles": {
            "total": total_articles,
            "draft": draft_articles,
            "review_pending": review_pending,
            "published": published_articles,
            "total_words": int(total_words),
            "avg_words": int(avg_words),
        },
        "engagement": {
            "total_views": total_views,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "ctr_percent": round(ctr, 2),
            "conversion_rate_percent": round(conversion_rate, 2),
        },
        "revenue": {
            "total": round(total_revenue, 2),
            "epc": round(total_revenue / total_clicks, 2) if total_clicks > 0 else 0,
        }
    }
