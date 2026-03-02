# Title: Database Connection Manager
# Approach: Uses mysql-connector to verify connection with MySQL.
# Work: Provides a quick way to test if the database is reachable.

import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables (Password etc.)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

def test_db_connection():
    """
    Independent function to test MySQL connection.
    Useful for debugging before running the main app.
    """
    print(">>> Testing Database Connection...")
    
    try:
        # Get password from environment (set by .env or main.py)
        db_pass = os.getenv("DB_PASSWORD", "sayaligauri") # Default from your .env
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=db_pass
        )
        
        if conn.is_connected():
            print("[SUCCESS] MySQL is connected and reachable!")
            conn.close()
            return True
            
    except Exception as e:
        print(f"[FAILED] Could not connect to MySQL: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()