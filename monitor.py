# monitor.py
# Task 1: System Health Monitor
# - Collects CPU, memory, disk, and network stats
# - Saves results into pretty JSON (easy to read)
# - Logs each run into logs/monitor.log
# - Auto-commits & pushes reports to GitHub

import psutil
import json
import os
import logging
import subprocess
from datetime import datetime

# --- Setup logging ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/monitor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- File paths ---
os.makedirs("reports/monitor", exist_ok=True)
JSON_FILE = "reports/monitor/system_report.json"

# --- Collect system stats ---
def collect_stats():
    """Collect system statistics using psutil."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "net_bytes_sent": psutil.net_io_counters().bytes_sent,
        "net_bytes_recv": psutil.net_io_counters().bytes_recv,
    }

# --- Save to pretty JSON ---
def save_to_json(data):
    # Load old data if file exists
    if os.path.isfile(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    # Append new record
    all_data.append(data)

    # Save back with indentation
    with open(JSON_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

# --- Git automation ---
def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "reports/monitor/"], check=True)
        commit_message = f"Update system report {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        logging.info("✅ Reports committed and pushed to GitHub.")
    except Exception as e:
        logging.error(f"❌ Git commit/push failed: {e}")

# --- Main function ---
def main():
    stats = collect_stats()
    save_to_json(stats)
    msg = f"System stats recorded: {stats}"
    print("✅", msg)
    logging.info(msg)

    # Auto commit & push
    git_commit_and_push()

if __name__ == "__main__":
    main()

