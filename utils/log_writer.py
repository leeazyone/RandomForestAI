# utils/log_writer.py

import csv
import os
from datetime import datetime

def log_prediction(userId, filename, attack, risk_level, log_file="prediction_log.csv"):
    timestamp = datetime.now()

    log_exists = os.path.exists(log_file)
    with open(log_file, mode="a", encoding="utf-8") as logfile:
        writer = csv.writer(logfile)
        if not log_exists:
            writer.writerow(["timestamp", "userId", "filename", "attack", "risk_level"])
        writer.writerow([timestamp, userId, filename, attack, risk_level])
        print("[log_writer] 저장됨:", timestamp, userId, filename, attack, risk_level)
