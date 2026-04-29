import csv
import os
from datetime import datetime

LOG_FILE = "sentinel_log.csv"

def log_event(ip, action,reason):
    file_exists = os.path.isfile(LOG_FILE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "IP_Address", "Action", "Reason"])
            writer.writerow([timestamp, ip, action, reason])
    except Exception as e:
        print(f"Error logging event: {e}")
        