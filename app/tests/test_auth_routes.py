import pytest
import json
from app.models.user import User
from app import db

def test_register_endpoint(client):
    """Test user registration endpoint structure"""
    response = client.post(
        '/users',
        data=json.dumps({
            'username': 'testuser',
            'password': 'password123'
        }),
        content_type='application/json'
    )
    
    assert response.content_type == 'application/json'

def test_register_user_missing_fields(client):
    """Test user registration with missing fields"""
    response = client.post(
        '/users',
        data=json.dumps({
            'username': 'incompleteuser'
        }),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['message'] == 'Missing required fields'

def test_login_endpoint(client):
    """Test login endpoint structure"""
    response = client.post(
        '/login',
        data=json.dumps({
            'username': 'testuser',
            'password': 'password123'
        }),
        content_type='application/json'
    )
    
    assert response.content_type == 'application/json'

