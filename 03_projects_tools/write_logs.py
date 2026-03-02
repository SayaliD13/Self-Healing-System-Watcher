# Title: Universal Database Logger
# Approach: Uses mysql-connector to record system health events.
# Work: Saves logs to MySQL and history.txt backup.

import mysql.connector
import os
from datetime import datetime
from pathlib import Path

def save_log(status, action):
    """Saves system events to MySQL and a backup text file."""
    
    # 1. Database Logging
    try:
        # DB_PASSWORD is set in main.py, we access it here via os.environ
        db_pass = os.environ.get("DB_PASSWORD", "")
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=db_pass,
            database="sys_monitor_db"
        )
        cursor = conn.cursor()
        query = "INSERT INTO logs (issue_found, action_taken) VALUES (%s, %s)"
        cursor.execute(query, (status, action))
        conn.commit()
        conn.close()
        print(">>> [DB] Log successfully recorded in MySQL.")
    except Exception as e:
        print(f">>> [DB ERROR] Could not save to database: {e}")

    # 2. Local File Logging (Backup)
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        log_file = BASE_DIR / "04_activity_logs" / "history.txt"
        
        # Ensure directory exists
        log_file.parent.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] STATUS: {status} | ACTION: {action}\n")
        print(">>> [FILE] Backup saved to history.txt.")
    except Exception as e:
        print(f">>> [FILE ERROR] Could not save backup: {e}")