import os
import re
import json
import subprocess
from datetime import datetime

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "log_analyzer")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(REPORTS_DIR, "log_summary.json")
ANALYZER_LOG = os.path.join(LOGS_DIR, "log_analyzer.log")

# --- Patterns ---
FAILED_LOGIN_PATTERNS = [
    r"failed password",
    r"authentication failure",
    r"FAILED su",
    r"invalid user",
]

def analyze_logs():
    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_count": 0,
        "warning_count": 0,
        "info_count": 0,
        "failed_logins": 0,
        "top_messages": []
    }

    # Only parse user-accessible logs (no root required)
    log_files = [
        os.path.join(LOGS_DIR, "monitor.log"),
        os.path.join(LOGS_DIR, "log_analyzer.log"),
    ]

    messages = []

    for log_file in log_files:
        if not os.path.exists(log_file):
            with open(ANALYZER_LOG, "a") as logf:
                logf.write(f"[{datetime.now()}] Skipping missing log: {log_file}\n")
            continue

        try:
            with open(log_file, "r", errors="ignore") as f:
                for line in f:
                    lower = line.lower()

                    if "error" in lower:
                        summary["error_count"] += 1
                        messages.append(line.strip())
                    elif "warning" in lower:
                        summary["warning_count"] += 1
                        messages.append(line.strip())
                    elif "info" in lower:
                        summary["info_count"] += 1

                    for pattern in FAILED_LOGIN_PATTERNS:
                        if re.search(pattern, lower):
                            summary["failed_logins"] += 1
                            messages.append(line.strip())
                            break
        except Exception as e:
            with open(ANALYZER_LOG, "a") as logf:
                logf.write(f"[{datetime.now()}] ERROR reading {log_file}: {e}\n")

    # Top 5 frequent messages
    summary["top_messages"] = messages[:5]
    return summary


def save_report(summary):
    try:
        with open(OUTPUT_FILE, "a") as f:  # append new entries
            f.write(json.dumps(summary, indent=4) + "\n")
        with open(ANALYZER_LOG, "a") as logf:
            logf.write(f"[{datetime.now()}] Saved summary to {OUTPUT_FILE}\n")
    except Exception as e:
        with open(ANALYZER_LOG, "a") as logf:
            logf.write(f"[{datetime.now()}] ERROR saving report: {e}\n")


def git_commit_and_push():
    now = datetime.now()
    # Only commit between 02:05 and 02:09 AM
    if now.hour == 2 and 5 <= now.minute < 10:
        try:
            repo_path = BASE_DIR

            # Sync with remote
            subprocess.run(
                ["git", "pull", "--rebase", "--autostash", "origin", "main"],
                check=True, cwd=repo_path
            )

            # Stage only log analyzer report
            subprocess.run(["git", "add", OUTPUT_FILE], check=True, cwd=repo_path)

            # Commit
            commit_message = f"Daily log analyzer report {now.strftime('%Y-%m-%d')}"
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path, capture_output=True, text=True
            )

            if "nothing to commit" in commit_result.stdout.lower():
                with open(ANALYZER_LOG, "a") as logf:
                    logf.write(f"[{datetime.now()}] No changes to commit.\n")
                return

            # Push
            subprocess.run(["git", "push", "origin", "main"], check=True, cwd=repo_path)

            with open(ANALYZER_LOG, "a") as logf:
                logf.write(f"[{datetime.now()}] ✅ Daily report committed and pushed.\n")

        except Exception as e:
            with open(ANALYZER_LOG, "a") as logf:
                logf.write(f"[{datetime.now()}] Git commit/push failed: {e}\n")
    else:
        with open(ANALYZER_LOG, "a") as logf:
            logf.write(f"[{datetime.now()}] Skipping commit — not scheduled time.\n")


if __name__ == "__main__":
    summary = analyze_logs()
    print(json.dumps(summary, indent=4))
    save_report(summary)
    git_commit_and_push()

