from flask import Flask
from flask_cors import CORS     
from routes.predict import predict_bp
from routes.log import log_bp
import os



app = Flask(__name__)
CORS(app)                       

# config.py 설정 불러오기
app.config.from_pyfile("config.py")

# 업로드 폴더 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 라우트 등록 (Blueprint)
app.register_blueprint(predict_bp)
app.register_blueprint(log_bp)


print("✅ predict_bp:", predict_bp)

print(app.url_map)



if __name__ == '__main__':
  app.run(debug=True, port=5050, host='0.0.0.0')
