# app.py

from flask import Flask
from src.routes import register_blueprints

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
