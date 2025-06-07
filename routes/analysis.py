# routes/analysis.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import csv
import os

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/api/analysis/save", methods=["POST"])
@jwt_required()
def save_analysis():
    user_id = get_jwt_identity()
    data = request.get_json()
    filename = data.get("filename")
    result = data.get("result")

    if not filename or not result:
        return jsonify({"error": "filename 또는 result가 누락되었습니다."}), 400

    # ✅ 로그 저장 로직 제거
    return jsonify({
        "message": "저장 완료 (실제 저장은 생략됨)",
        "data": {
            "userId": user_id,
            "filename": filename,
            "attack": result.get("attack"),
            "risk_level": result.get("risk_level"),
            "createdAt": datetime.now().isoformat()
        }
    }), 200
