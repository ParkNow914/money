"""
Tests for monetization service and routes.

Tests affiliate link management, EPC calculations, and revenue reporting.
"""

import pytest
from datetime import datetime, timedelta
from app.services.monetization import MonetizationService
from app.models import AffiliateLink, TrackingEvent, Article, ContentStatus
from app.db import get_db


def test_calculate_epc():
    """Test EPC calculation."""
    service = MonetizationService()
    
    # Normal case
    epc = service.calculate_epc(revenue=100.0, clicks=50)
    assert epc == 2.0
    
    # Zero clicks
    epc = service.calculate_epc(revenue=100.0, clicks=0)
    assert epc == 0.0
    
    # Decimal result
    epc = service.calculate_epc(revenue=75.0, clicks=30)
    assert epc == 2.5


def test_calculate_conversion_rate():
    """Test conversion rate calculation."""
    service = MonetizationService()
    
    # Normal case
    rate = service.calculate_conversion_rate(conversions=10, clicks=100)
    assert rate == 10.0
    
    # Zero clicks
    rate = service.calculate_conversion_rate(conversions=10, clicks=0)
    assert rate == 0.0
    
    # Fractional result
    rate = service.calculate_conversion_rate(conversions=3, clicks=50)
    assert rate == 6.0


def test_calculate_ctr():
    """Test CTR calculation."""
    service = MonetizationService()
    
    # Normal case
    ctr = service.calculate_ctr(clicks=50, views=1000)
    assert ctr == 5.0
    
    # Zero views
    ctr = service.calculate_ctr(clicks=50, views=0)
    assert ctr == 0.0


def test_get_affiliate_link_stats(test_db):
    """Test getting affiliate link statistics."""
    db = test_db
    service = MonetizationService()
    
    # Clear existing data first
    db.query(AffiliateLink).filter(AffiliateLink.link_id == "test-link-1").delete()
    db.commit()
    
    # Create affiliate link
    link = AffiliateLink(
        link_id="test-link-1",
        name="Test Product",
        destination_url="https://example.com/product",
        affiliate_program="amazon",
        commission_rate=10.0,
        clicks=100,
        conversions=5,
        revenue=250.0,
        created_at=datetime.utcnow()
    )
    db.add(link)
    db.commit()
    
    # Get stats
    stats = service.get_affiliate_link_stats(db, "test-link-1")
    
    assert stats is not None
    assert stats["link_id"] == "test-link-1"
    assert stats["clicks"] == 100
    assert stats["conversions"] == 5
    assert stats["revenue"] == 250.0
    assert stats["epc"] == 2.5
    assert stats["conversion_rate"] == 5.0


def test_get_affiliate_link_stats_not_found(test_db):
    """Test getting stats for non-existent link."""
    db = test_db
    service = MonetizationService()
    
    stats = service.get_affiliate_link_stats(db, "non-existent")
    assert stats is None


def test_get_revenue_by_period(test_db):
    """Test revenue statistics for a time period."""
    db = test_db
    service = MonetizationService()
    
    # Clear existing data first
    db.query(TrackingEvent).delete()
    db.commit()
    
    # Create tracking events
    for i in range(5):
        event = TrackingEvent(
            event_type="click",
            session_hash=f"session_{i}",
            revenue=10.0 if i < 2 else None,
            created_at=datetime.utcnow()
        )
        db.add(event)
    
    # Add conversion
    conversion = TrackingEvent(
        event_type="conversion",
        session_hash="session_conv",
        revenue=50.0,
        created_at=datetime.utcnow()
    )
    db.add(conversion)
    db.commit()
    
    # Get stats
    stats = service.get_revenue_by_period(db, days=30)
    
    assert stats["total_clicks"] == 5
    assert stats["total_conversions"] == 1
    assert stats["total_revenue"] == 70.0  # 10 + 10 + 50
    assert stats["epc"] == 14.0  # 70 / 5


def test_get_top_performing_links(test_db):
    """Test getting top performing links."""
    db = test_db
    service = MonetizationService()
    
    # Clear existing data first
    db.query(AffiliateLink).delete()
    db.commit()
    
    # Create multiple links
    links_data = [
        ("link-1", "Product 1", 100, 5, 250.0),
        ("link-2", "Product 2", 200, 10, 300.0),
        ("link-3", "Product 3", 50, 2, 100.0),
    ]
    
    for link_id, name, clicks, conversions, revenue in links_data:
        link = AffiliateLink(
            link_id=link_id,
            name=name,
            destination_url=f"https://example.com/{link_id}",
            affiliate_program="test",
            clicks=clicks,
            conversions=conversions,
            revenue=revenue,
            created_at=datetime.utcnow()
        )
        db.add(link)
    db.commit()
    
    # Get top by revenue
    top_links = service.get_top_performing_links(db, limit=2, order_by='revenue')
    
    assert len(top_links) == 2
    assert top_links[0]["link_id"] == "link-2"  # Highest revenue
    assert top_links[1]["link_id"] == "link-1"
    
    # Get top by clicks
    top_links = service.get_top_performing_links(db, limit=2, order_by='clicks')
    
    assert len(top_links) == 2
    assert top_links[0]["link_id"] == "link-2"  # Most clicks


def test_get_revenue_by_source(test_db):
    """Test revenue breakdown by UTM source."""
    db = test_db
    service = MonetizationService()
    
    # Clear existing data first
    db.query(TrackingEvent).delete()
    db.commit()
    
    # Create events with different sources - simpler test
    # Google: 2 events with revenue
    db.add(TrackingEvent(
        event_type="click",
        session_hash="session_google_1",
        utm_source="google",
        revenue=50.0,
        created_at=datetime.utcnow()
    ))
    db.add(TrackingEvent(
        event_type="click",
        session_hash="session_google_2",
        utm_source="google",
        revenue=30.0,
        created_at=datetime.utcnow()
    ))
    
    # Facebook: 1 event with revenue
    db.add(TrackingEvent(
        event_type="click",
        session_hash="session_facebook_1",
        utm_source="facebook",
        revenue=20.0,
        created_at=datetime.utcnow()
    ))
    db.commit()
    
    # Get breakdown
    sources = service.get_revenue_by_source(db, days=30)
    
    assert len(sources) == 2  # google and facebook
    # Google should have highest revenue
    assert sources[0]["source"] == "google"
    assert sources[0]["revenue"] == 80.0  # 50 + 30
    assert sources[0]["clicks"] == 2


@pytest.fixture
def test_db():
    """Create a test database session."""
    from app.db import SessionLocal, init_db
    
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
