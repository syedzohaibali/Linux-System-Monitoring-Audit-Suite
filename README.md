# Linux System Monitoring & Audit Suite

A lightweight Python-based toolkit to monitor Linux system health, analyze logs, automate backups, and track user/process activity.

This project is a hands-on excercise to reinforce the git and python expertise required to be a good DevOps practioner.

## Features 

**System Health Monitor (monitor.py)** → Records CPU, memory, disk, and network usage.

**Log Analyzer (log_analyzer.py)** → Parses and summarizes system logs for errors, warnings, info, and failed login attempts.

**Backup Tool (backup.py)** → Automates backups with retention policy.

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
│   │   └── monitor.py             # (Task 1)
│   ├── log_analyzer/
│   │   └── log_analyzer.py        # (Task 2)
│   ├── backup/
│   │   └── backup.py              # (Task 3)
│   └── user_process_tracker/
│       └── user_process_tracker.py # (Task 4)
│
│── reports/
│   ├── monitor/
│   │   └── system_report.json     
│   └── logs/
│       └── log_summary.json      
│
│── logs/
│   ├── monitor.log
│   └── log_analyzer.log          
│
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


