from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from utils.preprocess import preprocess_csv
from utils.tshark_runner import run_tshark
from utils.model_loader import rf_model, feature_names #,iso_model
from utils.attack_info import attack_explanations
from utils.logger import log_prediction
import traceback


predict_bp = Blueprint("predict", __name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() == 'pcap'

@predict_bp.route("/predict", methods=['POST'])
def hello():
  if 'file' not in request.files:
    return jsonify({'error': '파일이 없습니다'}),400
  
  file = request.files['file']
  if file.filename == '' or not allowed_file(file.filename):
    return jsonify({'error': '올바르지 않는 파일 형식입니다.'}),400
  
  try:
    filename = secure_filename(file.filename)
    pcap_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    csv_path = pcap_path+".csv"
    file.save(pcap_path)

    run_tshark(pcap_path, csv_path)
    summary = preprocess_csv(csv_path)

    X = summary[feature_names]

    attack = rf_model.predict(X)[0]
    #anomaly = iso_model.predict(summary)[0] 이상탐지 모델로 분석

    info = attack_explanations.get(attack, {"desc":"알 수 없는 공격", "level":"알 수 없음"})
    desc = info['desc']
    level = info['level']
    
    #print("✅ 전처리 결과:", summary)
    #print("✅ 예측 결과:", attack)
    #print("✅ 설명 딕셔너리 결과:", info)

    log_prediction(filename, attack,level,current_app.config['LOG_FILE'])
    
    return jsonify({
      "attack": attack,
      "description": desc,
      "risk_level":level,
    })

  except Exception as e:
    # 터미널에 오류 띄우기
    traceback.print_exc()
    return jsonify({'error': str(e)}),500