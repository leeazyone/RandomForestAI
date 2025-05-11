from flask import Blueprint, send_file, jsonify
import os

download_bp = Blueprint("download", __name__)

# 로그 파일 경로 설정 (필요 시 config에서 import해도 됨)
LOG_FILE_PATH = os.path.join(os.getcwd(), "prediction_log.csv")

@download_bp.route("/download-log", methods=["GET"])
def download_log():
    if not os.path.exists(LOG_FILE_PATH):
        return jsonify({"error": "로그 파일이 존재하지 않습니다."}), 404

    return send_file(
        LOG_FILE_PATH,
        as_attachment=True,
        mimetype="text/csv",
        download_name="prediction_log.csv"
    )
