import pytest
import json
from app.models.journal import Journal
from app.models.category import Category, Word
from app.models.user import User
from app.services.liwc_analyzer import LIWCAnalyzer
from app import db

def test_create_journal(client, auth_headers):
    """Test creating a journal entry"""
    response = client.post(
        '/journals',
        data=json.dumps({
            'text': 'I am happy today, but I was sad yesterday.'
        }),
        headers=auth_headers,
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'journal_id' in data
    assert 'score' in data
    assert 'categories' in data['score']
    assert 'total' in data['score']

def test_create_journal_missing_text(client, auth_headers):
    """Test creating a journal entry with missing text"""
    response = client.post(
        '/journals',
        data=json.dumps({}),
        headers=auth_headers,
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert response.content_type == 'application/json'

def test_get_journal_score(client, auth_headers):
    """Test getting a journal score"""
    user = db.session.query(User).filter_by(username='testuser').first()
    user_id = user.id
    
    text = 'I am happy today, but I was sad yesterday.'
    scores = LIWCAnalyzer.analyze_text(text)
    
    journal = Journal(text=text, user_id=user_id)
    journal.set_scores(scores)
    db.session.add(journal)
    db.session.commit()
    
    response = client.get(
        f'/journals/{journal.id}/score',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert data['journal_id'] == journal.id
    assert 'score' in data
    assert 'categories' in data['score']
    assert 'total' in data['score']

def test_get_journal_score_not_found(client, auth_headers):
    """Test getting a journal score for a non-existent journal"""
    response = client.get(
        '/journals/999/score',
        headers=auth_headers
    )
    
    assert response.status_code == 404
    assert response.content_type == 'application/json'

def test_get_user_journals(client, auth_headers):
    """Test getting all journals for a user"""
    user = db.session.query(User).filter_by(username='testuser').first()
    user_id = user.id
    
    text1 = 'I am happy today.'
    text2 = 'I was sad yesterday.'
    scores1 = LIWCAnalyzer.analyze_text(text1)
    scores2 = LIWCAnalyzer.analyze_text(text2)
    
    journal1 = Journal(text=text1, user_id=user_id)
    journal2 = Journal(text=text2, user_id=user_id)
    
    journal1.set_scores(scores1)
    journal2.set_scores(scores2)
    
    db.session.add(journal1)
    db.session.add(journal2)
    db.session.commit()
    
    response = client.get(
        '/journals',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'journals' in data
    assert len(data['journals']) >= 2
    
    for journal in data['journals']:
        assert 'scores' in journal or journal['scores'] is None

def test_liwc_analyzer(app):
    """Test the LIWC analyzer"""
    with app.app_context():
        text = 'I am happy today, but I was sad yesterday.'
        scores = LIWCAnalyzer.analyze_text(text)
        
        assert 'categories' in scores
        assert 'total' in scores
        
        assert isinstance(scores['categories'], dict)
        assert isinstance(scores['total'], int)
