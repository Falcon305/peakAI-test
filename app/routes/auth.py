from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user.
    
    Creates a new user account with username and password. Passwords are securely hashed.
    
    Required JSON body:
    - username: Unique username for the account
    - password: Password for the account
    
    Returns:
    - status: Success or error status
    - message: Description of the outcome
    - user: User details if registration was successful
    
    Status Codes:
    - 201: User created successfully
    - 400: Invalid request (missing fields)
    - 409: Username already exists
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Username already exists'
        }), 409
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Authenticates a user with username and password and returns a JWT token for accessing protected routes.
    
    Required JSON body:
    - username: Username of the account
    - password: Password for the account
    
    Returns:
    - status: Success or error status
    - message: Description of the outcome
    - token: JWT token if authentication succeeds
    - user: User details if authentication succeeds
    
    Status Codes:
    - 200: Login successful
    - 400: Invalid request (missing fields)
    - 401: Authentication failed (invalid credentials)
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    try:
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            token = user.generate_token()
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({
            'status': 'error',
            'message': 'Invalid credentials'
        }), 401
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
