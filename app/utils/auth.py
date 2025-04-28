from functools import wraps
from flask import request, jsonify
from app.models.user import User
import jwt

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'status': 'error',
                    'message': 'Token is missing or invalid'
                }), 401
        
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token is missing'
            }), 401
        
        try:
            user_id = User.decode_token(token)
            
            if isinstance(user_id, str):
                return jsonify({
                    'status': 'error',
                    'message': user_id
                }), 401
                
            current_user = User.query.get(user_id)
            
            if not current_user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
            
        return f(current_user, *args, **kwargs)
    
    return decorated
