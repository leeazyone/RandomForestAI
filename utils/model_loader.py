import joblib

#공격 분류 모델(RandomForest)
rf_model, feature_names = joblib.load("rm_model.joblib")

#이상 감지 모델(IsolationForest)
#iso_model = joblib.load("iso_model.joblib")