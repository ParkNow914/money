"""
Tests for content repurposer service.

Tests content transformation into various formats (threads, videos, emails, PDFs).
"""

import pytest
from datetime import datetime

from app.services.repurposer import ContentRepurposer
from app.models import Article, ContentStatus


def test_repurposer_initialization():
    """Test repurposer initializes correctly."""
    repurposer = ContentRepurposer()
    assert repurposer is not None


def test_repurpose_to_thread():
    """Test converting article to Twitter/X thread."""
    article = Article(
        slug="test-article",
        keyword="digital marketing",
        title="The Ultimate Guide to Digital Marketing",
        meta_description="Learn digital marketing basics",
        body_html="<p>Content</p>",
        body_plain="Content",
        word_count=800,
        headings=[
            {"level": "h1", "text": "Digital Marketing Guide"},
            {"level": "h2", "text": "What is Digital Marketing?"},
            {"level": "h2", "text": "Benefits of Digital Marketing"},
            {"level": "h2", "text": "Getting Started"},
        ],
        tags=["marketing", "digital"],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    thread = repurposer.repurpose_to_thread(article, max_tweets=10)
    
    # Verify thread structure
    assert thread["format"] == "thread"
    assert thread["platform"] == "twitter"
    assert "tweets" in thread
    assert len(thread["tweets"]) > 0
    
    # Verify first tweet is intro
    first_tweet = thread["tweets"][0]
    assert first_tweet["type"] == "intro"
    assert first_tweet["number"] == 1
    assert len(first_tweet["text"]) <= 280
    
    # Verify last tweet is CTA
    last_tweet = thread["tweets"][-1]
    assert last_tweet["type"] == "cta"
    
    # Verify metadata
    assert thread["metadata"]["article_slug"] == article.slug
    assert thread["metadata"]["keyword"] == article.keyword


def test_repurpose_to_video_script():
    """Test converting article to video script."""
    article = Article(
        slug="test-video",
        keyword="productivity",
        title="Top 10 Productivity Tips",
        meta_description="Boost your productivity",
        body_html="<p>Content</p>",
        body_plain="Content",
        word_count=1000,
        headings=[
            {"level": "h1", "text": "Productivity Tips"},
            {"level": "h2", "text": "Time Management"},
            {"level": "h2", "text": "Focus Techniques"},
            {"level": "h2", "text": "Tools and Apps"},
        ],
        tags=["productivity", "tips"],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    script = repurposer.repurpose_to_video_script(article, duration_minutes=5)
    
    # Verify script structure
    assert script["format"] == "video_script"
    assert script["duration_minutes"] == 5
    assert "sections" in script
    assert len(script["sections"]) > 0
    
    # Verify intro section
    intro = script["sections"][0]
    assert intro["type"] == "intro"
    assert intro["timestamp"] == "0:00"
    assert "text" in intro
    assert "visuals" in intro
    
    # Verify outro section
    outro = script["sections"][-1]
    assert outro["type"] == "outro"
    
    # Verify metadata
    assert script["metadata"]["article_slug"] == article.slug
    assert script["metadata"]["total_sections"] == len(script["sections"])


def test_repurpose_to_email():
    """Test converting article to email format."""
    article = Article(
        slug="test-email",
        keyword="email marketing",
        title="Email Marketing Best Practices",
        meta_description="Learn email marketing strategies",
        body_html="<p>Content</p>",
        body_plain="Content",
        word_count=900,
        headings=[
            {"level": "h1", "text": "Email Marketing"},
            {"level": "h2", "text": "Building Your List"},
            {"level": "h2", "text": "Writing Subject Lines"},
            {"level": "h2", "text": "Measuring Success"},
        ],
        tags=["email", "marketing"],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    email = repurposer.repurpose_to_email(article, email_type="newsletter")
    
    # Verify email structure
    assert email["format"] == "email"
    assert email["type"] == "newsletter"
    assert "subject" in email
    assert "preview_text" in email
    assert "sections" in email
    
    # Verify sections
    sections = email["sections"]
    assert "greeting" in sections
    assert "intro" in sections
    assert "key_points" in sections
    assert "cta" in sections
    assert "footer" in sections
    
    # Verify CTA
    assert "text" in sections["cta"]
    assert "url" in sections["cta"]
    assert article.slug in sections["cta"]["url"]
    
    # Verify metadata
    assert email["metadata"]["article_slug"] == article.slug


def test_repurpose_to_pdf_outline():
    """Test converting article to PDF outline."""
    article = Article(
        slug="test-pdf",
        keyword="content marketing",
        title="Content Marketing Handbook",
        meta_description="Complete guide to content marketing",
        body_html="<p>Content</p>",
        body_plain="Content",
        word_count=1200,
        headings=[
            {"level": "h1", "text": "Content Marketing"},
            {"level": "h2", "text": "Strategy"},
            {"level": "h2", "text": "Creation"},
            {"level": "h2", "text": "Distribution"},
        ],
        tags=["content", "marketing"],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    pdf = repurposer.repurpose_to_pdf_outline(article)
    
    # Verify PDF structure
    assert pdf["format"] == "pdf"
    assert pdf["title"] == article.title
    assert "metadata" in pdf
    assert "pages" in pdf
    assert "content_pages" in pdf
    
    # Verify metadata
    assert pdf["metadata"]["subject"] == article.keyword
    assert pdf["metadata"]["article_slug"] == article.slug
    assert "total_pages" in pdf["metadata"]
    
    # Verify pages
    assert len(pdf["pages"]) >= 2  # At least cover + TOC
    assert pdf["pages"][0]["type"] == "cover"
    assert pdf["pages"][1]["type"] == "toc"


def test_create_repurposed_content_thread():
    """Test generic repurpose method for thread."""
    article = Article(
        slug="test",
        keyword="test",
        title="Test Article",
        meta_description="Test",
        body_html="<p>Test</p>",
        body_plain="Test",
        word_count=800,
        headings=[{"level": "h2", "text": "Test Heading"}],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    result = repurposer.create_repurposed_content(article, 'thread')
    
    assert result["format"] == "thread"


def test_create_repurposed_content_invalid_type():
    """Test repurpose with invalid content type."""
    article = Article(
        slug="test",
        keyword="test",
        title="Test",
        meta_description="Test",
        body_html="<p>Test</p>",
        body_plain="Test",
        word_count=800,
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    repurposer = ContentRepurposer()
    
    with pytest.raises(ValueError) as exc_info:
        repurposer.create_repurposed_content(article, 'invalid_type')
    
    assert "Unknown content type" in str(exc_info.value)
