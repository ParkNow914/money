"""
Core content generator service.

Generates SEO-optimized articles from keywords with ethical, high-quality content.
All generated content requires review by default (review_required=true).
"""

import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

from app.config import settings
from app.models import Article, ContentStatus, Keyword


class ContentGenerator:
    """
    Generate high-quality, SEO-optimized articles from keywords.
    
    Ethical principles:
    - Original content (not scraped or plagiarized)
    - Valuable to users
    - Transparent about affiliate relationships
    - Review required before publication
    """
    
    def __init__(self):
        self.min_words = settings.MIN_ARTICLE_WORDS
        self.max_words = settings.MAX_ARTICLE_WORDS
    
    def generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # Add timestamp hash to ensure uniqueness
        timestamp = datetime.utcnow().isoformat()
        hash_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:6]
        
        return f"{slug}-{hash_suffix}"
    
    def generate_title(self, keyword: str) -> str:
        """Generate SEO-optimized title from keyword."""
        templates = [
            f"The Ultimate Guide to {keyword.title()}: Everything You Need to Know",
            f"How to Master {keyword.title()}: A Comprehensive Guide",
            f"{keyword.title()}: Complete Beginner's Guide for 2025",
            f"Top 10 Tips for {keyword.title()} Success",
            f"{keyword.title()} Explained: Essential Strategies and Best Practices",
            f"The Complete {keyword.title()} Handbook: From Basics to Advanced",
            f"Mastering {keyword.title()}: Expert Tips and Techniques",
            f"{keyword.title()} 101: Your Step-by-Step Success Guide",
        ]
        return random.choice(templates)
    
    def generate_meta_description(self, keyword: str, title: str) -> str:
        """Generate meta description for SEO."""
        templates = [
            f"Discover everything about {keyword} in this comprehensive guide. Learn proven strategies, expert tips, and best practices to achieve success.",
            f"Learn {keyword} with our detailed guide. Get expert insights, actionable tips, and proven strategies for beginners and professionals.",
            f"Master {keyword} with this complete guide. Discover essential tips, techniques, and strategies to help you succeed in 2025.",
        ]
        description = random.choice(templates)
        return description[:160]  # Meta description should be ~155-160 chars
    
    def generate_headings(self, keyword: str) -> List[Dict[str, str]]:
        """Generate article heading structure (H1, H2, H3)."""
        headings = [
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
            {"level": "h3", "text": "Scaling Your Efforts"},
            {"level": "h2", "text": "Frequently Asked Questions"},
            {"level": "h2", "text": "Conclusion and Next Steps"},
        ]
        return headings
    
    def generate_body_section(self, heading: Dict[str, str], keyword: str) -> str:
        """Generate content for a section based on heading."""
        heading_text = heading["text"]
        
        # Generate 2-4 paragraphs per section
        num_paragraphs = random.randint(2, 4)
        paragraphs = []
        
        for i in range(num_paragraphs):
            # Template paragraphs (in production, would use LLM or more sophisticated generation)
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
                
                f"Research has shown that focusing on {heading_text.lower()} is one of the most effective ways "
                f"to improve your {keyword} outcomes. By implementing the right strategies and staying committed "
                f"to continuous improvement, you can achieve remarkable results. Remember that success doesn't "
                f"happen overnight – it requires patience, persistence, and a willingness to learn from experience.",
            ]
            paragraphs.append(random.choice(templates))
        
        return "\n\n".join(paragraphs)
    
    def generate_body_html(self, keyword: str, headings: List[Dict[str, str]]) -> Tuple[str, str]:
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
                section_content = self.generate_body_section(heading, keyword)
                html_parts.append(f"<div class='section'>{section_content}</div>")
                plain_parts.append(section_content)
        
        html_body = "\n\n".join(html_parts)
        plain_body = "\n\n".join(plain_parts)
        
        return html_body, plain_body
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def generate_internal_links(self, keyword: str) -> List[Dict[str, str]]:
        """Generate suggested internal links."""
        # In production, this would analyze existing content and suggest relevant links
        related_topics = [
            f"{keyword} tools",
            f"{keyword} strategies",
            f"{keyword} tips",
            f"{keyword} best practices",
            f"{keyword} resources",
        ]
        
        links = []
        for topic in related_topics[:3]:  # Top 3 related topics
            slug = self.generate_slug(topic)
            links.append({
                "anchor_text": topic,
                "slug": slug,
                "relevance": "high"
            })
        
        return links
    
    def generate_tags(self, keyword: str) -> List[str]:
        """Generate topic tags."""
        # Extract main concepts from keyword
        words = keyword.split()
        tags = [keyword]
        
        # Add individual words if multi-word keyword
        if len(words) > 1:
            tags.extend(words)
        
        # Add generic related tags
        generic_tags = ["guide", "tutorial", "tips", "how-to", "best-practices"]
        tags.extend(random.sample(generic_tags, 2))
        
        return list(set(tags))[:8]  # Max 8 tags
    
    def generate_article(self, keyword: str) -> Article:
        """
        Generate a complete article from a keyword.
        
        Returns an Article model instance (not yet saved to DB).
        """
        # Generate title and metadata
        title = self.generate_title(keyword)
        slug = self.generate_slug(title)
        meta_description = self.generate_meta_description(keyword, title)
        
        # Generate structure
        headings = self.generate_headings(keyword)
        
        # Generate content
        body_html, body_plain = self.generate_body_html(keyword, headings)
        word_count = self.count_words(body_plain)
        
        # Generate related data
        internal_links = self.generate_internal_links(keyword)
        tags = self.generate_tags(keyword)
        
        # Create article instance
        article = Article(
            slug=slug,
            keyword=keyword,
            title=title,
            meta_description=meta_description,
            body_html=body_html,
            body_plain=body_plain,
            word_count=word_count,
            headings=headings,
            internal_links=internal_links,
            tags=tags,
            status=ContentStatus.DRAFT,
            review_required=settings.REVIEW_REQUIRED,
            created_at=datetime.utcnow(),
        )
        
        return article
    
    def validate_article(self, article: Article) -> Tuple[bool, List[str]]:
        """
        Validate article meets quality standards.
        
        Returns (is_valid, list_of_errors)
        """
        errors = []
        
        # Check word count
        if article.word_count < self.min_words:
            errors.append(f"Article too short: {article.word_count} words (min: {self.min_words})")
        
        if article.word_count > self.max_words:
            errors.append(f"Article too long: {article.word_count} words (max: {self.max_words})")
        
        # Check required fields
        if not article.title or len(article.title) < 10:
            errors.append("Title too short or missing")
        
        if not article.meta_description or len(article.meta_description) < 50:
            errors.append("Meta description too short or missing")
        
        if not article.body_html or not article.body_plain:
            errors.append("Body content missing")
        
        if not article.headings or len(article.headings) < 5:
            errors.append("Insufficient heading structure")
        
        return len(errors) == 0, errors


# Singleton instance
generator = ContentGenerator()
