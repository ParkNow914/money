"""
Repurposer service for transforming articles into different content formats.

Converts articles into:
- Twitter/X threads
- Video scripts
- Email newsletters
- PDF documents
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

from app.models import Article, RepurposedContent


class ContentRepurposer:
    """
    Repurpose article content into various formats.
    
    Each format is optimized for its specific platform or medium.
    """
    
    def repurpose_to_thread(self, article: Article, max_tweets: int = 10) -> Dict:
        """
        Convert article into a Twitter/X thread.
        
        Args:
            article: Source article
            max_tweets: Maximum number of tweets in thread
            
        Returns:
            Dictionary containing thread data
        """
        # Extract key points from headings
        headings = article.headings or []
        
        # First tweet: hook + intro
        tweets = [
            {
                "number": 1,
                "text": f"🧵 {article.title[:200]}\n\nLet's dive in 👇",
                "type": "intro"
            }
        ]
        
        # Convert H2 headings into thread tweets
        tweet_num = 2
        for heading in headings:
            if heading.get('level') == 'h2' and tweet_num <= max_tweets - 1:
                heading_text = heading.get('text', '')
                tweet_text = f"{tweet_num - 1}/ {heading_text}\n\n"
                
                # Add a snippet about this section (simplified version)
                tweet_text += f"Key insight: Understanding {heading_text.lower()} is crucial for {article.keyword}."
                
                tweets.append({
                    "number": tweet_num,
                    "text": tweet_text[:280],  # Twitter character limit
                    "type": "content"
                })
                tweet_num += 1
        
        # Final tweet: CTA
        tweets.append({
            "number": tweet_num,
            "text": f"Want to learn more about {article.keyword}?\n\nRead the full article: [LINK]\n\n♻️ Retweet if you found this helpful!",
            "type": "cta"
        })
        
        return {
            "format": "thread",
            "platform": "twitter",
            "tweet_count": len(tweets),
            "tweets": tweets,
            "metadata": {
                "article_slug": article.slug,
                "keyword": article.keyword,
                "created_at": datetime.utcnow().isoformat()
            }
        }
    
    def repurpose_to_video_script(self, article: Article, duration_minutes: int = 5) -> Dict:
        """
        Convert article into a video script.
        
        Args:
            article: Source article
            duration_minutes: Target video duration in minutes
            
        Returns:
            Dictionary containing video script data
        """
        headings = article.headings or []
        
        # Video script structure
        script = {
            "format": "video_script",
            "duration_minutes": duration_minutes,
            "sections": []
        }
        
        # Intro (0:00 - 0:30)
        script["sections"].append({
            "timestamp": "0:00",
            "duration": "0:30",
            "type": "intro",
            "text": f"Hey everyone! Today we're diving into {article.keyword}. "
                   f"I'm going to share {len([h for h in headings if h.get('level') == 'h2'])} key insights "
                   f"that will help you master this topic. Let's get started!",
            "visuals": "Title card with topic",
            "b_roll": "Engaging intro footage"
        })
        
        # Main content sections (from H2 headings)
        time_per_section = (duration_minutes - 1) * 60 / max(len([h for h in headings if h.get('level') == 'h2']), 1)
        current_time = 30  # Start after intro
        
        for i, heading in enumerate([h for h in headings if h.get('level') == 'h2']):
            heading_text = heading.get('text', '')
            
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            
            script["sections"].append({
                "timestamp": f"{minutes}:{seconds:02d}",
                "duration": f"{int(time_per_section)}s",
                "type": "content",
                "heading": heading_text,
                "text": f"Point number {i + 1}: {heading_text}. "
                       f"This is important because it helps you understand {article.keyword} better. "
                       f"Here's what you need to know...",
                "visuals": f"Screen capture or graphic for {heading_text}",
                "b_roll": "Relevant footage"
            })
            
            current_time += time_per_section
        
        # Outro (last 30 seconds)
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        script["sections"].append({
            "timestamp": f"{minutes}:{seconds:02d}",
            "duration": "0:30",
            "type": "outro",
            "text": f"That's it for today's video on {article.keyword}! "
                   f"If you found this helpful, don't forget to like and subscribe. "
                   f"Check the description for more resources. See you in the next one!",
            "visuals": "End screen with subscribe button",
            "b_roll": "Outro footage"
        })
        
        script["metadata"] = {
            "article_slug": article.slug,
            "keyword": article.keyword,
            "total_sections": len(script["sections"]),
            "created_at": datetime.utcnow().isoformat()
        }
        
        return script
    
    def repurpose_to_email(self, article: Article, email_type: str = "newsletter") -> Dict:
        """
        Convert article into an email format.
        
        Args:
            article: Source article
            email_type: Type of email (newsletter, digest, etc.)
            
        Returns:
            Dictionary containing email data
        """
        headings = article.headings or []
        
        # Extract key points (H2 headings)
        key_points = [h.get('text', '') for h in headings if h.get('level') == 'h2'][:5]
        
        email = {
            "format": "email",
            "type": email_type,
            "subject": f"📧 {article.title[:60]}...",
            "preview_text": article.meta_description[:100],
            "sections": {
                "greeting": "Hi there!",
                "intro": f"Today I want to share some insights about {article.keyword}. "
                        f"This is crucial if you want to succeed in this area.",
                "key_points": [
                    f"✓ {point}" for point in key_points
                ],
                "cta": {
                    "text": "Read the full article →",
                    "url": f"/articles/{article.slug}"
                },
                "footer": "Thanks for reading!\n\nP.S. Reply to this email if you have questions!"
            },
            "metadata": {
                "article_slug": article.slug,
                "keyword": article.keyword,
                "created_at": datetime.utcnow().isoformat()
            }
        }
        
        return email
    
    def repurpose_to_pdf_outline(self, article: Article) -> Dict:
        """
        Create a PDF outline/structure from article.
        
        Args:
            article: Source article
            
        Returns:
            Dictionary containing PDF structure (actual PDF generation would use reportlab/weasyprint)
        """
        headings = article.headings or []
        
        pdf_outline = {
            "format": "pdf",
            "title": article.title,
            "metadata": {
                "author": "AutoCash Ultimate",
                "subject": article.keyword,
                "keywords": article.tags or [],
                "created": datetime.utcnow().isoformat()
            },
            "pages": [
                {
                    "number": 1,
                    "type": "cover",
                    "content": {
                        "title": article.title,
                        "subtitle": f"A complete guide to {article.keyword}",
                        "date": datetime.utcnow().strftime("%B %Y")
                    }
                },
                {
                    "number": 2,
                    "type": "toc",
                    "content": {
                        "title": "Table of Contents",
                        "sections": [
                            {"title": h.get('text', ''), "page": i + 3}
                            for i, h in enumerate([h for h in headings if h.get('level') == 'h2'])
                        ]
                    }
                }
            ],
            "content_pages": [
                {
                    "heading": h.get('text', ''),
                    "level": h.get('level', 'h2'),
                    "content": f"Content for {h.get('text', '')} section..."
                }
                for h in headings
            ]
        }
        
        pdf_outline["metadata"]["total_pages"] = len(pdf_outline["pages"]) + len(pdf_outline["content_pages"])
        pdf_outline["metadata"]["article_slug"] = article.slug
        
        return pdf_outline
    
    def create_repurposed_content(
        self,
        article: Article,
        content_type: str,
        **kwargs
    ) -> Dict:
        """
        Create repurposed content of specified type.
        
        Args:
            article: Source article
            content_type: Type of content (thread, video_script, email, pdf)
            **kwargs: Additional arguments for specific repurposer
            
        Returns:
            Repurposed content data
        """
        repurposers = {
            'thread': self.repurpose_to_thread,
            'video_script': self.repurpose_to_video_script,
            'email': self.repurpose_to_email,
            'pdf': self.repurpose_to_pdf_outline
        }
        
        if content_type not in repurposers:
            raise ValueError(f"Unknown content type: {content_type}. "
                           f"Supported types: {list(repurposers.keys())}")
        
        return repurposers[content_type](article, **kwargs)


# Singleton instance
repurposer = ContentRepurposer()
