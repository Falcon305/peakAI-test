from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text
import logging

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    
    Verifies the application and database connection status.
    
    Returns:
    - status: Status of the application (healthy/unhealthy)
    - components: 
        - api: Status of the API (healthy)
        - database: Database connection status (healthy/unhealthy)
        - database_error: Error message if database connection fails
    """
    try:
        db_status = "healthy"
        db_error = None
        
        try:
            db.session.execute(text('SELECT 1'))
            logger.info("Database connection successful")
        except Exception as e:
            db_status = "unhealthy"
            db_error = str(e)
            logger.error(f"Database connection failed: {e}")
        
        response = {
            "status": "healthy" if db_status == "healthy" else "unhealthy",
            "components": {
                "api": "healthy",
                "database": db_status
            }
        }
        
        if db_error:
            response["components"]["database_error"] = db_error
            
        status_code = 200 if db_status == "healthy" else 503
        
        return jsonify(response), status_code
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
