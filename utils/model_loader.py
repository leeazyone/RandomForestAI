import joblib

#공격 분류 모델(RandomForest)
rf_model, feature_names = joblib.load("rf_model.joblib")

#이상 감지 모델(IsolationForest)
#iso_model = joblib.load("iso_model.joblib")

#if __name__ == "__main__":
# print("RandomForest 모델 클래스 목록:", rf_model.classes_)
# print("Feature 개수:", len(feature_names))