#Linux System Monitoring & Audit Suite

A lightweight Python-based toolkit to monitor Linux system health, analyze logs, automate backups, and track user/process activity.

This project is a hands-on excercise to reinforce the git and python expertise required to be a good DevOps practioner.

#Features (Planned & Implemented)

**System Health Monitor (monitor.py)** → Records CPU, memory, disk, and network usage.

**Log Analyzer (log_analyzer.py)** → Parses and summarizes system logs.

**Backup Tool (backup.py)** → Automates backups with retention policy.

**User & Process Tracker (user_process_tracker.py)** → Tracks login sessions and anomalies.

 **Git Pre-Commit Hook** → Ensures code quality and security checks.

##Installation

 1) Clone the repository:

git clone https://github.com/syedzohaibali/Linux-System-Monitoring-Audit-Suite.git
cd Linux-System-Monitoring-Audit-Suite


 2) Create and activate a virtual environment (Recommended):

python3 -m venv .venv
source .venv/bin/activate


 3) Install dependencies:

pip install -r requirements.txt

##Project Structure
Linux-System-Monitoring-Audit-Suite/
│── tasks/
│   ├── monitor/
│   │   └── monitor.py
│   ├── log_analyzer/
│   │   └── log_analyzer.py        # (to be added in Task 2)
│   ├── backup/
│   │   └── backup.py              # (placeholder)
│   └── user_process_tracker/
│       └── user_process_tracker.py # (placeholder)
│
│── reports/
│   ├── monitor/
│   │   └── system_report.json
│   └── logs/
│       └── log_summary.json       # (Task 2 output)
│
│── logs/
│   ├── monitor.log
│   └── log_analyzer.log           # (Task 2)
│
│── config/
│── hooks/
│── requirements.txt
│── README.md
│── .gitignore

Usage — Task 1: System Health Monitor

Run manually from the repo root:

# activate venv (recommended)
source .venv/bin/activate

# run the monitor
python3 tasks/monitor/monitor.py

Outputs

 Pretty JSON (grows over time): reports/monitor/system_report.json

 Logs: logs/monitor.log

Automation with CRON:
 This runs the monitor every 5 minutes and logs output:

*/5 * * * * cd /home/Linux_System_Monitoring_And_Audit_Suite && /home/Linux_System_Monitoring_And_Audit_Suite/.venv/bin/python /home/Linux_System_Monitoring_And_Audit_Suite/tasks/monitor/monitor.py >> /home/Linux_System_Monitoring_And_Audit_Suite/logs/monitor_cron.log 2>&1


Note: The script commits & pushes once per day (between 00:00–00:04).


Progress Tracking

 Task 1: System Health Monitor

 Task 2: Log Analyzer

 Task 3: Backup Tool

 Task 4: User & Process Tracker

 Task 5: Git Pre-Commit Hook
