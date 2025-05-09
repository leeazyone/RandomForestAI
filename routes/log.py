from flask import Blueprint, jsonify, current_app
import csv
import os

log_bp = Blueprint('log', __name__)

@log_bp.route("/log", methods=["GET"])
def get_log():
  log_file = current_app.config['LOG_FILE']

  if not os.path.exists(log_file):
    return jsonify({"message":"예측 로그가 없습니다."}), 200
  
  log_data=[]
  with open(log_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      log_data.append({
        "timestamp": row[0],
        "filename": row[1],
        "attack": row[2],
        "risk_level": row[3]
      })

  return jsonify(log_data)