"""
Security utilities for AutoCash Ultimate.
Includes password hashing, token generation, and hashing utilities.
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Password hashing context (Argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Length of token in bytes (default 32)
        
    Returns:
        Hex-encoded secure token
    """
    return secrets.token_hex(length)


def hash_with_salt(value: str, salt: Optional[str] = None) -> str:
    """
    Hash a value with optional salt using SHA-256.
    Used for privacy-preserving identifiers (IP, user agent, etc.)
    
    Args:
        value: Value to hash
        salt: Optional salt (uses secret_key if not provided)
        
    Returns:
        Hex-encoded hash
    """
    if salt is None:
        salt = settings.secret_key
    hasher = hashlib.sha256()
    hasher.update(salt.encode())
    hasher.update(value.encode())
    return hasher.hexdigest()


def hash_ip_address(ip: str) -> str:
    """
    Hash an IP address for privacy-compliant storage.
    Uses HMAC-SHA256 with secret key.
    
    Args:
        ip: IP address to hash
        
    Returns:
        Hashed IP address
    """
    return hmac.new(
        settings.secret_key.encode(), ip.encode(), hashlib.sha256
    ).hexdigest()


def hash_user_agent(user_agent: str) -> str:
    """
    Hash a user agent string for privacy-compliant storage.
    
    Args:
        user_agent: User agent string
        
    Returns:
        Hashed user agent
    """
    return hash_with_salt(user_agent)


def create_visitor_hash(ip: str, user_agent: str) -> str:
    """
    Create a combined hash for visitor identification.
    Privacy-preserving: hashes IP + UA together.
    
    Args:
        ip: IP address
        user_agent: User agent string
        
    Returns:
        Combined visitor hash
    """
    combined = f"{ip}:{user_agent}"
    return hash_with_salt(combined)


def verify_hmac_signature(data: str, signature: str, key: Optional[str] = None) -> bool:
    """
    Verify HMAC signature.
    
    Args:
        data: Original data
        signature: HMAC signature to verify
        key: Optional key (uses secret_key if not provided)
        
    Returns:
        True if signature is valid
    """
    if key is None:
        key = settings.secret_key
    expected = hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent directory traversal and other attacks.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    from pathlib import Path

    # Remove any path components
    filename = Path(filename).name

    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove null bytes
    filename = filename.replace("\x00", "")

    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        name = name[: 255 - len(ext) - 1]
        filename = f"{name}.{ext}" if ext else name

    return filename or "unnamed"
