import pandas as pd
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# =========================
# DATASET
# =========================

df = pd.read_csv(
    "datasets/national_matches.csv"
)

print(
    f"Registros encontrados: {len(df)}"
)

# =========================
# FEATURES
# =========================

X = df[
    [
        "avg_gf",
        "avg_ga",
        "win_rate",
        "form"
    ]
]

# Objetivo
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
# MODELO XGBOOST
# =========================

model = XGBRegressor(

    n_estimators=1000,

    max_depth=8,

    learning_rate=0.02,

    subsample=0.9,

    colsample_bytree=0.9,

    objective="reg:squarederror",

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
# GUARDAR MODELO
# =========================

joblib.dump(
    model,
    "app/models/football_model.pkl"
)

print(
    "Modelo guardado correctamente"
)