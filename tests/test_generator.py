"""
Tests for content generator service.

Validates article generation, quality checks, and content structure.
"""

import pytest
from app.services.generator import ContentGenerator, generator
from app.models import Article, ContentStatus


def test_generate_slug():
    """Test slug generation from title."""
    gen = ContentGenerator()
    
    title = "The Ultimate Guide to Digital Marketing"
    slug = gen.generate_slug(title)
    
    assert slug.startswith("the-ultimate-guide-to-digital-marketing")
    assert len(slug) > len("the-ultimate-guide-to-digital-marketing")  # Has hash suffix
    assert "-" in slug
    assert slug.islower() or "-" in slug  # Lowercase with hyphens


def test_generate_title():
    """Test title generation from keyword."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    title = gen.generate_title(keyword)
    
    assert len(title) > 10
    assert "digital marketing" in title.lower()


def test_generate_meta_description():
    """Test meta description generation."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    title = "The Ultimate Guide to Digital Marketing"
    meta = gen.generate_meta_description(keyword, title)
    
    assert len(meta) > 50
    assert len(meta) <= 160  # SEO best practice
    assert keyword in meta.lower()


def test_generate_headings():
    """Test heading structure generation."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    headings = gen.generate_headings(keyword)
    
    assert len(headings) >= 5  # Minimum structure
    assert headings[0]["level"] == "h1"  # First should be H1
    
    # Check for h2 and h3 presence
    levels = [h["level"] for h in headings]
    assert "h2" in levels
    assert "h3" in levels


def test_generate_body_html():
    """Test body content generation."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    headings = gen.generate_headings(keyword)
    html_body, plain_body = gen.generate_body_html(keyword, headings)
    
    assert len(html_body) > 0
    assert len(plain_body) > 0
    # H1 is skipped in body (rendered as page title in template)
    assert "<h2>" in html_body
    assert "<h3>" in html_body
    assert "<h2>" in html_body
    assert keyword in plain_body.lower()


def test_count_words():
    """Test word counting."""
    gen = ContentGenerator()
    
    text = "This is a test sentence with ten words in total here."
    count = gen.count_words(text)
    
    assert count == 11  # Actual word count


def test_generate_internal_links():
    """Test internal link suggestions."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    links = gen.generate_internal_links(keyword)
    
    assert len(links) > 0
    assert all("anchor_text" in link for link in links)
    assert all("slug" in link for link in links)


def test_generate_tags():
    """Test tag generation."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    tags = gen.generate_tags(keyword)
    
    assert len(tags) > 0
    assert keyword in tags
    assert len(tags) <= 8  # Max tags


def test_generate_article():
    """Test full article generation."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    article = gen.generate_article(keyword)
    
    # Check article structure
    assert isinstance(article, Article)
    assert article.keyword == keyword
    assert len(article.title) > 10
    assert len(article.meta_description) > 50
    assert len(article.body_html) > 0
    assert len(article.body_plain) > 0
    assert article.word_count > 0
    assert len(article.headings) > 0
    assert len(article.tags) > 0
    assert article.status == ContentStatus.DRAFT
    assert article.review_required is True  # Default


def test_validate_article_success():
    """Test article validation with valid article."""
    gen = ContentGenerator()
    
    keyword = "digital marketing"
    article = gen.generate_article(keyword)
    
    is_valid, errors = gen.validate_article(article)
    
    assert is_valid is True
    assert len(errors) == 0


def test_validate_article_too_short():
    """Test article validation fails for short content."""
    gen = ContentGenerator()
    
    # Create minimal article
    article = Article(
        slug="test-slug",
        keyword="test",
        title="Test Title",
        meta_description="Test meta",
        body_html="<p>Short</p>",
        body_plain="Short",
        word_count=1,  # Too short
        headings=[{"level": "h1", "text": "Title"}],
        internal_links=[],
        tags=["test"],
        status=ContentStatus.DRAFT,
        review_required=True,
    )
    
    is_valid, errors = gen.validate_article(article)
    
    assert is_valid is False
    assert len(errors) > 0
    assert any("too short" in error.lower() for error in errors)


def test_validate_article_missing_title():
    """Test article validation fails for missing title."""
    article = Article(
        slug="test-slug",
        keyword="test",
        title="",  # Missing
        meta_description="Test meta description that is long enough",
        body_html="<p>Body content</p>",
        body_plain="Body content",
        word_count=800,
        headings=[{"level": "h1", "text": "H1"}] * 5,
        internal_links=[],
        tags=["test"],
        status=ContentStatus.DRAFT,
        review_required=True,
    )
    
    gen = ContentGenerator()
    is_valid, errors = gen.validate_article(article)
    
    assert is_valid is False
    assert any("title" in error.lower() for error in errors)


def test_singleton_instance():
    """Test that generator is a singleton."""
    from app.services.generator import generator
    
    assert generator is not None
    assert isinstance(generator, ContentGenerator)


def test_article_word_count_in_range():
    """Test that generated articles are within word count range."""
    gen = ContentGenerator()
    
    keyword = "productivity tools"
    article = gen.generate_article(keyword)
    
    # Should be within configured range
    assert article.word_count >= gen.min_words
    assert article.word_count <= gen.max_words


def test_slug_uniqueness():
    """Test that slugs are unique (have timestamp hash)."""
    gen = ContentGenerator()
    
    title = "Same Title"
    slug1 = gen.generate_slug(title)
    slug2 = gen.generate_slug(title)
    
    # Should be different due to timestamp hash
    assert slug1 != slug2
