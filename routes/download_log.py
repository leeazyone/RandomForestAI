# routes/download_log.py

from flask import Blueprint, request, send_file, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.tshark_runner import run_tshark
import os
import traceback

download_bp = Blueprint("download", __name__)

@download_bp.route("/download/<filename>", methods=["GET"])
@jwt_required()
def download_csv(filename):
    try:
        user_id = get_jwt_identity()
        print(f"[DOWNLOAD] 요청한 사용자: {user_id}, 파일: {filename}")

        # 원본 pcap 경로
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        pcap_path = os.path.join(upload_folder, filename)

        # 변환될 csv 경로
        csv_path = pcap_path + ".csv"

        if not os.path.exists(pcap_path):
            return jsonify({"error": f"{filename} 파일이 존재하지 않습니다."}), 404

        # Tshark 실행 (기존 파일이 있다면 덮어쓰기)
        run_tshark(pcap_path, csv_path)

        if not os.path.exists(csv_path):
            return jsonify({"error": "CSV 파일 생성 실패"}), 500

        return send_file(
            csv_path,
            as_attachment=True,
            download_name=f"{filename}.csv",
            mimetype="text/csv"
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
