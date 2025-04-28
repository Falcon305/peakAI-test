from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import json

def create_swagger_spec(app):
    """Create an APISpec object with the Flask app"""
    spec = APISpec(
        title="Cognitive Assessment API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        info={
            "description": "Cognitive Assessment API - A platform for analyzing journal entries using LIWC algorithm"
        },
    )
    
    # Define security scheme for JWT authentication
    spec.components.security_scheme("Bearer", {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    })
    
    # Add endpoint documentation
    with app.test_request_context():
        # Health endpoint
        spec.path(view=app.view_functions['health.health_check'])
        # Auth endpoints
        spec.path(view=app.view_functions['auth.register_user'])
        spec.path(view=app.view_functions['auth.login'])
        # Journal endpoints
        spec.path(view=app.view_functions['journal.create_journal'])
        spec.path(view=app.view_functions['journal.get_journal_score'])
        spec.path(view=app.view_functions['journal.get_user_journals'])
    
    return spec

def setup_swagger(app: Flask):
    """Setup Swagger documentation for the Flask app"""
    swagger_bp = Blueprint('swagger', __name__)
    
    @swagger_bp.route('/api/swagger.json')
    def create_swagger_spec_endpoint():
        with open('app/static/swagger.json', 'r') as f:
            swagger_spec = json.load(f)
        return jsonify(swagger_spec)
    
    app.register_blueprint(swagger_bp)
    
    swagger_ui_blueprint = get_swaggerui_blueprint(
        '/api/docs',
        '/api/swagger.json',
        config={
            'app_name': "Cognitive Assessment API"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix='/api/docs')
    
    return app
