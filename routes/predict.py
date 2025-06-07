# routes/predict.py

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
import traceback

from utils.preprocess import preprocess_csv
from utils.tshark_runner import run_tshark
from utils.model_loader import rf_model, feature_names
from utils.attack_info import attack_explanations
from utils.log_writer import log_prediction
from utils.model_fixer import fix_prediction

predict_bp = Blueprint("predict", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pcap"

@predict_bp.route("/predict", methods=["POST"])
@jwt_required()  # JWT 인증이 필요한 엔드포인트
def hello():
    # 1) JWT에서 current_userId 꺼내기
    userId = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "파일이 없습니다"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "올바르지 않는 파일 형식입니다."}), 400

    try:
        # 2) 파일 저장
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        pcap_path = os.path.join(upload_folder, filename)
        csv_path = pcap_path + ".csv"
        file.save(pcap_path)

        # 3) tshark로 CSV 변환
        run_tshark(pcap_path, csv_path)

        # 4) CSV 전처리 → 피처(feature) 추출
        summary = preprocess_csv(csv_path)
        X = summary[feature_names]

        # 5) RandomForest 예측
        attack = rf_model.predict(X)[0]
        # Optional: 이상탐지 모델 예측 (iso_model 등을 추가했다면)
        # anomaly = iso_model.predict(summary)[0]

        # 6) 오탐 보정
        attack = fix_prediction(attack, summary)

        # 7) 공격 설명, 위험도 가져오기
        info = attack_explanations.get(attack, {"desc": "알 수 없는 공격", "level": "알 수 없음"})
        desc = info["desc"]
        level = info["level"]

        # 8) *로그 저장* → userId, filename, attack, level을 기록
        print(f"[DEBUG] log_prediction 호출됨 - userId: {userId}, filename: {filename}, attack: {attack}, risk_level: {level}")
        log_prediction(
            userId=userId,
            filename=filename,
            attack=attack,
            risk_level=level,
            log_file=current_app.config["LOG_FILE"]
        )

        # 9) JSON으로 결과 반환
        return jsonify({
            "attack": attack,
            "description": desc,
            "risk_level": level
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
