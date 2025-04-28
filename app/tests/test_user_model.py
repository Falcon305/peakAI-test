import pytest
from app.models.user import User
from app import db

def test_user_creation():
    """Test creating a new user"""
    user = User(username="testuser", password="password123")
    assert user.username == "testuser"
    assert user.password_hash is not None
    assert user.password_hash != "password123"

def test_password_hashing():
    """Test password hashing and verification"""
    user = User(username="testuser", password="password123")
    
    assert user.password_hash != "password123"
    assert user.check_password("password123") is True
    assert user.check_password("wrongpassword") is False
