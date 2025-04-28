import json
import pytest
from flask import url_for

def test_health_check_healthy(client, mock_db_healthy):
    """Test the health check endpoint when database is healthy."""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['components']['api'] == 'healthy'
    assert data['components']['database'] == 'healthy'
    assert 'database_error' not in data['components']

def test_health_check_unhealthy(client, mock_db_unhealthy):
    """Test the health check endpoint when database is unhealthy."""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 503
    assert data['status'] == 'unhealthy'
    assert data['components']['api'] == 'healthy'
    assert data['components']['database'] == 'unhealthy'
    assert 'database_error' in data['components']
    assert data['components']['database_error'] == 'Database connection error'

def test_health_check_exception(client, monkeypatch):
    """Test the health check endpoint when an unexpected exception occurs."""
    def mock_execute(*args, **kwargs):
        raise RuntimeError("Unexpected error")
    
    monkeypatch.setattr('app.routes.health.db.session.execute', mock_execute)
    
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 503
    assert data['status'] == 'unhealthy'
    assert data['components']['api'] == 'healthy'
    assert data['components']['database'] == 'unhealthy'
    assert data['components']['database_error'] == 'Unexpected error'
