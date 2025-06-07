from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import csv
import os
import traceback

from utils.preprocess import preprocess_csv
from utils.model_loader import rf_model, feature_names
from utils.attack_info import attack_explanations, attack_feature_map
from utils.model_fixer import fix_prediction

log_bp = Blueprint("log", __name__)

@log_bp.route("/log", methods=["GET"])
def hello_log():
    return {"message": "여긴 /log API야. 곧 로그가 출력될거야"}

@log_bp.route("/logs-json", methods=["GET"])
@jwt_required()
def get_log():
    current_userId = get_jwt_identity()
    print("현재 로그인된 userId:", current_userId)

    log_file = current_app.config.get("LOG_FILE", "prediction_log.csv")

    if not os.path.exists(log_file):
        return jsonify({"message": "예측 로그 파일이 없습니다."}), 404

    filtered_logs = []

    with open(log_file, newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_user_id = row.get("userId", "").strip()
            if row_user_id == current_userId:
                filtered_logs.append({
                    "timestamp": row.get("timestamp", ""),
                    "filename": row.get("filename", ""),
                    "attack": row.get("attack", ""),
                    "risk_level": row.get("risk_level", "")
                })

    print(f"필터링된 로그 수: {len(filtered_logs)}")
    return jsonify(filtered_logs)

# ✅ 분석 결과 그래프 상세 보기
@log_bp.route("/graph-detail", methods=['GET'])
def graph_detail():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "filename 파라미터가 필요합니다."}), 400

    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename + '.csv')
        if not os.path.exists(csv_path):
            return jsonify({'error': f"{filename}.csv 파일이 존재하지 않습니다."}), 404

        summary = preprocess_csv(csv_path)
        X = summary[feature_names]

        attack = rf_model.predict(X)[0]
        attack = fix_prediction(attack, summary)
        info = attack_explanations.get(attack, {"desc": "알 수 없는 공격", "level": "알 수 없음"})

        normal_avg = {
            "packet_count": 300.0,
            "mean_ip_len": 350.0,
            "std_ip_len": 100.0,
            "icmp_type_8_ratio": 0.01,
            "udp_port_variety": 3.0,
            "mean_udp_len": 80.0,
            "syn_count": 5.0,
            "tcp_port_variety": 8.0,
            "tcp_seq_var": 5000.0,
            "arp_reply_ratio": 0.01,
            "arp_src_ip_unique": 1.0
        }

        current_values = summary.iloc[0].to_dict()
        selected_features = attack_feature_map.get(attack, feature_names[:5])
        feature_comparison = {
            name: {
                "current": round(current_values.get(name, 0), 3),
                "normal_avg": round(normal_avg.get(name, 0), 3)
            }
            for name in selected_features if name in current_values
        }

        importances = rf_model.feature_importances_
        important_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:5]
        feature_importance = {name: round(score, 4) for name, score in important_features}

        return jsonify({
            "filename": filename,
            "attack": attack,
            "description": info["desc"],
            "risk_level": info["level"],
            "feature_comparison": feature_comparison,
            "feature_importance": feature_importance
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
