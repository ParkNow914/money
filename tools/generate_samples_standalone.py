#!/usr/bin/env python3
"""
Standalone sample post generator (no external dependencies).
Demonstrates the structure and content generation logic.
"""

import json
import hashlib
import random
import re
from datetime import datetime
from pathlib import Path


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    
    # Add timestamp hash to ensure uniqueness
    timestamp = datetime.utcnow().isoformat()
    hash_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:6]
    
    return f"{slug}-{hash_suffix}"


def generate_title(keyword: str) -> str:
    """Generate SEO-optimized title from keyword."""
    templates = [
        f"The Ultimate Guide to {keyword.title()}: Everything You Need to Know",
        f"How to Master {keyword.title()}: A Comprehensive Guide",
        f"{keyword.title()}: Complete Beginner's Guide for 2025",
        f"Top 10 Tips for {keyword.title()} Success",
        f"{keyword.title()} Explained: Essential Strategies and Best Practices",
    ]
    return random.choice(templates)


def generate_meta_description(keyword: str) -> str:
    """Generate meta description for SEO."""
    templates = [
        f"Discover everything about {keyword} in this comprehensive guide. Learn proven strategies, expert tips, and best practices to achieve success.",
        f"Learn {keyword} with our detailed guide. Get expert insights, actionable tips, and proven strategies for beginners and professionals.",
        f"Master {keyword} with this complete guide. Discover essential tips, techniques, and strategies to help you succeed in 2025.",
    ]
    return random.choice(templates)[:160]


def generate_headings(keyword: str) -> list:
    """Generate article heading structure."""
    return [
        {"level": "h1", "text": f"The Ultimate Guide to {keyword.title()}"},
        {"level": "h2", "text": f"What is {keyword.title()}?"},
        {"level": "h3", "text": f"Understanding the Basics of {keyword.title()}"},
        {"level": "h3", "text": f"Why {keyword.title()} Matters"},
        {"level": "h2", "text": f"Getting Started with {keyword.title()}"},
        {"level": "h3", "text": "Essential Tools and Resources"},
        {"level": "h3", "text": "Step-by-Step Getting Started Guide"},
        {"level": "h2", "text": f"Best Practices for {keyword.title()}"},
        {"level": "h3", "text": "Common Mistakes to Avoid"},
        {"level": "h3", "text": "Pro Tips for Success"},
        {"level": "h2", "text": f"Advanced {keyword.title()} Strategies"},
        {"level": "h3", "text": "Optimization Techniques"},
        {"level": "h2", "text": "Conclusion and Next Steps"},
    ]


def generate_body_section(heading_text: str, keyword: str) -> str:
    """Generate content for a section."""
    templates = [
        f"When it comes to {keyword}, understanding the fundamentals is crucial for success. "
        f"This aspect of {heading_text.lower()} plays a vital role in achieving your goals. "
        f"By focusing on the key principles and best practices, you can develop a strong foundation "
        f"that will serve you well as you progress in your journey.",
        
        f"Many people overlook the importance of {heading_text.lower()} when working with {keyword}. "
        f"However, experienced practitioners know that paying attention to these details can make "
        f"a significant difference in your results. Taking the time to master this area will pay "
        f"dividends in the long run and help you avoid common pitfalls.",
        
        f"The key to success with {keyword} lies in consistent application of proven strategies. "
        f"When addressing {heading_text.lower()}, it's essential to maintain a systematic approach. "
        f"Start with the basics, build your knowledge gradually, and don't be afraid to experiment "
        f"with different techniques to find what works best for your specific situation.",
    ]
    
    num_paragraphs = random.randint(2, 3)
    return "\n\n".join(random.choice(templates) for _ in range(num_paragraphs))


def generate_body(keyword: str, headings: list) -> tuple:
    """Generate HTML and plain text body content."""
    html_parts = []
    plain_parts = []
    
    for heading in headings:
        level = heading["level"]
        text = heading["text"]
        
        # Add heading
        html_parts.append(f"<{level}>{text}</{level}>")
        plain_parts.append(f"\n{'#' * int(level[1])} {text}\n")
        
        # Add section content (skip for h1)
        if level != "h1":
            section_content = generate_body_section(text, keyword)
            html_parts.append(f"<div class='section'>{section_content}</div>")
            plain_parts.append(section_content)
    
    return "\n\n".join(html_parts), "\n\n".join(plain_parts)


def count_words(text: str) -> int:
    """Count words in text."""
    return len(re.findall(r'\b\w+\b', text))


def generate_article(keyword: str) -> dict:
    """Generate a complete article from a keyword."""
    title = generate_title(keyword)
    slug = generate_slug(title)
    meta_description = generate_meta_description(keyword)
    headings = generate_headings(keyword)
    body_html, body_plain = generate_body(keyword, headings)
    word_count = count_words(body_plain)
    
    tags = [keyword] + ["guide", "tutorial", "tips"]
    
    return {
        "slug": slug,
        "keyword": keyword,
        "title": title,
        "meta_description": meta_description,
        "body_html": body_html,
        "body_plain": body_plain,
        "word_count": word_count,
        "headings": headings,
        "internal_links": [
            {"anchor_text": f"{keyword} tools", "slug": generate_slug(f"{keyword} tools")},
            {"anchor_text": f"{keyword} strategies", "slug": generate_slug(f"{keyword} strategies")},
        ],
        "tags": tags,
        "status": "draft",
        "review_required": True,
        "created_at": datetime.utcnow().isoformat(),
    }


def main():
    """Generate sample posts."""
    keywords = [
        "digital marketing",
        "passive income ideas",
        "productivity tools",
        "personal finance tips",
        "content creation strategies",
    ]
    
    print("🚀 autocash-ultimate Sample Post Generator")
    print("=" * 50)
    print(f"🎨 Generating {len(keywords)} sample posts...\n")
    
    posts = []
    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keywords)}] Generating: '{keyword}'")
        article = generate_article(keyword)
        posts.append(article)
        print(f"  ✅ {article['title'][:60]}...")
        print(f"     Words: {article['word_count']}, Headings: {len(article['headings'])}")
    
    # Save to JSON
    output_path = Path("examples/sample_posts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully generated {len(posts)} posts")
    print(f"📁 Saved to: {output_path}")
    print(f"\n📊 Summary:")
    print(f"   Total words: {sum(p['word_count'] for p in posts):,}")
    print(f"   Avg words/article: {sum(p['word_count'] for p in posts) // len(posts):,}")
    

if __name__ == "__main__":
    main()
