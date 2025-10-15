#!/usr/bin/env python3
"""
Example script demonstrating monetization features.

This script shows how to:
1. Create affiliate links
2. Track clicks and conversions
3. Calculate EPC and revenue metrics
4. Generate revenue reports

Usage:
    python examples/monetization_demo.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.monetization import MonetizationService
from app.models import AffiliateLink, TrackingEvent
from app.db import SessionLocal, init_db
from datetime import datetime, timedelta


def main():
    """Run the monetization demo."""
    print("=" * 60)
    print("Monetization Demo - autocash-ultimate v0.3.0")
    print("=" * 60)
    print()
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        service = MonetizationService()
        
        # Step 1: Create Affiliate Links
        print("Step 1: Creating affiliate links...")
        
        # Clear existing demo links
        db.query(AffiliateLink).filter(
            AffiliateLink.link_id.in_(['demo-amazon-book', 'demo-clickbank-course'])
        ).delete()
        db.commit()
        
        links_data = [
            {
                'link_id': 'demo-amazon-book',
                'name': 'Content Marketing Book',
                'destination_url': 'https://amazon.com/content-marketing-book',
                'affiliate_program': 'amazon',
                'commission_rate': 8.0,
                'commission_type': 'percentage',
                'product_category': 'books'
            },
            {
                'link_id': 'demo-clickbank-course',
                'name': 'Digital Marketing Course',
                'destination_url': 'https://clickbank.com/marketing-course',
                'affiliate_program': 'clickbank',
                'commission_rate': 50.0,
                'commission_type': 'percentage',
                'product_category': 'courses'
            }
        ]
        
        for link_data in links_data:
            link = AffiliateLink(**link_data, created_at=datetime.utcnow())
            db.add(link)
        
        db.commit()
        print(f"✓ Created {len(links_data)} affiliate links")
        print()
        
        # Step 2: Simulate Clicks and Conversions
        print("Step 2: Simulating traffic and conversions...")
        
        # Amazon book: 100 clicks, 5 conversions, $50 revenue
        amazon_link = db.query(AffiliateLink).filter(
            AffiliateLink.link_id == 'demo-amazon-book'
        ).first()
        amazon_link.clicks = 100
        amazon_link.conversions = 5
        amazon_link.revenue = 50.0
        
        # ClickBank course: 50 clicks, 3 conversions, $150 revenue
        clickbank_link = db.query(AffiliateLink).filter(
            AffiliateLink.link_id == 'demo-clickbank-course'
        ).first()
        clickbank_link.clicks = 50
        clickbank_link.conversions = 3
        clickbank_link.revenue = 150.0
        
        db.commit()
        
        print("  Amazon Book:")
        print(f"    Clicks: {amazon_link.clicks}")
        print(f"    Conversions: {amazon_link.conversions}")
        print(f"    Revenue: ${amazon_link.revenue}")
        print()
        
        print("  ClickBank Course:")
        print(f"    Clicks: {clickbank_link.clicks}")
        print(f"    Conversions: {clickbank_link.conversions}")
        print(f"    Revenue: ${clickbank_link.revenue}")
        print()
        
        # Step 3: Calculate Metrics
        print("Step 3: Calculating performance metrics...")
        
        # EPC for each link
        amazon_epc = service.calculate_epc(amazon_link.revenue, amazon_link.clicks)
        clickbank_epc = service.calculate_epc(clickbank_link.revenue, clickbank_link.clicks)
        
        print(f"\n  Amazon Book EPC: ${amazon_epc}")
        print(f"  ClickBank Course EPC: ${clickbank_epc}")
        
        # Conversion rates
        amazon_cr = service.calculate_conversion_rate(amazon_link.conversions, amazon_link.clicks)
        clickbank_cr = service.calculate_conversion_rate(clickbank_link.conversions, clickbank_link.clicks)
        
        print(f"\n  Amazon Book Conversion Rate: {amazon_cr}%")
        print(f"  ClickBank Course Conversion Rate: {clickbank_cr}%")
        print()
        
        # Step 4: Get Top Performing Links
        print("Step 4: Getting top performing links...")
        
        top_by_revenue = service.get_top_performing_links(db, limit=5, order_by='revenue')
        top_by_epc = service.get_top_performing_links(db, limit=5, order_by='epc')
        
        print("\n  Top by Revenue:")
        for i, link in enumerate(top_by_revenue[:3], 1):
            print(f"    {i}. {link['name']}: ${link['revenue']} (EPC: ${link['epc']})")
        
        print("\n  Top by EPC:")
        for i, link in enumerate(top_by_epc[:3], 1):
            print(f"    {i}. {link['name']}: ${link['epc']} (Revenue: ${link['revenue']})")
        print()
        
        # Step 5: Simulate UTM Tracking
        print("Step 5: Simulating UTM-based traffic...")
        
        # Clear existing tracking events
        db.query(TrackingEvent).delete()
        db.commit()
        
        # Create tracking events with different UTM sources
        utm_data = [
            ('google', 10, 30.0),
            ('facebook', 5, 15.0),
            ('twitter', 3, 9.0)
        ]
        
        for source, clicks, revenue in utm_data:
            for i in range(clicks):
                event = TrackingEvent(
                    event_type='click',
                    session_hash=f'demo_{source}_{i}',
                    utm_source=source,
                    revenue=revenue / clicks if i == 0 else None,
                    created_at=datetime.utcnow()
                )
                db.add(event)
        
        db.commit()
        
        # Get revenue by source
        revenue_by_source = service.get_revenue_by_source(db, days=30)
        
        print("\n  Revenue by UTM Source:")
        for source_data in revenue_by_source:
            print(f"    {source_data['source']}: ${source_data['revenue']} "
                  f"({source_data['clicks']} clicks, EPC: ${source_data['epc']})")
        print()
        
        # Step 6: Generate Period Report
        print("Step 6: Generating 30-day revenue report...")
        
        period_stats = service.get_revenue_by_period(db, days=30)
        
        print(f"\n  Period: {period_stats['period_days']} days")
        print(f"  Total Clicks: {period_stats['total_clicks']}")
        print(f"  Total Conversions: {period_stats['total_conversions']}")
        print(f"  Total Revenue: ${period_stats['total_revenue']}")
        print(f"  EPC: ${period_stats['epc']}")
        print(f"  Conversion Rate: {period_stats['conversion_rate']}%")
        print(f"  Average Daily Revenue: ${period_stats['average_daily_revenue']}")
        print()
        
        print("=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  ✓ Created and tracked {len(links_data)} affiliate links")
        print(f"  ✓ Simulated {150} total clicks")
        print(f"  ✓ Tracked {8} conversions")
        print(f"  ✓ Generated ${200} in revenue")
        print(f"  ✓ Analyzed {len(utm_data)} traffic sources")
        print()
        print("Next steps:")
        print("  1. Use the API to create real affiliate links")
        print("  2. Integrate tracking pixels in your content")
        print("  3. Set up conversion webhooks from affiliate networks")
        print("  4. Monitor revenue reports daily")
        print("  5. Optimize for highest EPC links")
        print()
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
