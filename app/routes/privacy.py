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
    
    Returns all data associated with the user in a portable JSON format.
    """
    from app.models import TrackingEvent
    
    # Hash email
    user_hash = hashlib.sha256(request.email.encode()).hexdigest()
    
    # Gather all user data from tables
    export_data = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "user_hash": user_hash,
        "email_hash": user_hash,  # For clarity
        "data": {}
    }
    
    # 1. Consents
    consents = db.query(UserConsent).filter(
        UserConsent.user_hash == user_hash
    ).all()
    export_data["data"]["consents"] = [
        {
            "id": c.id,
            "consent_type": c.consent_type.value,
            "granted": c.granted,
            "granted_at": c.granted_at.isoformat(),
            "ip_hash": c.ip_hash,
            "user_agent_hash": c.user_agent_hash,
            "expires_at": c.expires_at.isoformat() if c.expires_at else None
        }
        for c in consents
    ]
    
    # 2. Tracking events (by session_hash or ip_hash that could match)
    tracking_events = db.query(TrackingEvent).filter(
        TrackingEvent.session_hash == user_hash
    ).all()
    export_data["data"]["tracking_events"] = [
        {
            "id": e.id,
            "event_type": e.event_type,
            "article_id": e.article_id,
            "session_hash": e.session_hash,
            "ip_hash": e.ip_hash,
            "ua_hash": e.ua_hash,
            "utm_source": e.utm_source,
            "utm_medium": e.utm_medium,
            "utm_campaign": e.utm_campaign,
            "revenue": e.revenue,
            "created_at": e.created_at.isoformat()
        }
        for e in tracking_events
    ]
    
    # 3. Audit logs for this user
    audit_logs = db.query(AuditLog).filter(
        AuditLog.user_hash == user_hash
    ).all()
    export_data["data"]["audit_logs"] = [
        {
            "id": a.id,
            "action": a.action,
            "details": a.details,
            "created_at": a.created_at.isoformat(),
            "ip_hash": a.ip_hash
        }
        for a in audit_logs
    ]
    
    # Create audit log for this export
    audit = AuditLog(
        action="data_export_completed",
        user_hash=user_hash,
        details={
            "status": "completed",
            "records_exported": {
                "consents": len(export_data["data"]["consents"]),
                "tracking_events": len(export_data["data"]["tracking_events"]),
                "audit_logs": len(export_data["data"]["audit_logs"])
            }
        },
        created_at=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    
    return {
        "success": True,
        "message": "Data export completed",
        "export": export_data
    }


@router.post("/delete")
async def delete_data(request: DataDeletionRequest, db: Session = Depends(get_db)):
    """
    Delete all user data (DSAR - Right to be forgotten).
    
    LGPD Article 18: Right to deletion.
    
    Deletes all user data except audit logs (required for legal compliance).
    """
    from app.models import TrackingEvent
    
    if request.confirmation != "DELETE MY DATA":
        raise HTTPException(
            status_code=400,
            detail="Confirmation text must be exactly: DELETE MY DATA"
        )
    
    # Hash email
    user_hash = hashlib.sha256(request.email.encode()).hexdigest()
    
    # Count records before deletion
    consents_count = db.query(UserConsent).filter(
        UserConsent.user_hash == user_hash
    ).count()
    
    tracking_count = db.query(TrackingEvent).filter(
        TrackingEvent.session_hash == user_hash
    ).count()
    
    # Delete consents
    db.query(UserConsent).filter(
        UserConsent.user_hash == user_hash
    ).delete()
    
    # Delete tracking events
    db.query(TrackingEvent).filter(
        TrackingEvent.session_hash == user_hash
    ).delete()
    
    # Create audit log (this is kept for legal compliance)
    audit = AuditLog(
        action="data_deletion_completed",
        user_hash=user_hash,
        details={
            "status": "completed",
            "records_deleted": {
                "consents": consents_count,
                "tracking_events": tracking_count
            },
            "audit_logs_retained": "yes (legal requirement)"
        },
        created_at=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    
    return {
        "success": True,
        "message": "All user data has been deleted (except audit logs for legal compliance)",
        "deleted": {
            "consents": consents_count,
            "tracking_events": tracking_count
        },
        "retained": {
            "audit_logs": "Required for legal compliance (LGPD Article 37)"
        }
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
