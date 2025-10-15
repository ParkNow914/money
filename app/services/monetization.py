"""
Monetization service for revenue tracking and analysis.

Handles affiliate link management, EPC calculations, and revenue reporting.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import AffiliateLink, TrackingEvent, Article


class MonetizationService:
    """
    Service for managing monetization and revenue analytics.
    
    Features:
    - Affiliate link management
    - EPC (Earnings Per Click) calculations
    - Revenue reporting and analytics
    - Performance tracking
    """
    
    def calculate_epc(
        self,
        revenue: float,
        clicks: int
    ) -> float:
        """
        Calculate EPC (Earnings Per Click).
        
        Args:
            revenue: Total revenue generated
            clicks: Total number of clicks
            
        Returns:
            EPC value (revenue per click)
        """
        if clicks == 0:
            return 0.0
        return round(revenue / clicks, 2)
    
    def calculate_conversion_rate(
        self,
        conversions: int,
        clicks: int
    ) -> float:
        """
        Calculate conversion rate percentage.
        
        Args:
            conversions: Number of conversions
            clicks: Total number of clicks
            
        Returns:
            Conversion rate as percentage
        """
        if clicks == 0:
            return 0.0
        return round((conversions / clicks) * 100, 2)
    
    def calculate_ctr(
        self,
        clicks: int,
        views: int
    ) -> float:
        """
        Calculate CTR (Click-Through Rate).
        
        Args:
            clicks: Number of clicks
            views: Number of views
            
        Returns:
            CTR as percentage
        """
        if views == 0:
            return 0.0
        return round((clicks / views) * 100, 2)
    
    def get_affiliate_link_stats(
        self,
        db: Session,
        link_id: str
    ) -> Optional[Dict]:
        """
        Get statistics for a specific affiliate link.
        
        Args:
            db: Database session
            link_id: Affiliate link ID
            
        Returns:
            Dictionary with link statistics
        """
        link = db.query(AffiliateLink).filter(
            AffiliateLink.link_id == link_id
        ).first()
        
        if not link:
            return None
        
        epc = self.calculate_epc(link.revenue, link.clicks)
        conversion_rate = self.calculate_conversion_rate(link.conversions, link.clicks)
        
        return {
            "link_id": link.link_id,
            "name": link.name,
            "affiliate_program": link.affiliate_program,
            "clicks": link.clicks,
            "conversions": link.conversions,
            "revenue": round(link.revenue, 2),
            "epc": epc,
            "conversion_rate": conversion_rate,
            "commission_rate": link.commission_rate,
            "is_active": link.is_active,
            "last_click_at": link.last_click_at.isoformat() if link.last_click_at else None
        }
    
    def get_revenue_by_period(
        self,
        db: Session,
        days: int = 30,
        article_id: Optional[int] = None
    ) -> Dict:
        """
        Get revenue statistics for a time period.
        
        Args:
            db: Database session
            days: Number of days to look back
            article_id: Optional article ID filter
            
        Returns:
            Revenue statistics for the period
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query
        query = db.query(
            func.count(TrackingEvent.id).label('total_events'),
            func.sum(TrackingEvent.revenue).label('total_revenue')
        ).filter(
            TrackingEvent.created_at >= start_date
        )
        
        if article_id:
            query = query.filter(TrackingEvent.article_id == article_id)
        
        result = query.first()
        
        total_revenue = result.total_revenue or 0.0
        
        # Get click count
        click_query = db.query(func.count(TrackingEvent.id)).filter(
            TrackingEvent.created_at >= start_date,
            TrackingEvent.event_type == 'click'
        )
        
        if article_id:
            click_query = click_query.filter(TrackingEvent.article_id == article_id)
        
        total_clicks = click_query.scalar() or 0
        
        # Get conversion count
        conversion_query = db.query(func.count(TrackingEvent.id)).filter(
            TrackingEvent.created_at >= start_date,
            TrackingEvent.event_type == 'conversion'
        )
        
        if article_id:
            conversion_query = conversion_query.filter(TrackingEvent.article_id == article_id)
        
        total_conversions = conversion_query.scalar() or 0
        
        epc = self.calculate_epc(total_revenue, total_clicks)
        conversion_rate = self.calculate_conversion_rate(total_conversions, total_clicks)
        
        return {
            "period_days": days,
            "start_date": start_date.isoformat(),
            "end_date": datetime.utcnow().isoformat(),
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_revenue": round(total_revenue, 2),
            "epc": epc,
            "conversion_rate": conversion_rate,
            "average_daily_revenue": round(total_revenue / days, 2) if days > 0 else 0
        }
    
    def get_top_performing_links(
        self,
        db: Session,
        limit: int = 10,
        order_by: str = 'revenue'
    ) -> List[Dict]:
        """
        Get top performing affiliate links.
        
        Args:
            db: Database session
            limit: Number of links to return
            order_by: Sort field (revenue, epc, clicks, conversions)
            
        Returns:
            List of top performing links
        """
        # Build query
        query = db.query(AffiliateLink).filter(
            AffiliateLink.is_active == True
        )
        
        # Sort by requested field
        if order_by == 'revenue':
            query = query.order_by(AffiliateLink.revenue.desc())
        elif order_by == 'clicks':
            query = query.order_by(AffiliateLink.clicks.desc())
        elif order_by == 'conversions':
            query = query.order_by(AffiliateLink.conversions.desc())
        
        links = query.limit(limit).all()
        
        results = []
        for link in links:
            epc = self.calculate_epc(link.revenue, link.clicks)
            conversion_rate = self.calculate_conversion_rate(link.conversions, link.clicks)
            
            results.append({
                "link_id": link.link_id,
                "name": link.name,
                "affiliate_program": link.affiliate_program,
                "clicks": link.clicks,
                "conversions": link.conversions,
                "revenue": round(link.revenue, 2),
                "epc": epc,
                "conversion_rate": conversion_rate
            })
        
        # Sort by EPC if requested (can't do in SQL easily)
        if order_by == 'epc':
            results.sort(key=lambda x: x['epc'], reverse=True)
            results = results[:limit]
        
        return results
    
    def get_revenue_by_source(
        self,
        db: Session,
        days: int = 30
    ) -> List[Dict]:
        """
        Get revenue breakdown by UTM source.
        
        Args:
            db: Database session
            days: Number of days to look back
            
        Returns:
            Revenue breakdown by source
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query revenue by UTM source
        results = db.query(
            TrackingEvent.utm_source,
            func.count(TrackingEvent.id).label('clicks'),
            func.sum(TrackingEvent.revenue).label('revenue')
        ).filter(
            TrackingEvent.created_at >= start_date,
            TrackingEvent.utm_source.isnot(None)
        ).group_by(
            TrackingEvent.utm_source
        ).all()
        
        sources = []
        for source, clicks, revenue in results:
            revenue = revenue or 0.0
            epc = self.calculate_epc(revenue, clicks)
            
            sources.append({
                "source": source,
                "clicks": clicks,
                "revenue": round(revenue, 2),
                "epc": epc
            })
        
        # Sort by revenue
        sources.sort(key=lambda x: x['revenue'], reverse=True)
        
        return sources


# Singleton instance
monetization = MonetizationService()
