from flask import Blueprint

log_bp = Blueprint('log', __name__)

@log_bp.route("/log", methods=["GET"])
def hello_log():
  return {"message": "여긴 /log API야. 곧 로그가 여ddddd기에 출력될거야"}