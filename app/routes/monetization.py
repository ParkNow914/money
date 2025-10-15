"""
Monetization routes for affiliate link management and revenue analytics.

Provides endpoints for managing affiliate links, tracking revenue, and calculating EPC.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.config import settings
from app.db import get_db
from app.models import AffiliateLink, Article
from app.services.monetization import monetization
from app.routes.generate import verify_admin_token

router = APIRouter()


class AffiliateLinkCreate(BaseModel):
    """Request to create an affiliate link."""
    link_id: str
    name: str
    destination_url: str
    product_name: Optional[str] = None
    product_category: Optional[str] = None
    affiliate_program: str
    commission_rate: Optional[float] = None
    commission_type: Optional[str] = None
    article_slug: Optional[str] = None


class AffiliateLinkUpdate(BaseModel):
    """Request to update an affiliate link."""
    name: Optional[str] = None
    destination_url: Optional[str] = None
    commission_rate: Optional[float] = None
    is_active: Optional[bool] = None


class ConversionReport(BaseModel):
    """Report a conversion."""
    link_id: str
    revenue: float
    article_slug: Optional[str] = None


@router.post("/affiliate-links")
async def create_affiliate_link(
    link: AffiliateLinkCreate,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Create a new affiliate link.
    
    Admin only endpoint.
    """
    # Check if link_id already exists
    existing = db.query(AffiliateLink).filter(
        AffiliateLink.link_id == link.link_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail=f"Link ID already exists: {link.link_id}")
    
    # Get article if slug provided
    article_id = None
    if link.article_slug:
        article = db.query(Article).filter(
            Article.slug == link.article_slug
        ).first()
        if article:
            article_id = article.id
    
    # Create link
    affiliate_link = AffiliateLink(
        link_id=link.link_id,
        name=link.name,
        destination_url=link.destination_url,
        product_name=link.product_name,
        product_category=link.product_category,
        affiliate_program=link.affiliate_program,
        commission_rate=link.commission_rate,
        commission_type=link.commission_type,
        article_id=article_id,
        created_at=datetime.utcnow()
    )
    
    db.add(affiliate_link)
    db.commit()
    db.refresh(affiliate_link)
    
    return {
        "success": True,
        "message": "Affiliate link created",
        "link": {
            "link_id": affiliate_link.link_id,
            "name": affiliate_link.name,
            "affiliate_program": affiliate_link.affiliate_program,
            "destination_url": affiliate_link.destination_url
        }
    }


@router.get("/affiliate-links/{link_id}")
async def get_affiliate_link(
    link_id: str,
    db: Session = Depends(get_db)
):
    """
    Get affiliate link details and statistics.
    
    Public endpoint.
    """
    stats = monetization.get_affiliate_link_stats(db, link_id)
    
    if not stats:
        raise HTTPException(status_code=404, detail=f"Affiliate link not found: {link_id}")
    
    return stats


@router.put("/affiliate-links/{link_id}")
async def update_affiliate_link(
    link_id: str,
    update: AffiliateLinkUpdate,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Update an affiliate link.
    
    Admin only endpoint.
    """
    link = db.query(AffiliateLink).filter(
        AffiliateLink.link_id == link_id
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail=f"Affiliate link not found: {link_id}")
    
    # Update fields
    if update.name is not None:
        link.name = update.name
    if update.destination_url is not None:
        link.destination_url = update.destination_url
    if update.commission_rate is not None:
        link.commission_rate = update.commission_rate
    if update.is_active is not None:
        link.is_active = update.is_active
    
    link.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(link)
    
    return {
        "success": True,
        "message": "Affiliate link updated",
        "link_id": link.link_id
    }


@router.get("/affiliate-links")
async def list_affiliate_links(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all affiliate links.
    
    Public endpoint.
    """
    query = db.query(AffiliateLink)
    
    if active_only:
        query = query.filter(AffiliateLink.is_active == True)
    
    links = query.all()
    
    return {
        "links": [
            {
                "link_id": link.link_id,
                "name": link.name,
                "affiliate_program": link.affiliate_program,
                "clicks": link.clicks,
                "conversions": link.conversions,
                "revenue": round(link.revenue, 2),
                "epc": monetization.calculate_epc(link.revenue, link.clicks),
                "is_active": link.is_active
            }
            for link in links
        ],
        "total": len(links)
    }


@router.post("/conversions")
async def report_conversion(
    conversion: ConversionReport,
    _: str = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    """
    Report a conversion for an affiliate link.
    
    Admin only endpoint. In production, this would be called
    via webhook from affiliate network.
    """
    # Get link
    link = db.query(AffiliateLink).filter(
        AffiliateLink.link_id == conversion.link_id
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail=f"Affiliate link not found: {conversion.link_id}")
    
    # Update link stats
    link.conversions += 1
    link.revenue += conversion.revenue
    link.updated_at = datetime.utcnow()
    
    # Create tracking event
    from app.models import TrackingEvent
    
    article_id = None
    if conversion.article_slug:
        article = db.query(Article).filter(
            Article.slug == conversion.article_slug
        ).first()
        if article:
            article_id = article.id
    elif link.article_id:
        article_id = link.article_id
    
    event = TrackingEvent(
        event_type="conversion",
        article_id=article_id,
        session_hash="conversion_" + link.link_id,  # Placeholder
        revenue=conversion.revenue,
        created_at=datetime.utcnow()
    )
    
    db.add(event)
    db.commit()
    
    return {
        "success": True,
        "message": "Conversion recorded",
        "link_id": link.link_id,
        "revenue": conversion.revenue,
        "total_conversions": link.conversions,
        "total_revenue": round(link.revenue, 2)
    }


@router.get("/revenue/period")
async def get_revenue_period(
    days: int = 30,
    article_slug: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get revenue statistics for a time period.
    
    Public endpoint.
    """
    article_id = None
    if article_slug:
        article = db.query(Article).filter(
            Article.slug == article_slug
        ).first()
        if article:
            article_id = article.id
    
    stats = monetization.get_revenue_by_period(db, days, article_id)
    
    return stats


@router.get("/revenue/top-links")
async def get_top_links(
    limit: int = 10,
    order_by: str = "revenue",
    db: Session = Depends(get_db)
):
    """
    Get top performing affiliate links.
    
    Public endpoint.
    
    order_by: revenue, epc, clicks, conversions
    """
    if order_by not in ['revenue', 'epc', 'clicks', 'conversions']:
        raise HTTPException(status_code=400, detail="Invalid order_by parameter")
    
    links = monetization.get_top_performing_links(db, limit, order_by)
    
    return {
        "top_links": links,
        "order_by": order_by,
        "limit": limit
    }


@router.get("/revenue/by-source")
async def get_revenue_by_source(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get revenue breakdown by UTM source.
    
    Public endpoint.
    """
    sources = monetization.get_revenue_by_source(db, days)
    
    return {
        "period_days": days,
        "sources": sources,
        "total_sources": len(sources)
    }


@router.get("/epc")
async def calculate_epc(
    revenue: float,
    clicks: int
):
    """
    Calculate EPC (Earnings Per Click).
    
    Public utility endpoint.
    """
    epc = monetization.calculate_epc(revenue, clicks)
    
    return {
        "revenue": revenue,
        "clicks": clicks,
        "epc": epc,
        "formula": "EPC = Revenue / Clicks"
    }
