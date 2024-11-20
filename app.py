# app.py

from flask import Flask
from flask_cors import CORS
from src.routes import register_blueprints
from src.extensions import db  # Import SQLAlchemy
from src.config import connection_string  # Import constructed connection string

import os

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Configure app settings
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string  # Use the constructed connection string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure CORS
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")  # Default to allow all origins if not set
    CORS(app, resources={r"/*": {"origins": cors_origins}})

    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Register blueprints
    register_blueprints(app)

    return app

# Create and expose the app instance for Gunicorn
app = create_app()

# Create tables in development (if needed)
if not os.getenv("WEBSITE_ENVIRONMENT"):  # Only run locally
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
