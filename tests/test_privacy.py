"""
Tests for privacy and DSAR endpoints.

Tests LGPD compliance features including data export, deletion, and consent management.
"""

import pytest
from datetime import datetime
from app.models import UserConsent, TrackingEvent, AuditLog, ConsentType
from app.db import get_db
import hashlib


@pytest.mark.asyncio
async def test_consent_grant(test_db):
    """Test granting user consent."""
    from app.routes.privacy import manage_consent, ConsentRequest
    
    db = test_db
    
    request = ConsentRequest(
        email="user@example.com",
        consent_type="analytics",
        granted=True
    )
    
    response = await manage_consent(request, db)
    
    assert response["success"] is True
    assert "granted" in response["message"]
    
    # Verify consent was created
    user_hash = hashlib.sha256("user@example.com".encode()).hexdigest()
    consent = db.query(UserConsent).filter(
        UserConsent.user_hash == user_hash
    ).first()
    
    assert consent is not None
    assert consent.granted is True
    assert consent.consent_type == ConsentType.ANALYTICS


@pytest.mark.asyncio
async def test_consent_revoke(test_db):
    """Test revoking user consent."""
    from app.routes.privacy import manage_consent, ConsentRequest
    
    db = test_db
    
    request = ConsentRequest(
        email="user@example.com",
        consent_type="marketing",
        granted=False
    )
    
    response = await manage_consent(request, db)
    
    assert response["success"] is True
    assert "revoked" in response["message"]


@pytest.mark.asyncio
async def test_data_export_empty(test_db):
    """Test data export for user with no data."""
    from app.routes.privacy import export_data, DataExportRequest
    
    db = test_db
    
    request = DataExportRequest(email="newuser@example.com")
    
    response = await export_data(request, db)
    
    assert response["success"] is True
    assert "export" in response
    assert response["export"]["data"]["consents"] == []
    assert response["export"]["data"]["tracking_events"] == []


@pytest.mark.asyncio
async def test_data_export_with_data(test_db):
    """Test data export for user with existing data."""
    from app.routes.privacy import export_data, DataExportRequest, manage_consent, ConsentRequest
    
    db = test_db
    
    # Create some test data
    email = "testuser@example.com"
    user_hash = hashlib.sha256(email.encode()).hexdigest()
    
    # Add consent
    consent_req = ConsentRequest(
        email=email,
        consent_type="analytics",
        granted=True
    )
    await manage_consent(consent_req, db)
    
    # Add tracking event
    tracking = TrackingEvent(
        event_type="view",
        session_hash=user_hash,
        ip_hash="test_ip_hash",
        ua_hash="test_ua_hash",
        created_at=datetime.utcnow()
    )
    db.add(tracking)
    db.commit()
    
    # Export data
    export_req = DataExportRequest(email=email)
    response = await export_data(export_req, db)
    
    assert response["success"] is True
    assert len(response["export"]["data"]["consents"]) >= 1
    assert len(response["export"]["data"]["tracking_events"]) >= 1
    
    # Verify audit log was created
    audit_logs = db.query(AuditLog).filter(
        AuditLog.user_hash == user_hash,
        AuditLog.action == "data_export_completed"
    ).all()
    assert len(audit_logs) > 0


@pytest.mark.asyncio
async def test_data_deletion_without_confirmation(test_db):
    """Test data deletion fails without correct confirmation."""
    from app.routes.privacy import delete_data, DataDeletionRequest
    from fastapi import HTTPException
    
    db = test_db
    
    request = DataDeletionRequest(
        email="user@example.com",
        confirmation="wrong text"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await delete_data(request, db)
    
    assert exc_info.value.status_code == 400
    assert "DELETE MY DATA" in exc_info.value.detail


@pytest.mark.asyncio
async def test_data_deletion_success(test_db):
    """Test successful data deletion."""
    from app.routes.privacy import delete_data, DataDeletionRequest, manage_consent, ConsentRequest
    
    db = test_db
    
    # Create test data
    email = "deleteuser@example.com"
    user_hash = hashlib.sha256(email.encode()).hexdigest()
    
    # Add consent
    consent_req = ConsentRequest(
        email=email,
        consent_type="analytics",
        granted=True
    )
    await manage_consent(consent_req, db)
    
    # Add tracking event
    tracking = TrackingEvent(
        event_type="click",
        session_hash=user_hash,
        ip_hash="test_ip",
        created_at=datetime.utcnow()
    )
    db.add(tracking)
    db.commit()
    
    # Verify data exists
    assert db.query(UserConsent).filter(UserConsent.user_hash == user_hash).count() > 0
    assert db.query(TrackingEvent).filter(TrackingEvent.session_hash == user_hash).count() > 0
    
    # Delete data
    delete_req = DataDeletionRequest(
        email=email,
        confirmation="DELETE MY DATA"
    )
    response = await delete_data(delete_req, db)
    
    assert response["success"] is True
    assert response["deleted"]["consents"] > 0
    assert response["deleted"]["tracking_events"] > 0
    
    # Verify data was deleted
    assert db.query(UserConsent).filter(UserConsent.user_hash == user_hash).count() == 0
    assert db.query(TrackingEvent).filter(TrackingEvent.session_hash == user_hash).count() == 0
    
    # Verify audit log was retained
    audit_logs = db.query(AuditLog).filter(
        AuditLog.user_hash == user_hash
    ).all()
    assert len(audit_logs) > 0  # Audit logs should be retained


@pytest.mark.asyncio
async def test_get_consents(test_db):
    """Test getting user consents."""
    from app.routes.privacy import get_consents, manage_consent, ConsentRequest
    
    db = test_db
    
    email = "consentuser@example.com"
    
    # Add multiple consents
    for consent_type in ["analytics", "marketing"]:
        req = ConsentRequest(
            email=email,
            consent_type=consent_type,
            granted=True
        )
        await manage_consent(req, db)
    
    # Get consents
    response = await get_consents(email, db)
    
    assert "consents" in response
    assert len(response["consents"]) >= 2


@pytest.fixture
def test_db():
    """Create a test database session."""
    from app.db import SessionLocal, init_db
    
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
