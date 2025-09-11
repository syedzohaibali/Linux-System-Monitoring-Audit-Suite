#!/usr/bin/env python3
"""
System Health Monitor
---------------------
Collects CPU, memory, disk, and network statistics,
and writes them into JSONL and CSV files.

Outputs:
- reports/monitor/system_report.jsonl  (append-only log in JSON lines format)
- reports/monitor/system_report.csv    (append-only log in CSV format)
"""

import psutil
import json
import csv
from datetime import datetime
from pathlib import Path

# Paths
REPORT_DIR = Path("reports/monitor")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
JSONL_FILE = REPORT_DIR / "system_report.jsonl"
CSV_FILE = REPORT_DIR / "system_report.csv"

def collect_stats():
    """Collect CPU, memory, disk, and network usage."""
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "net_bytes_sent": psutil.net_io_counters().bytes_sent,
        "net_bytes_recv": psutil.net_io_counters().bytes_recv,
    }
    return stats

def write_jsonl(data):
    """Append a record to JSONL file."""
    with open(JSONL_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")

def write_csv(data):
    """Append a record to CSV file (write header if file is new)."""
    file_exists = CSV_FILE.exists()
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def main():
    stats = collect_stats()
    write_jsonl(stats)
    write_csv(stats)
    print("✅ System stats recorded:", stats)

if __name__ == "__main__":
    main()

