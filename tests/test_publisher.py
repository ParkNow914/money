"""
Tests for publisher service.

Tests static site generation functionality.
"""

import pytest
from pathlib import Path
from datetime import datetime

from app.services.publisher import Publisher
from app.models import Article, ContentStatus


def test_publisher_initialization():
    """Test publisher initializes correctly."""
    publisher = Publisher()
    
    assert publisher.templates_dir.exists()
    assert publisher.output_dir.exists()
    assert publisher.env is not None


def test_publish_article(tmp_path):
    """Test publishing an article to HTML."""
    # Create a test article
    article = Article(
        slug="test-article",
        keyword="testing",
        title="Test Article Title",
        meta_description="This is a test article for unit testing",
        body_html="<p>Test content</p>",
        body_plain="Test content",
        word_count=100,
        headings=[{"level": "h1", "text": "Test Heading"}],
        tags=["test", "article"],
        status=ContentStatus.APPROVED,
        created_at=datetime.utcnow()
    )
    
    # Override output directory for test
    publisher = Publisher()
    publisher.output_dir = tmp_path
    
    # Publish article
    output_file = publisher.publish_article(
        article,
        site_name="Test Site",
        base_url="https://test.com"
    )
    
    # Verify file was created
    assert output_file.exists()
    assert output_file.suffix == '.html'
    
    # Verify content
    content = output_file.read_text()
    assert article.title in content
    assert article.meta_description in content
    assert article.keyword in content


def test_publish_index(tmp_path):
    """Test publishing index page with multiple articles."""
    articles = [
        Article(
            slug=f"article-{i}",
            keyword=f"keyword{i}",
            title=f"Article {i}",
            meta_description=f"Description {i}",
            body_html=f"<p>Content {i}</p>",
            body_plain=f"Content {i}",
            word_count=100,
            tags=[f"tag{i}"],
            status=ContentStatus.PUBLISHED,
            created_at=datetime.utcnow()
        )
        for i in range(3)
    ]
    
    publisher = Publisher()
    publisher.output_dir = tmp_path
    
    # Publish index
    index_file = publisher.publish_index(
        articles,
        site_name="Test Site",
        base_url="https://test.com",
        title="Test Index"
    )
    
    # Verify file was created
    assert index_file.exists()
    assert index_file.name == 'index.html'
    
    # Verify content includes all articles
    content = index_file.read_text()
    for article in articles:
        assert article.title in content
        assert article.slug in content


def test_clean_output_directory(tmp_path):
    """Test cleaning output directory."""
    publisher = Publisher()
    publisher.output_dir = tmp_path
    
    # Create some test files
    test_file = tmp_path / 'test.html'
    test_file.write_text('test')
    
    # Clean directory
    publisher.clean_output_directory()
    
    # Verify directory is clean but exists
    assert publisher.output_dir.exists()
    assert not test_file.exists()


def test_get_published_count(tmp_path):
    """Test counting published files."""
    publisher = Publisher()
    publisher.output_dir = tmp_path
    
    # Initially should be 0
    assert publisher.get_published_count() == 0
    
    # Create articles directory and files
    articles_dir = tmp_path / 'articles'
    articles_dir.mkdir()
    
    for i in range(3):
        (articles_dir / f'article-{i}.html').write_text(f'content {i}')
    
    # Should count files
    assert publisher.get_published_count() == 3
