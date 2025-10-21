"""Tests for security utilities."""
import pytest

from app.security import (
    create_access_token,
    decode_access_token,
    generate_secure_token,
    hash_ip_address,
    hash_password,
    hash_user_agent,
    hash_with_salt,
    sanitize_filename,
    verify_password,
)


class TestPasswordHashing:
    """Tests for password hashing."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "my_secure_password_123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert "$argon2" in hashed

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "my_secure_password_123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "my_secure_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False


class TestTokenGeneration:
    """Tests for token generation."""

    def test_generate_secure_token_default_length(self):
        """Test secure token generation with default length."""
        token = generate_secure_token()

        assert len(token) == 64  # 32 bytes = 64 hex chars
        assert all(c in "0123456789abcdef" for c in token)

    def test_generate_secure_token_custom_length(self):
        """Test secure token generation with custom length."""
        token = generate_secure_token(length=16)

        assert len(token) == 32  # 16 bytes = 32 hex chars

    def test_tokens_are_unique(self):
        """Test that generated tokens are unique."""
        token1 = generate_secure_token()
        token2 = generate_secure_token()

        assert token1 != token2


class TestJWTTokens:
    """Tests for JWT token operations."""

    def test_create_and_decode_token(self):
        """Test creating and decoding JWT tokens."""
        data = {"user_id": 123, "username": "testuser"}
        token = create_access_token(data)

        decoded = decode_access_token(token)

        assert decoded is not None
        assert decoded["user_id"] == 123
        assert decoded["username"] == "testuser"
        assert "exp" in decoded

    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"

        decoded = decode_access_token(invalid_token)

        assert decoded is None


class TestPrivacyHashing:
    """Tests for privacy-preserving hashing."""

    def test_hash_with_salt(self):
        """Test hashing with salt."""
        value = "192.168.1.1"
        hashed = hash_with_salt(value)

        assert hashed != value
        assert len(hashed) == 64  # SHA256 hex length

    def test_hash_with_custom_salt(self):
        """Test hashing with custom salt."""
        value = "192.168.1.1"
        salt = "my_custom_salt"

        hashed1 = hash_with_salt(value, salt)
        hashed2 = hash_with_salt(value, salt)

        assert hashed1 == hashed2  # Same salt = same hash

    def test_hash_ip_address(self):
        """Test IP address hashing."""
        ip = "192.168.1.1"
        hashed = hash_ip_address(ip)

        assert hashed != ip
        assert len(hashed) == 64

    def test_hash_user_agent(self):
        """Test user agent hashing."""
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        hashed = hash_user_agent(ua)

        assert hashed != ua
        assert len(hashed) == 64


class TestFilenameSanitization:
    """Tests for filename sanitization."""

    def test_sanitize_basic_filename(self):
        """Test sanitizing a normal filename."""
        filename = "my_document.pdf"
        sanitized = sanitize_filename(filename)

        assert sanitized == "my_document.pdf"

    def test_sanitize_dangerous_characters(self):
        """Test sanitizing filename with dangerous characters."""
        filename = "my<doc>ument:test.pdf"
        sanitized = sanitize_filename(filename)

        assert "<" not in sanitized
        assert ">" not in sanitized
        assert ":" not in sanitized

    def test_sanitize_path_traversal(self):
        """Test sanitizing filename with path traversal attempt."""
        filename = "../../../etc/passwd"
        sanitized = sanitize_filename(filename)

        assert ".." not in sanitized or "/" not in sanitized
        assert sanitized != filename

    def test_sanitize_long_filename(self):
        """Test sanitizing very long filename."""
        filename = "a" * 300 + ".txt"
        sanitized = sanitize_filename(filename)

        assert len(sanitized) <= 255

    def test_sanitize_empty_filename(self):
        """Test sanitizing empty filename."""
        filename = ""
        sanitized = sanitize_filename(filename)

        assert sanitized == "unnamed"
