"""
Publisher service for generating static HTML files from articles.

Creates SEO-optimized static HTML pages that can be deployed to CDN or static hosting.
"""

import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings
from app.models import Article


class Publisher:
    """
    Static site publisher service.
    
    Converts articles into static HTML files with SEO optimization.
    """
    
    def __init__(self):
        """Initialize publisher with Jinja2 templates."""
        self.templates_dir = settings.TEMPLATES_DIR
        self.output_dir = settings.SITE_OUT_DIR
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml', 'j2'])
        )
    
    def publish_article(
        self,
        article: Article,
        site_name: str = "AutoCash Ultimate",
        base_url: str = "https://example.com"
    ) -> Path:
        """
        Publish an article as a static HTML file.
        
        Args:
            article: Article object to publish
            site_name: Name of the site for metadata
            base_url: Base URL for canonical links
            
        Returns:
            Path to the generated HTML file
        """
        # Load template
        template = self.env.get_template('article.j2')
        
        # Build canonical URL
        canonical_url = f"{base_url}/articles/{article.slug}"
        
        # Prepare template context
        context = {
            'title': article.title,
            'meta_description': article.meta_description,
            'body_html': article.body_html,
            'tags': article.tags or [],
            'canonical_url': canonical_url,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat() if article.updated_at else None,
            'site_name': site_name,
            'slug': article.slug,
            'keyword': article.keyword
        }
        
        # Render HTML
        html_content = template.render(**context)
        
        # Create article directory
        article_dir = self.output_dir / 'articles'
        article_dir.mkdir(parents=True, exist_ok=True)
        
        # Write HTML file
        output_file = article_dir / f"{article.slug}.html"
        output_file.write_text(html_content, encoding='utf-8')
        
        return output_file
    
    def publish_index(
        self,
        articles: List[Article],
        site_name: str = "AutoCash Ultimate",
        base_url: str = "https://example.com",
        title: str = "Latest Articles"
    ) -> Path:
        """
        Publish an index page with list of articles.
        
        Args:
            articles: List of Article objects to include
            site_name: Name of the site
            base_url: Base URL for links
            title: Title for the index page
            
        Returns:
            Path to the generated index HTML file
        """
        # Create a simple index template if it doesn't exist
        index_template_path = self.templates_dir / 'index.j2'
        if not index_template_path.exists():
            # Create basic index template
            index_template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - {{ site_name }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="articles">
        {% for article in articles %}
        <article class="article-preview">
            <h2><a href="/articles/{{ article.slug }}.html">{{ article.title }}</a></h2>
            <p>{{ article.meta_description }}</p>
            <p class="meta">Published: {{ article.created_at }}</p>
            <div class="tags">
                {% for tag in article.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
        </article>
        {% endfor %}
    </div>
</body>
</html>"""
            index_template_path.write_text(index_template_content, encoding='utf-8')
        
        # Load template
        template = self.env.get_template('index.j2')
        
        # Prepare context
        context = {
            'title': title,
            'site_name': site_name,
            'base_url': base_url,
            'articles': [
                {
                    'title': a.title,
                    'slug': a.slug,
                    'meta_description': a.meta_description,
                    'created_at': a.created_at.isoformat(),
                    'tags': a.tags or []
                }
                for a in articles
            ]
        }
        
        # Render HTML
        html_content = template.render(**context)
        
        # Write index file
        output_file = self.output_dir / 'index.html'
        output_file.write_text(html_content, encoding='utf-8')
        
        return output_file
    
    def clean_output_directory(self) -> None:
        """Clean the output directory (remove all generated files)."""
        import shutil
        
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_published_count(self) -> int:
        """Get count of published HTML files."""
        article_dir = self.output_dir / 'articles'
        if not article_dir.exists():
            return 0
        
        return len(list(article_dir.glob('*.html')))


# Singleton instance
publisher = Publisher()
