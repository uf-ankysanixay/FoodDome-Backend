# src\config.py

import os
from dotenv import load_dotenv

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