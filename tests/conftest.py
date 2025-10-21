"""
Pytest configuration and fixtures.
"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal, Base, engine
from app.models import Article, Keyword


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test.
    Rolls back changes after test completes.
    """
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

    # Clean up tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def sample_keyword(db_session: AsyncSession) -> Keyword:
    """Create a sample keyword for testing."""
    keyword = Keyword(
        keyword="passive income",
        priority=8,
        category="finance",
        search_volume=10000,
        competition=0.65,
        cpc_estimate=2.50,
        is_active=True,
    )
    db_session.add(keyword)
    await db_session.commit()
    await db_session.refresh(keyword)
    return keyword


@pytest.fixture
async def multiple_keywords(db_session: AsyncSession) -> list[Keyword]:
    """Create multiple keywords for batch testing."""
    keywords = [
        Keyword(keyword="affiliate marketing", priority=9, is_active=True),
        Keyword(keyword="blogging tips", priority=7, is_active=True),
        Keyword(keyword="online business", priority=8, is_active=True),
    ]

    for kw in keywords:
        db_session.add(kw)

    await db_session.commit()

    for kw in keywords:
        await db_session.refresh(kw)

    return keywords


@pytest.fixture
async def sample_article(db_session: AsyncSession, sample_keyword: Keyword) -> Article:
    """Create a sample article for testing."""
    article = Article(
        keyword_id=sample_keyword.id,
        title="Test Article About Passive Income",
        slug="test-article-about-passive-income",
        meta_description="A test article about passive income strategies.",
        body="This is a test article body with sufficient content for testing purposes. " * 50,
        word_count=500,
        tags={"tags": ["passive income", "finance"]},
        status="draft",
        review_required=True,
    )
    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    return article
