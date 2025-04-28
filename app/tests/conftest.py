import pytest
import os
from app import create_app, db
from sqlalchemy import text

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    
    # Using a dedicated test database in PostgreSQL
    test_db_url = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres_test')
    
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_url,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def mock_db_healthy(monkeypatch):
    """Mock a healthy database connection."""
    def mock_execute(*args, **kwargs):
        return True
    
    monkeypatch.setattr(db.session, 'execute', mock_execute)

@pytest.fixture
def mock_db_unhealthy(monkeypatch):
    """Mock an unhealthy database connection."""
    def mock_execute(*args, **kwargs):
        raise Exception("Database connection error")
    
    monkeypatch.setattr(db.session, 'execute', mock_execute)
