from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_pymongo import PyMongo
from routes.predict import predict_bp
from routes.log import log_bp
from routes.download_log import download_bp
from routes.analysis import analysis_bp
import os

app = Flask(__name__)

#config.py 설정 불러오기
app.config.from_pyfile("config.py")

CORS(app, resources={r"/*": {"origins": "*"}})

jwt = JWTManager(app)

# 4) PyMongo 초기화 (config.py 에 정의된 MONGO_URI 사용)
mongo = PyMongo(app)   # => 이제 app.config['MONGO_URI']를 통해 DB에 접근 가능

#업로드 폴더 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#라우트 등록 (Blueprint)
app.register_blueprint(predict_bp)
app.register_blueprint(log_bp)
app.register_blueprint(download_bp)
app.register_blueprint(analysis_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5050, host='0.0.0.0')
