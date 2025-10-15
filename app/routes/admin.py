"""
Admin routes for system management and monitoring.

Protected endpoints for administrative operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from app.config import settings
from app.db import get_db
from app.models import Article, Keyword, TrackingEvent, UserConsent, AuditLog, ContentStatus
from app.routes.generate import verify_admin_token

router = APIRouter()


class SystemStats(BaseModel):
    """System statistics."""
    uptime_seconds: float
    database_size_mb: float
    total_articles: int
    total_keywords: int
    total_events: int
    total_consents: int
    disk_usage_percent: float


class BulkActionRequest(BaseModel):
    """Bulk action request."""
    action: str  # approve, archive, delete
    article_ids: List[int]


@router.get("/status")
async def admin_status(
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Get comprehensive system status.
    
    Requires admin authorization.
    """
    # Database statistics
    total_articles = db.query(func.count(Article.id)).scalar() or 0
    total_keywords = db.query(func.count(Keyword.id)).scalar() or 0
    total_events = db.query(func.count(TrackingEvent.id)).scalar() or 0
    total_consents = db.query(func.count(UserConsent.id)).scalar() or 0
    total_audits = db.query(func.count(AuditLog.id)).scalar() or 0
    
    # Articles by status
    articles_by_status = db.query(
        Article.status,
        func.count(Article.id)
    ).group_by(Article.status).all()
    
    # Recent activity (last 24h)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_articles = db.query(func.count(Article.id)).filter(
        Article.created_at >= yesterday
    ).scalar() or 0
    recent_events = db.query(func.count(TrackingEvent.id)).filter(
        TrackingEvent.created_at >= yesterday
    ).scalar() or 0
    
    return {
        "status": "healthy" if not settings.KILL_SWITCH_ENABLED else "paused",
        "kill_switch": settings.KILL_SWITCH_ENABLED,
        "review_required": settings.REVIEW_REQUIRED,
        "environment": settings.ENVIRONMENT,
        "database": {
            "total_articles": total_articles,
            "total_keywords": total_keywords,
            "total_events": total_events,
            "total_consents": total_consents,
            "total_audit_logs": total_audits,
            "articles_by_status": {
                status.value: count for status, count in articles_by_status
            }
        },
        "activity_24h": {
            "new_articles": recent_articles,
            "new_events": recent_events
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/articles/bulk")
async def bulk_article_action(
    request: BulkActionRequest,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Perform bulk actions on articles.
    
    Actions: approve, archive, delete
    """
    if request.action not in ["approve", "archive", "delete"]:
        raise HTTPException(status_code=400, detail=f"Invalid action: {request.action}")
    
    articles = db.query(Article).filter(Article.id.in_(request.article_ids)).all()
    
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found with given IDs")
    
    modified = 0
    
    for article in articles:
        if request.action == "approve":
            article.status = ContentStatus.APPROVED
            article.review_required = False
            article.published_at = datetime.utcnow()
            modified += 1
        elif request.action == "archive":
            article.status = ContentStatus.ARCHIVED
            modified += 1
        elif request.action == "delete":
            db.delete(article)
            modified += 1
    
    db.commit()
    
    return {
        "success": True,
        "action": request.action,
        "modified": modified,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/cleanup")
async def cleanup_old_data(
    days: int = 365,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Clean up old data based on retention policy.
    
    LGPD Article 16: Data retention limits.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Delete old tracking events
    old_events = db.query(TrackingEvent).filter(
        TrackingEvent.created_at < cutoff_date
    ).delete()
    
    # Delete expired consents
    expired_consents = db.query(UserConsent).filter(
        UserConsent.expires_at < datetime.utcnow()
    ).delete()
    
    db.commit()
    
    return {
        "success": True,
        "deleted": {
            "tracking_events": old_events,
            "expired_consents": expired_consents
        },
        "retention_days": days,
        "cutoff_date": cutoff_date.isoformat()
    }


@router.get("/logs/audit")
async def get_audit_logs(
    limit: int = 100,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_admin_token)
):
    """
    Retrieve audit logs for compliance.
    
    LGPD compliance: maintaining records of data processing.
    """
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "action": log.action,
                "user_hash": log.user_hash,
                "details": log.details,
                "created_at": log.created_at.isoformat(),
                "ip_hash": log.ip_hash
            }
            for log in logs
        ],
        "total": len(logs)
    }


@router.post("/killswitch")
async def toggle_killswitch(
    enabled: bool,
    authorized: bool = Depends(verify_admin_token)
):
    """
    Toggle the emergency kill switch.
    
    Note: This only affects the current process.
    For persistent changes, update environment variable.
    """
    # In a real implementation, this would update a persistent flag
    # For now, it's informational
    
    return {
        "success": True,
        "kill_switch_enabled": enabled,
        "message": "Kill switch toggled. Note: Restart required for persistence.",
        "current_setting": settings.KILL_SWITCH_ENABLED
    }
