#예측 결과를 CSV로 기록
import csv
from datetime import datetime

def log_prediction(filename, attack, anomaly, level, log_file):
  with open(log_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([datetime.now(), filename, attack, anomaly, level])