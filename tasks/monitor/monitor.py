# monitor.py
# Task 1: System Health Monitor
# - Collects CPU, memory, disk, and network stats
# - Saves results into pretty JSON
# - Logs each run into logs/monitor.log
# - Auto-commits & pushes updates to GitHub only once per day

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
    # Load existing data if available
    if os.path.isfile(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
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


# --- Git automation (once per day) ---
def git_commit_and_push():
    now = datetime.now()
    # Only commit near midnight (00:00 ± 5 minutes)
    if now.hour == 0 and 45 <= now.minute < 60:
        try:
            # 1. Sync with remote (autostash avoids unstaged changes)
            subprocess.run(
                ["git", "pull", "--rebase", "--autostash", "origin", "main"],
                check=True
            )

            # 2. Stage the JSON file
            subprocess.run(["git", "add", JSON_FILE], check=True)

            # 3. Commit with date stamp
            commit_message = f"Daily system report {now.strftime('%Y-%m-%d')}"
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=False, capture_output=True, text=True
            )

            # Skip push if nothing new
            if "nothing to commit" in commit_result.stdout.lower():
                logging.info("ℹ️ No changes detected, skipping push.")
                return

            # 4. Push
            subprocess.run(["git", "push", "origin", "main"], check=True)
            logging.info("✅ Daily report committed and pushed to GitHub.")

        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Git command failed: {e}")
        except Exception as e:
            logging.error(f"❌ Unexpected error in git_commit_and_push: {e}")
    else:
        logging.info("ℹ️ Skipping commit — not scheduled time yet.")


# --- Main function ---
def main():
    stats = collect_stats()
    save_to_json(stats)
    msg = f"System stats recorded: {stats}"
    print("✅", msg)
    logging.info(msg)

    # Commit/push only if time condition matches
    git_commit_and_push()


if __name__ == "__main__":
    main()

