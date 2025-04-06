from flask import Blueprint, jsonify
from APP.database import db
from sqlalchemy.sql import text
from APP.Services.rate_limiter import limiter
from flask import request
from flask_limiter.util import get_remote_address
health_blueprint = Blueprint('health', __name__)
@health_blueprint.route('/health/db', methods=['GET'])
@limiter.exempt
def check_database_connection():

    try:
        # Execute a simple query to test the connection
        db.session.execute(text("SELECT 1"))
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Database connection is healthy"
        }), 200
    except Exception as e:
        # If there's an error, return failure status
        return jsonify({
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }), 500
    
@health_blueprint.route('/check-limiter', methods=['GET'])
@limiter.limit("5 per minute")
def check_limiter():
    return jsonify({
        "client_ip": request.remote_addr,
        "limiter_key": get_remote_address(),
        "status": "success",
        "message": "Rate limiter is working"
    }), 200