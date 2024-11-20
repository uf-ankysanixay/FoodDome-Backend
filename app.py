from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.routes import register_blueprints
from src.extensions import db  # Import SQLAlchemy

import os

# Load environment variables
load_dotenv()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Configure app settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///example.db')  # Update this with your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure CORS
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")  # Default to allow all origins if not set
    CORS(app, resources={r"/*": {"origins": cors_origins}})

    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Register blueprints
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
