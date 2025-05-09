#허용된 업로드 파일 확장자
ALLOWED_EXTENSIONS = {'pcap'}

#업로드된 파일 저장 폴더
UPLOAD_FOLDER = './uploads'

#파일 크기 제한: 50MB
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

#예측 로그 파일 저장 경로
LOG_FILE = './prediction_log.csv'