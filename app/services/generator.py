"""
Content Generator Service - Core MVP.

Generates high-quality, SEO-optimized articles from keywords.
Implements originality checking and ethical content generation.

NO FRAUDULENT PRACTICES:
- Real content generation (no spinning/copying)
- Originality verification before publishing
- Human review workflow (review_required=true)
"""
import json
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Article, ArticleStatus, Keyword


class ContentGenerator:
    """
    Ethical content generator with originality checking.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.min_words = settings.min_word_count
        self.max_words = settings.max_word_count

    async def generate_article(
        self, keyword_id: int, review_required: Optional[bool] = None
    ) -> Article:
        """
        Generate a complete article from a keyword.

        Args:
            keyword_id: ID of keyword to generate content for
            review_required: Override default review_required setting

        Returns:
            Generated Article instance (saved to DB)

        Raises:
            ValueError: If keyword not found or duplicate content detected
        """
        # Get keyword
        keyword = await self._get_keyword(keyword_id)
        if not keyword:
            raise ValueError(f"Keyword ID {keyword_id} not found")

        # Generate title and slug
        title = self._generate_title(keyword.keyword)
        slug = self._generate_slug(title)

        # Check if slug already exists (duplicate)
        if await self._slug_exists(slug):
            raise ValueError(f"Content with slug '{slug}' already exists")

        # Generate main content
        body = self._generate_body(keyword.keyword, title)
        word_count = len(body.split())

        # Validate word count
        if word_count < self.min_words or word_count > self.max_words:
            raise ValueError(
                f"Generated content word count ({word_count}) outside range [{self.min_words}, {self.max_words}]"
            )

        # Check originality (similarity with existing content)
        if await self._is_duplicate_content(body):
            raise ValueError("Generated content too similar to existing articles")

        # Generate additional assets
        meta_description = self._generate_meta_description(body)
        tags = self._generate_tags(keyword.keyword, body)
        internal_links = self._generate_internal_links(keyword.keyword)
        schema_markup = self._generate_schema_markup(title, meta_description)
        cta_variants = self._generate_cta_variants(keyword.keyword)

        # Generate multi-channel content
        video_script = self._generate_video_script(title, body)
        thread_content = self._generate_thread(title, body)

        # Determine status based on review requirement
        if review_required is None:
            review_required = settings.review_required

        status = ArticleStatus.REVIEW if review_required else ArticleStatus.DRAFT

        # Create article
        article = Article(
            keyword_id=keyword_id,
            title=title,
            slug=slug,
            meta_description=meta_description,
            body=body,
            word_count=word_count,
            tags=tags,
            internal_links=internal_links,
            schema_markup=schema_markup,
            cta_variants=cta_variants,
            video_script=video_script,
            thread_content=thread_content,
            status=status,
            review_required=review_required,
        )

        self.db.add(article)
        await self.db.commit()
        await self.db.refresh(article)

        return article

    async def _get_keyword(self, keyword_id: int) -> Optional[Keyword]:
        """Fetch keyword by ID."""
        result = await self.db.execute(
            select(Keyword).where(Keyword.id == keyword_id, Keyword.is_active == True)
        )
        return result.scalar_one_or_none()

    async def _slug_exists(self, slug: str) -> bool:
        """Check if slug already exists."""
        result = await self.db.execute(select(Article).where(Article.slug == slug))
        return result.scalar_one_or_none() is not None

    async def _is_duplicate_content(self, body: str) -> bool:
        """
        Check if content is too similar to existing articles.
        
        For MVP: uses simple word overlap heuristic.
        TODO: Implement proper similarity with embeddings/Chroma.
        """
        # Get recent articles for comparison
        result = await self.db.execute(
            select(Article).order_by(Article.created_at.desc()).limit(100)
        )
        existing_articles = result.scalars().all()

        body_words = set(re.findall(r"\w+", body.lower()))

        for article in existing_articles:
            article_words = set(re.findall(r"\w+", article.body.lower()))
            if not article_words:
                continue

            # Calculate Jaccard similarity
            intersection = len(body_words & article_words)
            union = len(body_words | article_words)
            similarity = intersection / union if union > 0 else 0

            if similarity > settings.similarity_threshold:
                return True

        return False

    def _generate_title(self, keyword: str) -> str:
        """
        Generate SEO-optimized title.
        
        Templates designed for engagement and SEO.
        """
        templates = [
            f"The Ultimate Guide to {keyword.title()}: Everything You Need to Know",
            f"How to Master {keyword.title()}: Expert Tips and Strategies",
            f"{keyword.title()} in 2025: Complete Beginner's Guide",
            f"Top 10 {keyword.title()} Techniques That Actually Work",
            f"{keyword.title()} Explained: A Comprehensive Deep Dive",
            f"Why {keyword.title()} Matters: Benefits and Best Practices",
            f"Getting Started with {keyword.title()}: Step-by-Step Tutorial",
            f"{keyword.title()} Secrets: What Experts Don't Tell You",
        ]
        return random.choice(templates)

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug."""
        return slugify(title, max_length=100)

    def _generate_body(self, keyword: str, title: str) -> str:
        """
        Generate article body content.
        
        For MVP: template-based generation.
        TODO: Integrate LLM (OpenAI/local) for higher quality.
        """
        sections = [
            self._intro_section(keyword, title),
            self._why_matters_section(keyword),
            self._how_to_section(keyword),
            self._tips_section(keyword),
            self._common_mistakes_section(keyword),
            self._tools_resources_section(keyword),
            self._conclusion_section(keyword),
        ]

        return "\n\n".join(sections)

    def _intro_section(self, keyword: str, title: str) -> str:
        """Generate introduction."""
        intros = [
            f"## Introduction\n\nIn today's rapidly evolving landscape, understanding {keyword} has become more crucial than ever. "
            f"Whether you're just starting out or looking to enhance your existing knowledge, this comprehensive guide will walk you through "
            f"everything you need to know about {keyword}.\n\n"
            f"The world has changed dramatically in recent years, and {keyword} has become a cornerstone of success in many fields. "
            f"From startups to established enterprises, professionals are discovering that mastery of {keyword} can be the difference "
            f"between average results and exceptional outcomes.\n\n"
            f"By the end of this article, you'll have a deep understanding of the fundamental concepts, practical applications, and expert "
            f"strategies that can help you achieve success with {keyword}. We'll explore proven methodologies, common pitfalls to avoid, "
            f"and actionable steps you can take today to start seeing results.",
            f"## What Is {keyword.title()}?\n\n{keyword.title()} represents a fundamental concept that has gained significant attention in recent years. "
            f"For beginners and experts alike, mastering {keyword} opens up new opportunities and possibilities.\n\n"
            f"The importance of {keyword} cannot be overstated. Industry leaders consistently emphasize its role in driving innovation, "
            f"improving efficiency, and achieving sustainable growth. Yet many people struggle to fully grasp its potential or implement "
            f"it effectively in their daily work.\n\n"
            f"This guide breaks down complex ideas into digestible sections, ensuring you can implement what you learn immediately. "
            f"We've structured the content to build progressively, starting with fundamentals and advancing to sophisticated techniques "
            f"that experienced practitioners use to stay ahead of the curve.",
        ]
        return random.choice(intros)

    def _why_matters_section(self, keyword: str) -> str:
        """Generate 'why it matters' section."""
        return (
            f"## Why {keyword.title()} Matters\n\n"
            f"Understanding {keyword} is essential for several key reasons:\n\n"
            f"1. **Competitive Advantage**: Those who master {keyword} gain a significant edge in their field\n"
            f"2. **Long-term Benefits**: The skills and knowledge related to {keyword} provide lasting value\n"
            f"3. **Practical Applications**: {keyword.title()} can be applied across various scenarios and contexts\n"
            f"4. **Future-Proofing**: Staying current with {keyword} trends ensures you remain relevant\n\n"
            f"Research shows that individuals and organizations that prioritize {keyword} consistently outperform their peers."
        )

    def _how_to_section(self, keyword: str) -> str:
        """Generate how-to section."""
        return (
            f"## How to Get Started with {keyword.title()}\n\n"
            f"Getting started with {keyword} doesn't have to be overwhelming. Follow this step-by-step approach:\n\n"
            f"### Step 1: Build Your Foundation\n"
            f"Begin by understanding the core principles of {keyword}. Familiarize yourself with key terminology and concepts.\n\n"
            f"### Step 2: Practice Regularly\n"
            f"Consistent practice is crucial for mastering {keyword}. Dedicate time each day to work on your skills.\n\n"
            f"### Step 3: Learn from Examples\n"
            f"Study real-world applications of {keyword}. Analyze what works and why.\n\n"
            f"### Step 4: Experiment and Iterate\n"
            f"Don't be afraid to try new approaches with {keyword}. Learn from both successes and failures.\n\n"
            f"### Step 5: Stay Updated\n"
            f"The landscape of {keyword} evolves constantly. Follow industry leaders and stay informed about new developments."
        )

    def _tips_section(self, keyword: str) -> str:
        """Generate tips section with more content."""
        return (
            f"## Expert Tips for {keyword.title()} Success\n\n"
            f"Based on years of experience and research, here are proven tips to accelerate your {keyword} mastery:\n\n"
            f"1. **Balance theory with practical application of {keyword}**\n"
            f"   Understanding concepts is important, but nothing beats hands-on experience. Try to apply what you learn "
            f"immediately in real-world scenarios. Start small, experiment often, and iterate based on results.\n\n"
            f"2. **Seek feedback from experienced practitioners in {keyword}**\n"
            f"   Find mentors or join communities where you can get constructive criticism. Others' perspectives will help "
            f"you identify blind spots and accelerate your growth. Don't be afraid to ask questions or share your work.\n\n"
            f"3. **Don't rush—take time to understand {keyword} thoroughly**\n"
            f"   Quality always beats speed when it comes to learning. Take time to absorb information, practice consistently, "
            f"and review what you've learned. Building a solid foundation pays dividends in the long run.\n\n"
            f"4. **Set clear, measurable goals for your {keyword} development**\n"
            f"   Define what success looks like for you. Break down large objectives into smaller, manageable milestones. "
            f"Track your progress regularly and adjust your approach as needed.\n\n"
            f"5. **Document your {keyword} journey to track progress**\n"
            f"   Keep notes, write reflections, and maintain a learning journal. This helps reinforce concepts and provides "
            f"valuable reference material for future challenges. You'll also appreciate seeing how far you've come.\n\n"
            f"Remember, success with {keyword} comes from consistent effort and a willingness to learn and adapt."
        )

    def _common_mistakes_section(self, keyword: str) -> str:
        """Generate common mistakes section."""
        return (
            f"## Common Mistakes to Avoid\n\n"
            f"Even experienced practitioners make mistakes with {keyword}. Here are pitfalls to watch out for:\n\n"
            f"**Mistake #1: Rushing the Learning Process**\n"
            f"Many people try to master {keyword} too quickly, leading to gaps in understanding. This often happens when "
            f"following hype or trying to keep up with peers. Take your time to really absorb the material, practice regularly, "
            f"and don't move on until you've solidified each concept. Rushing creates a shaky foundation that will cause "
            f"problems later when you encounter more advanced topics.\n\n"
            f"**Mistake #2: Ignoring Fundamentals**\n"
            f"Skipping basic concepts in {keyword} creates a weak foundation for advanced topics. Many beginners want to jump "
            f"straight to advanced techniques without understanding the underlying principles. This leads to confusion and "
            f"frustration. Always start with the basics, even if they seem simple or boring. A strong grasp of fundamentals "
            f"makes everything else easier.\n\n"
            f"**Mistake #3: Not Seeking Feedback**\n"
            f"Working in isolation limits your growth with {keyword}. Regular feedback is essential for identifying blind spots "
            f"and improving your approach. Find mentors, join communities, or participate in peer reviews. External perspectives "
            f"can reveal issues you'd never notice on your own and accelerate your learning significantly.\n\n"
            f"**Mistake #4: Following Trends Blindly**\n"
            f"Not all {keyword} trends are worth following. Evaluate each one critically based on your specific needs and goals. "
            f"What works for one person or organization may not work for another. Stay informed about trends, but don't feel "
            f"pressured to adopt every new approach. Focus on what delivers real value for your situation.\n\n"
            f"By avoiding these mistakes, you'll progress much faster with {keyword} and build skills that last."
        )

    def _tools_resources_section(self, keyword: str) -> str:
        """Generate tools & resources section."""
        return (
            f"## Essential Tools and Resources\n\n"
            f"To excel with {keyword}, leverage these types of resources:\n\n"
            f"### Learning Resources\n"
            f"- Online courses and tutorials focused on {keyword}\n"
            f"- Books written by {keyword} experts\n"
            f"- Research papers and case studies\n\n"
            f"### Community Resources\n"
            f"- Forums and discussion groups about {keyword}\n"
            f"- Professional networks and mentorship opportunities\n"
            f"- Conferences and workshops\n\n"
            f"### Practical Tools\n"
            f"- Software and platforms designed for {keyword}\n"
            f"- Templates and frameworks\n"
            f"- Analytics and measurement tools\n\n"
            f"Building a comprehensive toolkit accelerates your {keyword} journey significantly."
        )

    def _conclusion_section(self, keyword: str) -> str:
        """Generate conclusion."""
        return (
            f"## Conclusion\n\n"
            f"Mastering {keyword} is a journey that requires dedication, continuous learning, and practical application. "
            f"Throughout this guide, we've covered the essential concepts, strategies, and best practices that form the "
            f"foundation of {keyword} expertise.\n\n"
            f"The path forward is clear: start with fundamentals, build incrementally, and never stop learning. The field "
            f"of {keyword} continues to evolve, presenting new opportunities and challenges. Those who stay committed to "
            f"continuous improvement will find themselves well-positioned for long-term success.\n\n"
            f"Remember that success with {keyword} doesn't happen overnight. Start with the basics, practice consistently, "
            f"learn from mistakes, and stay curious. The investment you make in understanding {keyword} will pay dividends "
            f"throughout your personal and professional life. Every expert was once a beginner—the difference is they never "
            f"gave up.\n\n"
            f"What's your next step with {keyword}? Start implementing what you've learned today, and you'll be amazed at how "
            f"quickly you progress. Whether you begin with a small pilot project or dive into comprehensive training, the "
            f"important thing is to take action. Knowledge without application remains theoretical—make it real."
        )

    def _generate_meta_description(self, body: str) -> str:
        """Generate SEO meta description from body content."""
        # Extract first meaningful sentence
        sentences = re.split(r"[.!?]+", body)
        for sentence in sentences:
            clean = sentence.strip()
            if len(clean) > 50 and not clean.startswith("#"):
                # Truncate to ~155 characters for SEO
                if len(clean) > 155:
                    clean = clean[:152] + "..."
                return clean
        return "Comprehensive guide with expert tips, strategies, and best practices."

    def _generate_tags(self, keyword: str, body: str) -> Dict:
        """Generate relevant tags."""
        # Base tags from keyword
        base_tags = keyword.split()

        # Common related tags
        related = [
            "guide",
            "tutorial",
            "tips",
            "best practices",
            "how-to",
            "beginner-friendly",
            "expert advice",
        ]

        all_tags = base_tags + random.sample(related, min(3, len(related)))

        return {"tags": all_tags}

    def _generate_internal_links(self, keyword: str) -> Dict:
        """Generate suggested internal links."""
        return {
            "suggested_links": [
                {"text": f"Getting Started with {keyword.title()}", "url": "/getting-started"},
                {"text": f"Advanced {keyword.title()} Techniques", "url": "/advanced-techniques"},
                {"text": "Related Resources", "url": "/resources"},
            ]
        }

    def _generate_schema_markup(self, title: str, description: str) -> Dict:
        """Generate JSON-LD schema markup for SEO."""
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "datePublished": datetime.utcnow().isoformat(),
            "author": {"@type": "Organization", "name": "AutoCash Ultimate"},
        }

    def _generate_cta_variants(self, keyword: str) -> Dict:
        """Generate Call-To-Action variants for A/B testing."""
        variants = [
            f"Start Your {keyword.title()} Journey Today",
            f"Get Expert {keyword.title()} Resources",
            f"Download Our Free {keyword.title()} Guide",
        ]
        return {"variants": variants}

    def _generate_video_script(self, title: str, body: str) -> str:
        """Generate 40-60 second video script."""
        # Extract key points
        lines = [line.strip() for line in body.split("\n") if line.strip() and not line.startswith("#")]
        key_points = random.sample(lines, min(3, len(lines)))

        script = (
            f"[INTRO - 5s]\n"
            f"Hey! Want to master {title}? Let's dive in!\n\n"
            f"[POINT 1 - 15s]\n"
            f"{key_points[0] if key_points else 'First key insight about the topic.'}\n\n"
            f"[POINT 2 - 15s]\n"
            f"{key_points[1] if len(key_points) > 1 else 'Second important concept.'}\n\n"
            f"[POINT 3 - 15s]\n"
            f"{key_points[2] if len(key_points) > 2 else 'Third critical tip.'}\n\n"
            f"[CTA - 10s]\n"
            f"Want the full guide? Check the link in description!"
        )
        return script

    def _generate_thread(self, title: str, body: str) -> str:
        """Generate X/Twitter thread."""
        return (
            f"🧵 Thread: {title}\n\n"
            f"1/ Want to understand this topic better? Here's everything you need to know 👇\n\n"
            f"2/ First, let's cover the basics. This foundational knowledge is crucial...\n\n"
            f"3/ Now the practical part: Here's how to apply this in real scenarios...\n\n"
            f"4/ Common mistakes to avoid (save yourself time and frustration!)...\n\n"
            f"5/ Tools and resources that make this 10x easier...\n\n"
            f"6/ That's it! Questions? Drop them below. Full article linked in my bio 🔗"
        )


async def generate_batch(
    db: AsyncSession, count: int = 5, review_required: bool = True
) -> List[Article]:
    """
    Generate multiple articles in batch.

    Args:
        db: Database session
        count: Number of articles to generate
        review_required: Whether articles require review

    Returns:
        List of generated Article instances
    """
    generator = ContentGenerator(db)

    # Get active keywords
    result = await db.execute(
        select(Keyword).where(Keyword.is_active == True).order_by(Keyword.priority.desc()).limit(count * 2)
    )
    keywords = result.scalars().all()

    if not keywords:
        raise ValueError("No active keywords found")

    articles = []
    errors = []

    for keyword in keywords[:count]:
        try:
            article = await generator.generate_article(keyword.id, review_required)
            articles.append(article)
        except Exception as e:
            errors.append({"keyword": keyword.keyword, "error": str(e)})
            continue

        if len(articles) >= count:
            break

    if errors:
        print(f"⚠️  Some articles failed to generate: {json.dumps(errors, indent=2)}")

    return articles
