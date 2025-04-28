import json
import pytest

def test_swagger_json_endpoint(client):
    """Test that the Swagger JSON endpoint returns a valid Swagger specification."""
    response = client.get('/api/swagger.json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'openapi' in data
    assert 'info' in data
    assert 'title' in data['info']
    assert 'paths' in data
    
    assert '/health' in data['paths']
    assert 'get' in data['paths']['/health']

def test_swagger_ui_endpoint(client):
    """Test that the Swagger UI endpoint is accessible."""
    response = client.get('/api/docs/')
    
    assert response.status_code == 200
    assert b'swagger-ui' in response.data
