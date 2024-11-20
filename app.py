# app.py

from flask import Flask
from flask_cors import CORS
from src.routes import register_blueprints
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")  # Default to allow all origins if not set
CORS(app, resources={r"/*": {"origins": cors_origins}})

# Register blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
