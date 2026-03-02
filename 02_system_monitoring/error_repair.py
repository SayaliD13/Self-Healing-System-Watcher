# Title: Self-Healing Repair Logic
# Approach: Executes the C++ monitor and processes the system health status.
# Work: Detects system issues and triggers an automated repair sequence while logging data.

import subprocess
import os
import sys
import importlib.util
from pathlib import Path

# Define base directory and paths
BASE_DIR = Path(__file__).resolve().parent.parent
# Make sure this folder name matches your actual folder name!
LOG_MODULE_PATH = BASE_DIR / "03_projects_tools" / "write_logs.py"
MONITOR_EXE_PATH = BASE_DIR / "02_system_monitoring" / "health_checker.exe"

def trigger_database_log(status, action):
    """Dynamically loads the logging module to save data."""
    try:
        spec = importlib.util.spec_from_file_location("write_logs", str(LOG_MODULE_PATH))
        logger = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(logger)
        logger.save_log(status, action)
    except Exception as e:
        print(f"[Internal Error] Logging failed: {e}")

def execute_repair_sequence():
    """Simulates automated repair tasks."""
    print(">>> [INITIATING] Self-Healing Protocol...")
    print(">>> [ACTION] Flushing temporary buffers and restarting services...")
    print(">>> [SUCCESS] System stability has been restored.")
    return "Automated Cache Flush & Service Restart"

def monitor_system_health():
    """Orchestrates monitoring and repair."""
    if not os.path.exists(MONITOR_EXE_PATH):
        print(f"Error: Monitor binary (exe) not found at {MONITOR_EXE_PATH}")
        return

    # Run C++ tool
    print(f"Running Diagnostic Check: {MONITOR_EXE_PATH.name}")
    process = subprocess.run([str(MONITOR_EXE_PATH)], capture_output=True, text=True)
    diagnostic_result = process.stdout.strip()
    
    print(f"Diagnostic Output: {diagnostic_result}")

    # Decision Logic
    if "UNHEALTHY" in diagnostic_result:
        print("Alert: Critical RAM threshold reached.")
        resolution = execute_repair_sequence()
        trigger_database_log("CRITICAL (High RAM)", resolution)
    else:
        print("Status: System performing within optimal parameters.")
        trigger_database_log("STABLE", "No Action Required")