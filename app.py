from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Determine if running in production or development
if os.getenv("WEBSITE_ENVIRONMENT"):
    # Running in Azure (Production)
    print("Running in Azure environment")
else:
    # Running locally (Development)
    dotenv_path = ".env"
    if os.path.exists(dotenv_path):
        print(f"Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path)
    else:
        print("No .env file found in the current directory")

# Initialize Flask app
app = Flask(__name__)

# Database connection settings
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER")

# Construct the connection string
connection_string = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER}"
engine = create_engine(connection_string)

# Debug environment variables (only in development)
if not os.getenv("WEBSITE_ENVIRONMENT"):
    print(f"DB_SERVER: {DB_SERVER}")
    print(f"DB_NAME: {DB_NAME}")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_PASSWORD: {DB_PASSWORD}")
    print(f"DB_DRIVER: {DB_DRIVER}")
    print(f"Connection string: {connection_string}")

# Home endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Project Food Dome!"})

# Database test endpoint
@app.route('/db-test', methods=['GET'])
def db_test():
    try:
        with engine.connect() as connection:
            # Use SQLAlchemy's `text` for the raw query
            result = connection.execute(text("SELECT 'Connection successful!' AS message"))
            row = result.fetchone()
            # Access the first column in the result tuple
            return jsonify({"message": row[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health Check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "Operational"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    # Application health details
    health_details = {
        "app_name": "Project Food Dome",
        "version": "1.0.0",
        "status": "Running",
        "database": db_status,
        "environment": os.getenv("WEBSITE_ENVIRONMENT", "Development"),
    }

    return jsonify(health_details), 200

if __name__ == '__main__':
    app.run(debug=True)
