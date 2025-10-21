"""
Encryption utilities for sensitive data at rest.
Uses AES-256 encryption with the configured encryption key.
"""
import base64
import hashlib
from typing import Optional

from cryptography.fernet import Fernet

from app.config import settings


def _get_fernet() -> Fernet:
    """
    Get Fernet cipher instance using the encryption key from settings.
    The key must be 32 bytes, base64-encoded.
    """
    # Ensure key is proper format
    key = settings.encryption_key.encode()
    # Hash the key to get exactly 32 bytes
    key_hash = hashlib.sha256(key).digest()
    # Base64 encode for Fernet
    key_b64 = base64.urlsafe_b64encode(key_hash)
    return Fernet(key_b64)


def encrypt_string(plaintext: str) -> str:
    """
    Encrypt a string value.
    
    Args:
        plaintext: String to encrypt
        
    Returns:
        Base64-encoded encrypted string
    """
    if not plaintext:
        return ""
    
    fernet = _get_fernet()
    encrypted = fernet.encrypt(plaintext.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_string(ciphertext: str) -> Optional[str]:
    """
    Decrypt an encrypted string.
    
    Args:
        ciphertext: Base64-encoded encrypted string
        
    Returns:
        Decrypted string or None if decryption fails
    """
    if not ciphertext:
        return None
    
    try:
        fernet = _get_fernet()
        encrypted = base64.urlsafe_b64decode(ciphertext.encode())
        decrypted = fernet.decrypt(encrypted)
        return decrypted.decode()
    except Exception:
        return None


def encrypt_dict_field(data: dict, field: str) -> dict:
    """
    Encrypt a specific field in a dictionary.
    
    Args:
        data: Dictionary containing the field
        field: Field name to encrypt
        
    Returns:
        Dictionary with encrypted field
    """
    if field in data and data[field]:
        data[field] = encrypt_string(str(data[field]))
    return data


def decrypt_dict_field(data: dict, field: str) -> dict:
    """
    Decrypt a specific field in a dictionary.
    
    Args:
        data: Dictionary containing the field
        field: Field name to decrypt
        
    Returns:
        Dictionary with decrypted field
    """
    if field in data and data[field]:
        decrypted = decrypt_string(data[field])
        if decrypted:
            data[field] = decrypted
    return data
