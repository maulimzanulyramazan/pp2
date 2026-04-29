# Database connection module
import psycopg2                     # Import PostgreSQL adapter
from config import host, database, user, password, port  # Import config values

def connect():
    """Establish and return a connection to PostgreSQL database"""
    conn = psycopg2.connect(        # Create connection object
        host=host,                  # Server address
        database=database,          # Database name
        user=user,                  # Username
        password=password,          # Password
        port=port                   # Port number
    )
    return conn                     # Return connection object