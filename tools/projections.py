#!/usr/bin/env python3
"""
Revenue and traffic projections tool.

Simulates different growth scenarios to estimate potential revenue.
"""

import json
from dataclasses import dataclass
from typing import List
import math


@dataclass
class Scenario:
    """Growth scenario parameters."""
    name: str
    initial_traffic: int  # Monthly visitors month 1
    growth_rate: float  # Monthly growth rate (0.1 = 10%)
    ctr: float  # Click-through rate (0.03 = 3%)
    conversion_rate: float  # Conversion rate (0.05 = 5%)
    avg_commission: float  # Average commission per conversion


def project_month(
    month: int,
    initial_traffic: int,
    growth_rate: float,
    ctr: float,
    conversion_rate: float,
    avg_commission: float
) -> dict:
    """Calculate projections for a single month."""
    # Traffic growth (compounded)
    traffic = int(initial_traffic * math.pow(1 + growth_rate, month - 1))
    
    # Calculate funnel
    clicks = int(traffic * ctr)
    conversions = int(clicks * conversion_rate)
    revenue = conversions * avg_commission
    
    return {
        "month": month,
        "traffic": traffic,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": round(revenue, 2),
        "cumulative_revenue": 0  # Set later
    }


def run_projection(scenario: Scenario, months: int = 12) -> List[dict]:
    """Run projection for a scenario."""
    results = []
    cumulative_revenue = 0
    
    for month in range(1, months + 1):
        projection = project_month(
            month=month,
            initial_traffic=scenario.initial_traffic,
            growth_rate=scenario.growth_rate,
            ctr=scenario.ctr,
            conversion_rate=scenario.conversion_rate,
            avg_commission=scenario.avg_commission
        )
        
        cumulative_revenue += projection["revenue"]
        projection["cumulative_revenue"] = round(cumulative_revenue, 2)
        
        results.append(projection)
    
    return results


def main():
    """Run all scenarios and display results."""
    print("=" * 80)
    print("autocash-ultimate Revenue Projections")
    print("=" * 80)
    print()
    
    # Define scenarios
    scenarios = [
        Scenario(
            name="Pessimista",
            initial_traffic=100,
            growth_rate=0.05,  # 5% monthly growth
            ctr=0.02,  # 2% CTR
            conversion_rate=0.03,  # 3% conversion
            avg_commission=25.00
        ),
        Scenario(
            name="Realista",
            initial_traffic=500,
            growth_rate=0.15,  # 15% monthly growth
            ctr=0.03,  # 3% CTR
            conversion_rate=0.05,  # 5% conversion
            avg_commission=30.00
        ),
        Scenario(
            name="Otimista",
            initial_traffic=1000,
            growth_rate=0.25,  # 25% monthly growth
            ctr=0.04,  # 4% CTR
            conversion_rate=0.07,  # 7% conversion
            avg_commission=35.00
        ),
        Scenario(
            name="Agressivo",
            initial_traffic=2000,
            growth_rate=0.35,  # 35% monthly growth
            ctr=0.05,  # 5% CTR
            conversion_rate=0.10,  # 10% conversion
            avg_commission=40.00
        ),
    ]
    
    all_results = {}
    
    for scenario in scenarios:
        print(f"\n{scenario.name.upper()} Scenario")
        print("-" * 80)
        print(f"Initial Traffic: {scenario.initial_traffic:,} visits/month")
        print(f"Growth Rate: {scenario.growth_rate * 100:.0f}% monthly")
        print(f"CTR: {scenario.ctr * 100:.1f}%")
        print(f"Conversion Rate: {scenario.conversion_rate * 100:.1f}%")
        print(f"Avg Commission: ${scenario.avg_commission:.2f}")
        print()
        
        results = run_projection(scenario, months=12)
        
        # Print monthly table
        print(f"{'Month':<6} {'Traffic':<10} {'Clicks':<8} {'Conv':<7} {'Revenue':<10} {'Cumul. Rev'}")
        print("-" * 80)
        
        for r in results:
            print(
                f"{r['month']:<6} "
                f"{r['traffic']:<10,} "
                f"{r['clicks']:<8,} "
                f"{r['conversions']:<7,} "
                f"${r['revenue']:<9,.2f} "
                f"${r['cumulative_revenue']:,.2f}"
            )
        
        # Summary
        print("-" * 80)
        final = results[-1]
        print(f"12-Month Total Revenue: ${final['cumulative_revenue']:,.2f}")
        print(f"Final Monthly Revenue: ${final['revenue']:,.2f}")
        print(f"Final Monthly Traffic: {final['traffic']:,}")
        print()
        
        all_results[scenario.name.lower()] = results
    
    # Save to JSON
    with open('revenue_projections.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("=" * 80)
    print("Projections saved to: revenue_projections.json")
    print("=" * 80)
    print()
    print("NOTES:")
    print("- These are theoretical projections for planning purposes")
    print("- Actual results depend on content quality, SEO, and market conditions")
    print("- Start with pessimistic/realistic scenarios for planning")
    print("- Reinvest profits for faster growth")
    print("- Focus on high-quality content and user value")
    print()


if __name__ == "__main__":
    main()
