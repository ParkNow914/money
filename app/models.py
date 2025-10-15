"""
Database models for autocash-ultimate.

Privacy-first design with LGPD compliance:
- Minimal data collection
- Hashed identifiers
- Consent tracking
- Data retention controls
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Enum as SQLEnum, Float, 
    Integer, String, Text, JSON, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ContentStatus(str, Enum):
    """Status of generated content."""
    DRAFT = "draft"
    REVIEW_PENDING = "review_pending"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ConsentType(str, Enum):
    """Types of user consent."""
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    REQUIRED = "required"


class Article(Base):
    """Generated article content."""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    keyword = Column(String(255), index=True, nullable=False)
    title = Column(String(500), nullable=False)
    meta_description = Column(String(500))
    
    # Content
    body_html = Column(Text, nullable=False)
    body_plain = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False)
    
    # SEO & Structure
    headings = Column(JSON)  # H1, H2, H3 structure
    internal_links = Column(JSON)  # Suggested internal links
    tags = Column(JSON)  # Topic tags
    
    # Status
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT, nullable=False)
    review_required = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    repurposed_content = relationship("RepurposedContent", back_populates="article")
    tracking_events = relationship("TrackingEvent", back_populates="article")
    affiliate_links = relationship("AffiliateLink", back_populates="article")


class RepurposedContent(Base):
    """Content repurposed from articles (threads, videos, emails, PDFs)."""
    __tablename__ = "repurposed_content"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    
    content_type = Column(String(50), nullable=False)  # thread, video_script, email, pdf
    content_data = Column(JSON, nullable=False)  # Actual content
    
    storage_url = Column(String(500), nullable=True)  # URL in object storage if applicable
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    article = relationship("Article", back_populates="repurposed_content")


class UserConsent(Base):
    """Track user consent for LGPD compliance."""
    __tablename__ = "user_consents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Anonymized identifier (hashed email or cookie)
    user_hash = Column(String(64), index=True, nullable=False)
    
    # Consent details
    consent_type = Column(SQLEnum(ConsentType), nullable=False)
    granted = Column(Boolean, nullable=False)
    
    # Audit trail
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_hash = Column(String(64), nullable=True)  # Hashed IP for audit
    user_agent_hash = Column(String(64), nullable=True)
    
    # Data retention
    expires_at = Column(DateTime, nullable=True)


class TrackingEvent(Base):
    """Privacy-preserving tracking of clicks and conversions."""
    __tablename__ = "tracking_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event details
    event_type = Column(String(50), nullable=False)  # view, click, conversion
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    
    # Anonymized user data (LGPD compliant)
    session_hash = Column(String(64), index=True, nullable=False)  # Hashed session ID
    ip_hash = Column(String(64), nullable=True)  # Hashed IP (salted)
    ua_hash = Column(String(64), nullable=True)  # Hashed user agent
    
    # UTM parameters (for attribution)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    
    # Revenue tracking (when applicable)
    revenue = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    article = relationship("Article", back_populates="tracking_events")


class AffiliateLink(Base):
    """Affiliate link management for monetization."""
    __tablename__ = "affiliate_links"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link identification
    link_id = Column(String(100), unique=True, index=True, nullable=False)  # e.g., "amazon-product-123"
    name = Column(String(255), nullable=False)  # Descriptive name
    
    # Link details
    destination_url = Column(String(1000), nullable=False)  # Actual affiliate URL
    product_name = Column(String(255), nullable=True)
    product_category = Column(String(100), nullable=True)
    
    # Affiliate program
    affiliate_program = Column(String(100), nullable=False)  # amazon, clickbank, etc.
    commission_rate = Column(Float, nullable=True)  # Percentage or fixed amount
    commission_type = Column(String(20), nullable=True)  # percentage, fixed, cpa
    
    # Performance tracking
    clicks = Column(Integer, default=0, nullable=False)
    conversions = Column(Integer, default=0, nullable=False)
    revenue = Column(Float, default=0.0, nullable=False)
    
    # Article association (optional - link can be used across multiple articles)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_click_at = Column(DateTime, nullable=True)
    
    # Relationships
    article = relationship("Article", back_populates="affiliate_links")


class Keyword(Base):
    """Keywords for content generation."""
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), unique=True, index=True, nullable=False)
    
    # Metadata
    search_volume = Column(Integer, nullable=True)
    competition = Column(String(50), nullable=True)
    priority = Column(Integer, default=5, nullable=False)  # 1-10
    
    # Status
    used = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    used_at = Column(DateTime, nullable=True)


class AuditLog(Base):
    """Audit log for LGPD compliance (DSAR, consent changes, etc)."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    action = Column(String(100), nullable=False)  # data_export, data_deletion, consent_grant, etc
    user_hash = Column(String(64), index=True, nullable=False)
    
    details = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_hash = Column(String(64), nullable=True)
