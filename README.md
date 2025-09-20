# Linux System Monitoring & Audit Suite

A lightweight Python-based toolkit to monitor Linux system health, analyze logs, automate backups, and track user/process activity.

This project is a hands-on excercise to reinforce the git and python expertise required to be a good DevOps practioner.

## Features 

**System Health Monitor (monitor.py)** → Records CPU, memory, disk, and network usage.

**Log Analyzer (log_analyzer.py)** → Parses and summarizes system logs for errors, warnings, info, and failed login attempts.

**Backup Tool (backup.py)** → Created and automates backups while keeping the recent 3 tar.gz backups ONLY (and deleting the older backups)

**User & Process Tracker (user_process_tracker.py)** → Tracks login sessions and anomalies.

**Git Pre-Commit Hook** → Ensures code quality and security checks.

## Installation

 1) Clone the repository:
git clone <repo-url>
cd Linux-System-Monitoring-Audit-Suite

 2) Create and activate a virtual environment (Recommended):

python3 -m venv .venv
source .venv/bin/activate

 3) Install dependencies:

pip install -r requirements.txt

## Project Structure
```
Linux-System-Monitoring-Audit-Suite/
│── tasks/
│   ├── monitor/
│   │   └── monitor.py              # (Task 1: System Health Monitor)
│   ├── log_analyzer/
│   │   └── log_analyzer.py         # (Task 2: Log Analyzer)
│   ├── backup/
│   │   └── backup.py               # (Task 3: Automated Backup System)
│   └── user_process_tracker/
│       └── user_process_tracker.py # (Task 4: User & Process Tracker)
│
│── reports/
│   ├── monitor/
│   │   └── system_report.json      # Task 1 output
│   ├── log_analyzer/
│   │   └── log_summary.json        # Task 2 output
│   └── backup/
│       ├── backup_2025-09-20_16-40-59.tar.gz
│       ├── backup_2025-09-20_16-41-02.tar.gz
│       └── backup_2025-09-20_16-41-08.tar.gz   # Task 3 backups (rotated, last 3 kept)
│
│── logs/
│── config/
│── hooks/
│── requirements.txt
│── README.md
│── .gitignore
```

##Usage
**Task 1: System Health Monitor**

Run manually:
source .venv/bin/activate

python3 tasks/monitor/monitor.py

**_Outputs_**

JSON Report: reports/monitor/system_report.json

Logs: logs/monitor.log


**Task 2: Log Anlyzer**

Run Manually:
source .venv/bin/activate

python3 tasks/log_analyzer/log_analyzer.py

**_Outputs_**
JSON report: reports/log_analyzer/log_summary.json

Logs: logs/log_analyzer.log

**Task3: Automated BAckups**
Compressed backups → reports/backup/backup_<timestamp>.tar.gz
Logs: logs/backup.log
