import pandas as pd
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# =========================
# DATASET
# =========================

df = pd.read_csv(
    "datasets/matches.csv"
)

# =========================
# FEATURES
# =========================

X = df[
    [
        "avg_gf",
        "avg_ga",
        "win_rate",
        "form",
        "home_avg",
        "away_avg"
    ]
]

# goles reales

y = df["goals_scored"]

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# XGBOOST
# =========================

model = XGBRegressor(

    n_estimators=500,

    max_depth=6,

    learning_rate=0.03,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42
)

model.fit(
    X_train,
    y_train
)

# =========================
# EVALUACIÓN
# =========================

preds = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    preds
)

print(
    f"MAE: {mae:.3f}"
)

# =========================
# GUARDAR
# =========================

joblib.dump(
    model,
    "app/models/football_model.pkl"
)

print(
    "Modelo guardado correctamente"
)