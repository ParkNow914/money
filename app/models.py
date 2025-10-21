"""
Database models for AutoCash Ultimate.

All models follow:
- LGPD compliance (data minimization, consent tracking)
- Privacy by design
- Audit trail where needed
"""
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ArticleStatus(str, PyEnum):
    """Article lifecycle status."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ConsentType(str, PyEnum):
    """Types of user consent."""

    ANALYTICS = "analytics"
    MARKETING = "marketing"
    NECESSARY = "necessary"


class ConsentStatus(str, PyEnum):
    """Consent status."""

    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"


class Keyword(Base):
    """Keywords for content generation."""

    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    keyword: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    search_volume: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    competition: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cpc_estimate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1-10
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    articles: Mapped[list["Article"]] = relationship(
        "Article", back_populates="keyword", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Keyword(id={self.id}, keyword='{self.keyword}')>"


class Article(Base):
    """Generated articles/content."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    keyword_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("keywords.id", ondelete="CASCADE"), index=True
    )

    # Content
    title: Mapped[str] = mapped_column(String(500))
    slug: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    meta_description: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    word_count: Mapped[int] = mapped_column(Integer)

    # SEO & Structure
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # List of tags
    internal_links: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # Suggested links
    schema_markup: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # JSON-LD

    # Multi-channel assets
    video_script: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    thread_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pdf_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # CTAs & Monetization
    cta_variants: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # List of CTA options

    # Embedding for similarity/personalization
    embedding_vector: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # Store as JSON for SQLite
    embedding_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Status & Review
    status: Mapped[ArticleStatus] = mapped_column(
        Enum(ArticleStatus), default=ArticleStatus.DRAFT, index=True
    )
    review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Analytics
    views: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    keyword: Mapped["Keyword"] = relationship("Keyword", back_populates="articles")
    tracking_events: Mapped[list["TrackingEvent"]] = relationship(
        "TrackingEvent", back_populates="article", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_article_status_created", "status", "created_at"),)

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title[:50]}...', status={self.status})>"


class TrackingEvent(Base):
    """
    Privacy-compliant tracking events.
    Stores hashed identifiers only, no raw IPs.
    """

    __tablename__ = "tracking_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("articles.id", ondelete="CASCADE"), index=True
    )

    # Privacy-preserving identifiers (hashed with salt)
    visitor_hash: Mapped[str] = mapped_column(
        String(64), index=True
    )  # Hashed IP + salt
    ua_hash: Mapped[str] = mapped_column(String(64))  # Hashed user agent

    # Event data
    event_type: Mapped[str] = mapped_column(
        String(50), index=True
    )  # view, click, conversion
    affiliate_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Revenue (if applicable)
    revenue_amount: Mapped[float] = mapped_column(Float, default=0.0)

    # Consent check
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    # Relationships
    article: Mapped["Article"] = relationship(
        "Article", back_populates="tracking_events"
    )

    __table_args__ = (
        Index("idx_tracking_visitor_event", "visitor_hash", "event_type", "created_at"),
        Index("idx_tracking_article_created", "article_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<TrackingEvent(id={self.id}, type={self.event_type}, article_id={self.article_id})>"


class UserConsent(Base):
    """
    LGPD-compliant consent tracking.
    Records user consent for different data processing purposes.
    """

    __tablename__ = "user_consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Privacy-preserving identifier
    user_hash: Mapped[str] = mapped_column(String(64), index=True)

    # Email (only if explicitly provided and consented)
    email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, index=True
    )

    # Consent details
    consent_type: Mapped[ConsentType] = mapped_column(Enum(ConsentType), index=True)
    consent_status: Mapped[ConsentStatus] = mapped_column(
        Enum(ConsentStatus), default=ConsentStatus.GRANTED, index=True
    )

    # Audit trail
    consent_text: Mapped[str] = mapped_column(Text)  # What user agreed to
    ip_hash: Mapped[str] = mapped_column(String(64))  # Hashed IP for audit
    user_agent: Mapped[str] = mapped_column(String(500))

    # Timestamps
    granted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_consent_user_type", "user_hash", "consent_type"),
        UniqueConstraint("user_hash", "consent_type", name="uq_user_consent_type"),
    )

    def __repr__(self) -> str:
        return f"<UserConsent(id={self.id}, type={self.consent_type}, status={self.consent_status})>"


class DataExportRequest(Base):
    """
    LGPD DSAR (Data Subject Access Request) tracking.
    Records requests for data export, deletion, etc.
    """

    __tablename__ = "data_export_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Requester identification
    email: Mapped[str] = mapped_column(String(255), index=True)
    user_hash: Mapped[str] = mapped_column(String(64), index=True)

    # Request details
    request_type: Mapped[str] = mapped_column(
        String(50), index=True
    )  # export, delete, update
    status: Mapped[str] = mapped_column(
        String(50), default="pending", index=True
    )  # pending, processing, completed, failed

    # Verification
    verification_token: Mapped[str] = mapped_column(String(255), unique=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Processing
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    export_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Temporary URL for download

    # Audit
    ip_hash: Mapped[str] = mapped_column(String(64))
    user_agent: Mapped[str] = mapped_column(String(500))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime
    )  # Export links expire after 7 days

    __table_args__ = (Index("idx_export_email_status", "email", "status"),)

    def __repr__(self) -> str:
        return f"<DataExportRequest(id={self.id}, type={self.request_type}, status={self.status})>"


class KillSwitch(Base):
    """
    Kill-switch state tracking.
    Used to pause/resume automated operations.
    """

    __tablename__ = "kill_switches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Switch details
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    # Reason and context
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    triggered_by: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # user, system, monitor

    # Timestamps
    activated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deactivated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<KillSwitch(name='{self.name}', active={self.is_active})>"
