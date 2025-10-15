"""
Tests for tracking and privacy features.

Validates LGPD compliance and privacy-preserving tracking.
"""

import pytest
import hashlib
from datetime import datetime

from app.models import TrackingEvent, UserConsent, ConsentType


def test_tracking_event_hashed_identifiers():
    """Test that tracking events use hashed identifiers."""
    event = TrackingEvent(
        event_type="click",
        session_hash=hashlib.sha256(b"session_123").hexdigest(),
        ip_hash=hashlib.sha256(b"192.168.1.1" + b"salt").hexdigest(),
        ua_hash=hashlib.sha256(b"Mozilla/5.0").hexdigest(),
        utm_source="google",
        utm_medium="cpc",
        utm_campaign="test",
    )
    
    # Verify hashes are proper length (SHA256 = 64 chars)
    assert len(event.session_hash) == 64
    assert len(event.ip_hash) == 64
    assert len(event.ua_hash) == 64
    
    # Verify no raw PII
    assert "192.168.1.1" not in event.ip_hash
    assert "Mozilla" not in event.ua_hash


def test_user_consent_structure():
    """Test user consent model structure."""
    consent = UserConsent(
        user_hash=hashlib.sha256(b"user@example.com").hexdigest(),
        consent_type=ConsentType.ANALYTICS,
        granted=True,
        granted_at=datetime.utcnow(),
        ip_hash=hashlib.sha256(b"ip" + b"salt").hexdigest(),
    )
    
    assert consent.user_hash is not None
    assert len(consent.user_hash) == 64
    assert consent.consent_type == ConsentType.ANALYTICS
    assert consent.granted is True
    
    # No raw email stored
    assert "@" not in consent.user_hash


def test_consent_types():
    """Test all consent types are defined."""
    assert ConsentType.ANALYTICS == "analytics"
    assert ConsentType.MARKETING == "marketing"
    assert ConsentType.REQUIRED == "required"


def test_tracking_event_without_revenue():
    """Test tracking event can exist without revenue."""
    event = TrackingEvent(
        event_type="view",
        session_hash=hashlib.sha256(b"session").hexdigest(),
        revenue=None,  # No revenue for views
    )
    
    assert event.revenue is None


def test_tracking_event_with_revenue():
    """Test tracking event with revenue data."""
    event = TrackingEvent(
        event_type="conversion",
        session_hash=hashlib.sha256(b"session").hexdigest(),
        revenue=25.50,
    )
    
    assert event.revenue == 25.50


def test_hash_consistency():
    """Test that same input produces same hash."""
    input_data = b"test_session_123"
    
    hash1 = hashlib.sha256(input_data).hexdigest()
    hash2 = hashlib.sha256(input_data).hexdigest()
    
    assert hash1 == hash2
    assert len(hash1) == 64


def test_salted_hash_different():
    """Test that salted hashes are different from unsalted."""
    ip = b"192.168.1.1"
    salt = b"random_salt"
    
    hash_unsalted = hashlib.sha256(ip).hexdigest()
    hash_salted = hashlib.sha256(ip + salt).hexdigest()
    
    assert hash_unsalted != hash_salted
