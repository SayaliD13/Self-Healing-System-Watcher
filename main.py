# Title: Self-Healing System Watcher
# Approach: Using Python to connect C++ monitoring with MySQL logging.
# Work: Runs health checks and fixes system issues automatically.

import subprocess
import sys
import os
import importlib.util
from pathlib import Path

# 1. AUTO INSTALLER (Checks first, then installs) 
def install_tools():
    tools = ["mysql-connector-python", "python-dotenv"]
    for tool in tools:
        if importlib.util.find_spec(tool.replace("-", "_")) is None:
            print(f"[INFO] Installing {tool} for the first time...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", tool], stdout=subprocess.DEVNULL)

install_tools()

import mysql.connector
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 2. DATABASE SETUP
def setup_db():
    common_pass = ["", "root", "password"]
    conn = None
    
    for pwd in common_pass:
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password=pwd, connect_timeout=2)
            os.environ["DB_PASSWORD"] = pwd
            break
        except: continue

    if not conn:
        print("\n" + "!"*30)
        user_pwd = input("Enter your MySQL Password: ")
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password=user_pwd)
            os.environ["DB_PASSWORD"] = user_pwd
        except:
            print("[ERROR] Could not connect to MySQL. Closing."); return False

    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS sys_monitor_db")
    cursor.execute("USE sys_monitor_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            issue_found VARCHAR(255),
            action_taken VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    return True

# 3. RUNNER 
def start_project():
    print("="*50)
    print("      SELF-HEALING SYSTEM WATCHER ACTIVE      ")
    print("="*50)

    if not setup_db(): return

    # Correct Path to error_repair.py
    REPAIR_PATH = BASE_DIR / "02_system_monitoring" / "error_repair.py"
    spec = importlib.util.spec_from_file_location("error_repair", str(REPAIR_PATH))
    repair_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(repair_module)

    count = 1
    while True:
        print(f"\n>>> CYCLE {count} STARTING...")
        repair_module.monitor_system_health()
        print(f">>> CYCLE {count} COMPLETED.")
        
        print("\n[CONTROLS] 'n' = Next Cycle | 's' = Stop")
        choice = input("Select: ").lower()

        if choice == 'n':
            count += 1
        elif choice == 's':
            print("Shutting down... Goodbye!")
            break
        else:
            print("Invalid input. Press 'n' or 's'.")

if __name__ == "__main__":
    start_project()