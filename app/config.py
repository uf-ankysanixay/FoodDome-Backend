import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
if os.getenv("WEBSITE_ENVIRONMENT"):
    print("Running in Azure environment")
else:
    dotenv_path = ".env"
    if os.path.exists(dotenv_path):
        print(f"Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path)
    else:
        print("No .env file found in the current directory")

# Database connection settings
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER")

# Construct the connection string
connection_string = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER}"

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Debug environment variables (only in development)
if not os.getenv("WEBSITE_ENVIRONMENT"):
    print(f"DB_SERVER: {DB_SERVER}")
    print(f"DB_NAME: {DB_NAME}")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_PASSWORD: {DB_PASSWORD}")
    print(f"DB_DRIVER: {DB_DRIVER}")
    print(f"Connection string: {connection_string}")
