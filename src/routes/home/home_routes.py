# src\routes\home\home_routes.py

from flask import Blueprint, jsonify
from sqlalchemy import text
from src.config import engine
import os

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return jsonify({"message": "Welcome to Project Food Dome!"})

@home_bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "Operational"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    # Fetch environment variables
    environment = os.getenv("ENVIRONMENT", "Development")
    db_server = os.getenv("DB_SERVER", "Unknown")
    db_name = os.getenv("DB_NAME", "Unknown")
    db_user = os.getenv("DB_USER", "Unknown")
    db_driver = os.getenv("DB_DRIVER", "Unknown")

    health_details = {
        "app_name": "Project Food Dome",
        "version": "1.0.0",
        "status": "Running",
        "database": {
            "status": db_status,
            "server": db_server,
            "name": db_name,
            "user": db_user,
            "driver": db_driver
        },
        "environment": environment
    }

    return jsonify(health_details), 200
