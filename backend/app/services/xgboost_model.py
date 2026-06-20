import joblib
import numpy as np

model = joblib.load("app/models/football_model.pkl")


def predict_xg(features):

    # =========================
    # VALIDACIÓN
    # =========================
    if features is None:
        return 1.2

    try:
        features = np.array(features).reshape(1, -1)

        pred = model.predict(features)[0]

        # =========================
        # CLAMP (evita valores absurdos)
        # =========================
        pred = max(0.2, min(float(pred), 5.0))

        return pred

    except Exception as e:

        print("XG ERROR:", e)

        return 1.2