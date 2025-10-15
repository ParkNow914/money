"""
Privacy and DSAR (Data Subject Access Request) routes.

Implements LGPD compliance endpoints for data export, deletion, and consent management.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import hashlib
from datetime import datetime

from app.config import settings
from app.db import get_db
from app.models import UserConsent, AuditLog, ConsentType

router = APIRouter()


class ConsentRequest(BaseModel):
    """Request to grant or revoke consent."""
    email: EmailStr
    consent_type: str
    granted: bool


class DataExportRequest(BaseModel):
    """Request to export user data."""
    email: EmailStr


class DataDeletionRequest(BaseModel):
    """Request to delete user data."""
    email: EmailStr
    confirmation: str  # User must confirm with specific text


@router.post("/consent")
async def manage_consent(request: ConsentRequest, db: Session = Depends(get_db)):
    """
    Grant or revoke user consent.
    
    LGPD Article 8: Consent must be freely given, specific, informed and unambiguous.
    """
    # Hash email for privacy
    user_hash = hashlib.sha256(request.email.encode()).hexdigest()
    
    # Validate consent type
    try:
        consent_type_enum = ConsentType(request.consent_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid consent type: {request.consent_type}")
    
    # Create or update consent
    consent = UserConsent(
        user_hash=user_hash,
        consent_type=consent_type_enum,
        granted=request.granted,
        granted_at=datetime.utcnow()
    )
    
    db.add(consent)
    
    # Audit log
    audit = AuditLog(
        action="consent_grant" if request.granted else "consent_revoke",
        user_hash=user_hash,
        details={"consent_type": request.consent_type},
        created_at=datetime.utcnow()
    )
    db.add(audit)
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Consent {'granted' if request.granted else 'revoked'} for {request.consent_type}",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/export")
async def export_data(request: DataExportRequest, db: Session = Depends(get_db)):
    """
    Export all user data (DSAR - Data Subject Access Request).
    
    LGPD Article 18: Right to access data.
    
    Note: This is a placeholder. Full implementation requires:
    - Verification flow (email confirmation)
    - Data gathering from all tables
    - Structured export format
    """
    # Hash email
    user_hash = hashlib.sha256(request.email.encode()).hexdigest()
    
    # TODO: Implement full data export
    # - Query all tables for user_hash
    # - Format data in portable format (JSON/CSV)
    # - Send via email or download link
    
    # Audit log
    audit = AuditLog(
        action="data_export_request",
        user_hash=user_hash,
        details={"status": "pending"},
        created_at=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    
    return {
        "success": True,
        "message": "Data export request received. You will receive an email with your data.",
        "status": "pending",
        "note": "Full implementation pending - Phase 2"
    }


@router.post("/delete")
async def delete_data(request: DataDeletionRequest, db: Session = Depends(get_db)):
    """
    Delete all user data (DSAR - Right to be forgotten).
    
    LGPD Article 18: Right to deletion.
    
    Note: This is a placeholder. Full implementation requires:
    - Verification flow
    - Cascading deletion across tables
    - Retention of audit logs for legal compliance
    """
    if request.confirmation != "DELETE MY DATA":
        raise HTTPException(
            status_code=400,
            detail="Confirmation text must be exactly: DELETE MY DATA"
        )
    
    # Hash email
    user_hash = hashlib.sha256(request.email.encode()).hexdigest()
    
    # TODO: Implement full data deletion
    # - Verify user identity
    # - Delete from all tables (except audit logs)
    # - Keep audit logs for legal compliance
    
    # Audit log
    audit = AuditLog(
        action="data_deletion_request",
        user_hash=user_hash,
        details={"status": "pending"},
        created_at=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    
    return {
        "success": True,
        "message": "Data deletion request received. You will receive confirmation.",
        "status": "pending",
        "note": "Full implementation pending - Phase 2"
    }


@router.get("/consents/{email}")
async def get_consents(email: str, db: Session = Depends(get_db)):
    """
    Get all consents for a user.
    
    Public endpoint for transparency.
    """
    user_hash = hashlib.sha256(email.encode()).hexdigest()
    
    consents = db.query(UserConsent).filter(
        UserConsent.user_hash == user_hash
    ).order_by(UserConsent.granted_at.desc()).all()
    
    return {
        "consents": [
            {
                "consent_type": c.consent_type.value,
                "granted": c.granted,
                "granted_at": c.granted_at.isoformat()
            }
            for c in consents
        ]
    }
