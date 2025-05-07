from flask import Blueprint

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=['GET'])
def hello():
  return {"message": "여긴 /predict API야. 아직은 테스트만 가능해!"}