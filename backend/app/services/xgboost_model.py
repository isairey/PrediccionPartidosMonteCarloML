import joblib

model = joblib.load(
    "app/models/football_model.pkl"
)

def predict_xg(features):

    result = model.predict(
        [features]
    )

    return float(result[0])