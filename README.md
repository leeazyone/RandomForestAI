# 🧠 AI 기반 Flask 백엔드 API 서버

이 프로젝트는 `.pcap` 파일을 업로드 받아 AI 모델로 분석한 뒤, 결과를 JSON으로 반환하는 Flask 기반 백엔드 서버입니다.

## 📁 프로젝트 구조

test/
├── app.py # 서버 실행 진입점
├── config.py # 설정 파일
├── requirements.txt # 패키지 목록
├── utils/ # 전처리 및 모델 관련 로직
│ ├── preprocess.py
│ ├── tshark_runner.py
│ ├── model_loader.py
│ ├── attack_info.py
│ └── logger.py
├── routes/ # API 라우팅 파일
│ ├── predict.py
│ └── log.py
└── uploads/ # 업로드된 파일 저장 폴더

## 🚀 실행 방법

1. 가상환경 설정 (선택)

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. 패키지 설치

   ```bash
   pip install -r requirements.txt
   ```

3. 서버 실행
   ```bash
   python app.py
   ```

---

## 🔌 API 엔드포인트

| Method | URL        | 설명                        |
| ------ | ---------- | --------------------------- |
| POST   | `/predict` | pcap 파일 분석 및 결과 반환 |
| GET    | `/log`     | 로그 조회 (JSON)            |

---

## 🧪 테스트

- Postman이나 Curl을 이용해 `.pcap` 파일을 `/predict`로 업로드
- `/log`에서 분석 내역 확인 가능

---

## 🌿 브랜치 전략

| 브랜치 이름  | 설명                                    |
| ------------ | --------------------------------------- |
| `main`       | 운영 및 배포용 (최종 안정 버전)         |
| `dev`        | 통합 개발 브랜치                        |
| `feature/*`  | 기능 개발용 (예: `feature/predict-api`) |
| `fix/*`      | 버그 수정용                             |
| `refactor/*` | 코드 리팩터링용                         |
