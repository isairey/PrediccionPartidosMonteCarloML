from app.services.team_stats import (
    search_team,
    get_last_matches,
    get_h2h,
    build_features
)

from app.services.xgboost_model import predict_xg
from app.services.montecarlo import simulate_scores


# =========================
# FALLBACK BASE (SELECCIONES)
# =========================
DEFAULT_XG = {
    "home": 1.4,
    "away": 1.2
}


def predict_match(home_team, away_team):

    # =========================
    # TEAMS
    # =========================
    home_id = search_team(home_team)
    away_id = search_team(away_team)

    if not home_id or not away_id:
        return {
            "error": "No se encontraron equipos",
            "home_team": home_team,
            "away_team": away_team
        }

    # =========================
    # MATCHES
    # =========================
    home_matches = get_last_matches(home_id, 20)
    away_matches = get_last_matches(away_id, 20)

    # =========================
    # FEATURES
    # =========================
    home_features = build_features(home_matches, home_id)
    away_features = build_features(away_matches, away_id)

    # fallback seguro
    if not home_features:
        home_features = [1.5, 1.2, 0.5, 0.5]

    if not away_features:
        away_features = [1.3, 1.4, 0.5, 0.5]

    # =========================
    # XGBOOST (o fallback)
    # =========================
    try:
        home_xg = float(predict_xg(home_features))
        away_xg = float(predict_xg(away_features))

    except Exception:
        home_xg = DEFAULT_XG["home"]
        away_xg = DEFAULT_XG["away"]

    # =========================
    # HOME ADVANTAGE (IMPORTANTE EN SELECCIONES)
    # =========================
    home_xg += 0.15

    # =========================
    # HEAD TO HEAD (suave, no dominante)
    # =========================
    h2h = get_h2h(home_id, away_id)

    if h2h and len(h2h) > 0:

        hg = sum((m["goals"]["home"] or 0) for m in h2h) / len(h2h)
        ag = sum((m["goals"]["away"] or 0) for m in h2h) / len(h2h)

        home_xg = (home_xg * 0.85) + (hg * 0.15)
        away_xg = (away_xg * 0.85) + (ag * 0.15)

    # =========================
    # LIMITADORES (IMPORTANTE)
    # =========================
    home_xg = max(0.2, min(home_xg, 4.5))
    away_xg = max(0.2, min(away_xg, 4.5))

    # =========================
    # MONTE CARLO
    # =========================
    top_scores = simulate_scores(
        home_xg,
        away_xg,
        simulations=50000  # 🔥 más estable que 200k
    )

    # =========================
    # RESPONSE
    # =========================
    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "predicted_score": top_scores[0]["score"],
        "top_scores": top_scores
    }