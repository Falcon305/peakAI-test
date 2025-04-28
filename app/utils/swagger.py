from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

def create_swagger_spec(app):
    """Create an APISpec object with the Flask app"""
    spec = APISpec(
        title="Flask PostgreSQL API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        info={
            "description": "A simple Flask API with PostgreSQL database",
            "contact": {"email": "admin@example.com"}
        },
    )
    
    # Add health check endpoint documentation
    with app.test_request_context():
        spec.path(view=app.view_functions['health.health_check'])
    
    return spec

def setup_swagger(app: Flask):
    """Setup Swagger documentation for the Flask app"""
    # Create Swagger spec
    spec = create_swagger_spec(app)
    
    # Create a blueprint for serving the Swagger spec
    swagger_bp = Blueprint('swagger', __name__)
    
    @swagger_bp.route('/api/swagger.json')
    def create_swagger_spec_endpoint():
        return jsonify(spec.to_dict())
    
    # Register the swagger blueprint
    app.register_blueprint(swagger_bp)
    
    # Configure Swagger UI
    swagger_ui_blueprint = get_swaggerui_blueprint(
        '/api/docs',
        '/api/swagger.json',
        config={
            'app_name': "Flask PostgreSQL API"
        }
    )
    
    # Register the Swagger UI blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix='/api/docs')
    
    return app
