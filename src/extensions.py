# src\extensions.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from src.config import connection_string 

# Initialize the extensions
db = SQLAlchemy()
engine = create_engine(connection_string)  
