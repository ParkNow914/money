#!/usr/bin/env python3
"""
Example script demonstrating the content pipeline workflow.

This script shows how to:
1. Generate an article
2. Publish it as static HTML
3. Repurpose it into different formats (thread, video, email, PDF)

Usage:
    python examples/content_pipeline_demo.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.generator import ContentGenerator
from app.services.publisher import Publisher
from app.services.repurposer import ContentRepurposer
from app.models import Article
import json


def main():
    """Run the content pipeline demo."""
    print("=" * 60)
    print("Content Pipeline Demo - autocash-ultimate")
    print("=" * 60)
    print()
    
    # Step 1: Generate Article
    print("Step 1: Generating article...")
    generator = ContentGenerator()
    article = generator.generate_article("content marketing")
    
    print(f"✓ Generated article: {article.title}")
    print(f"  - Slug: {article.slug}")
    print(f"  - Word count: {article.word_count}")
    print(f"  - Tags: {', '.join(article.tags)}")
    print()
    
    # Step 2: Publish as HTML
    print("Step 2: Publishing to static HTML...")
    publisher = Publisher()
    
    # Publish single article
    output_file = publisher.publish_article(
        article,
        site_name="AutoCash Demo",
        base_url="https://demo.autocash.com"
    )
    print(f"✓ Published to: {output_file}")
    print()
    
    # Step 3: Repurpose to different formats
    print("Step 3: Repurposing content...")
    repurposer = ContentRepurposer()
    
    # 3a. Twitter/X Thread
    print("\n  3a. Creating Twitter/X thread...")
    thread = repurposer.repurpose_to_thread(article, max_tweets=8)
    print(f"  ✓ Created thread with {thread['tweet_count']} tweets")
    print(f"    First tweet: {thread['tweets'][0]['text'][:80]}...")
    
    # 3b. Video Script
    print("\n  3b. Creating video script...")
    video = repurposer.repurpose_to_video_script(article, duration_minutes=5)
    print(f"  ✓ Created {video['duration_minutes']}-minute video script")
    print(f"    Sections: {len(video['sections'])}")
    
    # 3c. Email Newsletter
    print("\n  3c. Creating email newsletter...")
    email = repurposer.repurpose_to_email(article)
    print(f"  ✓ Created email newsletter")
    print(f"    Subject: {email['subject']}")
    print(f"    Key points: {len(email['sections']['key_points'])}")
    
    # 3d. PDF Outline
    print("\n  3d. Creating PDF outline...")
    pdf = repurposer.repurpose_to_pdf_outline(article)
    print(f"  ✓ Created PDF outline")
    print(f"    Total pages: {pdf['metadata']['total_pages']}")
    
    print()
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - HTML: {output_file}")
    print(f"  - Thread data: {len(json.dumps(thread))} bytes")
    print(f"  - Video script: {len(json.dumps(video))} bytes")
    print(f"  - Email data: {len(json.dumps(email))} bytes")
    print(f"  - PDF outline: {len(json.dumps(pdf))} bytes")
    print()
    print("Next steps:")
    print("  1. Review the generated HTML file")
    print("  2. Use the thread data to post on Twitter/X")
    print("  3. Create a video using the script")
    print("  4. Send the email newsletter to subscribers")
    print("  5. Generate the actual PDF from the outline")
    print()


if __name__ == "__main__":
    main()
