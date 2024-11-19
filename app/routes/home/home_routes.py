from flask import Blueprint, jsonify
from sqlalchemy import text
from app.config import engine

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return jsonify({"message": "Welcome to Project Food Dome!"})

@home_bp.route('/db-test', methods=['GET'])
def db_test():
    try:
        with engine.connect() as connection:
            # Use SQLAlchemy's `text` for the raw query
            result = connection.execute(text("SELECT 'Connection successful!' AS message"))
            row = result.fetchone()
            return jsonify({"message": row[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@home_bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "Operational"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    health_details = {
        "app_name": "Project Food Dome",
        "version": "1.0.0",
        "status": "Running",
        "database": db_status,
        "environment": "Production" if db_status == "Operational" else "Development"
    }

    return jsonify(health_details), 200
