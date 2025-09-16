import os
import re
import json
from datetime import datetime
from collections import Counter

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "log_analyzer")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(REPORTS_DIR, "log_summary.json")
ANALYZER_LOG = os.path.join(LOGS_DIR, "log_analyzer.log")

def analyze_logs():
    summary = {
        "timestamp": datetime.now().isoformat(),
        "error_count": 0,
        "warning_count": 0,
        "info_count": 0,
        "failed_logins": 0,
        "top_messages": []
    }

    log_files = ["/var/log/syslog", "/var/log/auth.log"]
    messages = []

    for log_file in log_files:
        if not os.path.exists(log_file):
            continue
        try:
            with open(log_file, "r", errors="ignore") as f:
                for line in f:
                    l = line.lower()
                    if "error" in l:
                        summary["error_count"] += 1
                        messages.append(line.strip())
                    elif "warning" in l:
                        summary["warning_count"] += 1
                        messages.append(line.strip())
                    elif "info" in l:
                        summary["info_count"] += 1
                        messages.append(line.strip())

                    if "failed password" in l:
                        summary["failed_logins"] += 1
        except Exception as e:
            with open(ANALYZER_LOG, "a") as logf:
                logf.write(f"[{datetime.now()}] ERROR reading {log_file}: {e}\n")

    # Top 5 frequent messages
    counter = Counter(messages)
    summary["top_messages"] = counter.most_common(5)

    return summary

def save_report(summary):
    try:
        # Save as a growing JSON list
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(summary)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=4)

        with open(ANALYZER_LOG, "a") as logf:
            logf.write(f"[{datetime.now()}] Saved summary to {OUTPUT_FILE}\n")
    except Exception as e:
        with open(ANALYZER_LOG, "a") as logf:
            logf.write(f"[{datetime.now()}] ERROR saving report: {e}\n")

if __name__ == "__main__":
    summary = analyze_logs()
    print(json.dumps(summary, indent=4))  # Show in terminal
    save_report(summary)

