import os
import tarfile
import subprocess
from datetime import datetime

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports", "backup")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

BACKUP_LOG = os.path.join(LOGS_DIR, "backup.log")

# Directories to back up (critical project dirs)
CRITICAL_DIRS = [
    os.path.join(BASE_DIR, "tasks"),
    os.path.join(BASE_DIR, "reports"),
    os.path.join(BASE_DIR, "logs"),
    os.path.join(BASE_DIR, "config"),
]

# Keep only the last 3 backups
RETENTION_COUNT = 3


def create_backup():
    """Create a compressed backup of critical directories."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(REPORTS_DIR, f"backup_{now}.tar.gz")

    try:
        with tarfile.open(backup_file, "w:gz") as tar:
            for directory in CRITICAL_DIRS:
                if os.path.exists(directory):
                    tar.add(directory, arcname=os.path.basename(directory))
        log(f"✅ Created backup: {backup_file}")
        return backup_file
    except Exception as e:
        log(f"❌ Backup failed: {e}")
        return None


def rotate_backups():
    """Keep only the last RETENTION_COUNT backups, delete older ones."""
    try:
        backups = sorted(
            [f for f in os.listdir(REPORTS_DIR) if f.startswith("backup_")],
            key=lambda x: os.path.getctime(os.path.join(REPORTS_DIR, x))
        )

        while len(backups) > RETENTION_COUNT:
            old_backup = backups.pop(0)
            os.remove(os.path.join(REPORTS_DIR, old_backup))
            log(f"🗑️ Deleted old backup: {old_backup}")

    except Exception as e:
        log(f"❌ Rotation failed: {e}")


def git_commit_and_push():
    """Commit and push backups once per day at ~3:00 AM."""
    now = datetime.now()
    if now.hour == 3 and 0 <= now.minute < 5:  # commit window 03:00–03:04
        try:
            repo_path = BASE_DIR

            subprocess.run(
                ["git", "pull", "--rebase", "--autostash", "origin", "main"],
                check=True, cwd=repo_path
            )

            subprocess.run(["git", "add", REPORTS_DIR], check=True, cwd=repo_path)

            commit_message = f"Daily backup {now.strftime('%Y-%m-%d')}"
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path, capture_output=True, text=True
            )

            if "nothing to commit" in commit_result.stdout.lower():
                log("ℹ️ No new backup to commit.")
                return

            subprocess.run(["git", "push", "origin", "main"], check=True, cwd=repo_path)
            log("✅ Daily backup committed and pushed to GitHub.")

        except Exception as e:
            log(f"❌ Git commit/push failed: {e}")
    else:
        log("⏭️ Skipping commit — not scheduled time.")


def log(message):
    """Log messages to backup.log."""
    with open(BACKUP_LOG, "a") as logf:
        logf.write(f"[{datetime.now()}] {message}\n")
    print(message)


if __name__ == "__main__":
    backup_file = create_backup()
    if backup_file:
        rotate_backups()
    git_commit_and_push()

