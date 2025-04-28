from flask import Blueprint, request, jsonify
from app import db
from app.models.journal import Journal
from app.models.user import User
from app.utils.auth import token_required
from app.services.liwc_analyzer import LIWCAnalyzer
import json

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/journals', methods=['POST'])
@token_required
def create_journal(current_user):
    """
    Create a new journal entry.
    
    Submits a journal text for LIWC analysis and returns scores based on linguistic features.
    
    Required JSON body:
    - text: The journal entry text to analyze
    
    Returns:
    - journal_id: ID of the created journal entry
    - score: Analysis results with category scores and total score
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Text is required'
        }), 400
    
    scores = LIWCAnalyzer.analyze_text(data['text'])
    
    journal = Journal(
        text=data['text'],
        user_id=current_user.id
    )
    
    journal.set_scores(scores)
    
    db.session.add(journal)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'journal_id': journal.id,
        'score': scores
    }), 201

@journal_bp.route('/journals/<int:journal_id>/score', methods=['GET'])
@token_required
def get_journal_score(current_user, journal_id):
    """
    Get the score for a journal entry.
    
    Retrieves the linguistic analysis scores for a previously submitted journal entry.
    
    Parameters:
    - journal_id: ID of the journal entry to retrieve scores for
    
    Returns:
    - journal_id: ID of the journal entry
    - score: Analysis results with category scores and total score
    """
    journal = db.session.get(Journal, journal_id)
    
    if not journal:
        return jsonify({
            'status': 'error',
            'message': 'Journal not found'
        }), 404
    
    if journal.user_id != current_user.id:
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to access this journal'
        }), 403
    
    scores = journal.get_scores()
    return jsonify({
        'status': 'success',
        'journal_id': journal.id,
        'score': scores
    }), 200

@journal_bp.route('/journals', methods=['GET'])
@token_required
def get_user_journals(current_user):
    """
    Get all journals for the current user.
    
    Retrieves all journal entries submitted by the authenticated user.
    
    Returns:
    - journals: List of journal entries with their details
    """
    journals = Journal.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'status': 'success',
        'journals': [journal.to_dict() for journal in journals]
    }), 200
