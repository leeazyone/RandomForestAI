# utils/logger.py

import os
import csv
from datetime import datetime

def log_prediction(userId, filename, attack, risk_level, log_file):
    file_exists = os.path.exists(log_file)

    with open(log_file, mode="a", newline="\n", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "userId", "filename", "attack", "risk_level"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        writer.writerow([timestamp, userId, filename, attack, risk_level])
