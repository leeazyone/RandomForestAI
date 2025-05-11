from flask import Flask
from routes.predict import predict_bp
from routes.log import log_bp
from routes.download_log import download_bp
import os

app = Flask(__name__)

#config.py 설정 불러오기
app.config.from_pyfile("config.py")

#업로드 폴더 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#라우트 등록 (Blueprint)
app.register_blueprint(predict_bp)
app.register_blueprint(log_bp)
app.register_blueprint(download_bp)

if __name__ == '__main__':
  app.run(debug=True)
