#!/usr/bin/env python3
"""
Generate sample posts for demonstration.

This script generates 5 high-quality sample posts and saves them to examples/sample_posts.json
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.services.generator import generator
from app.models import ContentStatus


def generate_sample_posts(keywords: list[str], output_file: str = "examples/sample_posts.json"):
    """Generate sample posts and save to JSON."""
    print(f"🎨 Generating {len(keywords)} sample posts...")
    
    posts = []
    
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] Generating article for: '{keyword}'")
        
        # Generate article
        article = generator.generate_article(keyword)
        
        # Validate
        is_valid, errors = generator.validate_article(article)
        if not is_valid:
            print(f"  ⚠️  Validation failed: {', '.join(errors)}")
            continue
        
        print(f"  ✅ Generated: '{article.title}'")
        print(f"     - Slug: {article.slug}")
        print(f"     - Words: {article.word_count}")
        print(f"     - Headings: {len(article.headings)}")
        print(f"     - Tags: {', '.join(article.tags)}")
        
        # Convert to dict for JSON
        post_data = {
            "slug": article.slug,
            "keyword": article.keyword,
            "title": article.title,
            "meta_description": article.meta_description,
            "body_html": article.body_html,
            "body_plain": article.body_plain,
            "word_count": article.word_count,
            "headings": article.headings,
            "internal_links": article.internal_links,
            "tags": article.tags,
            "status": article.status.value,
            "review_required": article.review_required,
            "created_at": article.created_at.isoformat() if article.created_at else None,
        }
        
        posts.append(post_data)
    
    # Save to JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully generated {len(posts)} posts")
    print(f"📁 Saved to: {output_path}")
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   Total articles: {len(posts)}")
    print(f"   Total words: {sum(p['word_count'] for p in posts):,}")
    print(f"   Avg words/article: {sum(p['word_count'] for p in posts) // len(posts):,}")
    print(f"   Review required: {sum(1 for p in posts if p['review_required'])}/{len(posts)}")
    
    return posts


def main():
    """Main function."""
    # Sample keywords for demonstration
    sample_keywords = [
        "digital marketing",
        "passive income ideas",
        "productivity tools",
        "personal finance tips",
        "content creation strategies",
    ]
    
    print("🚀 autocash-ultimate Sample Post Generator")
    print("=" * 50)
    
    # Generate posts
    posts = generate_sample_posts(sample_keywords)
    
    if posts:
        print("\n✨ Sample generation complete!")
        print("\n💡 Next steps:")
        print("   1. Review generated content in examples/sample_posts.json")
        print("   2. Verify quality and SEO structure")
        print("   3. Test with actual database: docker-compose up")
        print("   4. Approve for publication if quality is acceptable")
    else:
        print("\n❌ No posts generated - check for errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
