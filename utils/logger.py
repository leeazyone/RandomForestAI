#예측 결과를 CSV로 기록
import csv
from datetime import datetime

def log_prediction(filename, attack, level, log_file):
  with open(log_file, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([datetime.now(), filename, attack, level])

# anomaly는 이상탐지 모델로 하는 것이기 때문에 지금은 제거 
#def log_prediction(filename, attack, anomaly, level, log_file):
#with open(log_file, 'a', newline='') as csvfile:
#   writer = csv.writer(csvfile)
#   writer.writerow([datetime.now(), filename, attack, anomaly, level])