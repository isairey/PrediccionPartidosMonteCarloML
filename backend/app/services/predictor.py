from app.services.team_stats import (
    search_team,
    get_last_matches,
    get_h2h,
    build_features
)

from app.services.xgboost_model import (
    predict_xg
)

from app.services.montecarlo import (
    simulate_scores
)


def predict_match(
    home_team,
    away_team
):

    home_id = search_team(
        home_team
    )

    away_id = search_team(
        away_team
    )

    if not home_id:

        return {
            "error":
            f"No se encontró {home_team}"
        }

    if not away_id:

        return {
            "error":
            f"No se encontró {away_team}"
        }

    # =====================
    # PARTIDOS RECIENTES
    # =====================

    home_matches = get_last_matches(
        home_id,
        20
    )

    away_matches = get_last_matches(
        away_id,
        20
    )

    h2h_matches = get_h2h(
        home_id,
        away_id
    )

    # =====================
    # FEATURES
    # =====================

    home_stats = build_features(
        home_matches,
        home_id
    )

    away_stats = build_features(
        away_matches,
        away_id
    )

    # =====================
    # XGBOOST
    # =====================

    try:

        home_features = [

            home_stats["avg_gf"],
            home_stats["avg_ga"],
            home_stats["win_rate"],
            home_stats["form"],
            home_stats["home_avg"],
            home_stats["away_avg"]
        ]

        away_features = [

            away_stats["avg_gf"],
            away_stats["avg_ga"],
            away_stats["win_rate"],
            away_stats["form"],
            away_stats["home_avg"],
            away_stats["away_avg"]
        ]

        home_xg = predict_xg(
            home_features
        )

        away_xg = predict_xg(
            away_features
        )

    except:

        home_xg = (
            home_stats["avg_gf"] * 0.70
            +
            away_stats["avg_ga"] * 0.30
        )

        away_xg = (
            away_stats["avg_gf"] * 0.70
            +
            home_stats["avg_ga"] * 0.30
        )

    # =====================
    # FORMA RECIENTE
    # =====================

    home_xg += (
        home_stats["form"] * 0.25
    )

    away_xg += (
        away_stats["form"] * 0.25
    )

    # =====================
    # LOCAL / VISITANTE
    # =====================

    home_xg = (
        home_xg * 0.80
        +
        home_stats["home_avg"] * 0.20
    )

    away_xg = (
        away_xg * 0.80
        +
        away_stats["away_avg"] * 0.20
    )

    # =====================
    # H2H
    # =====================

    home_h2h = 0
    away_h2h = 0

    for match in h2h_matches:

        try:

            hg = match["goals"]["home"]
            ag = match["goals"]["away"]

            if hg > ag:

                home_h2h += 1

            elif ag > hg:

                away_h2h += 1

        except:
            pass

    total_h2h = (
        home_h2h +
        away_h2h
    )

    if total_h2h > 0:

        factor = (
            home_h2h -
            away_h2h
        ) / total_h2h

        home_xg += (
            factor * 0.35
        )

        away_xg -= (
            factor * 0.35
        )

    # =====================
    # VENTAJA LOCAL
    # =====================

    home_xg *= 1.10

    # =====================
    # LIMITES
    # =====================

    home_xg = max(
        0.2,
        min(home_xg, 5)
    )

    away_xg = max(
        0.2,
        min(away_xg, 5)
    )

    # =====================
    # MONTE CARLO
    # =====================

    top_scores = simulate_scores(
        home_xg,
        away_xg,
        simulations=1000000
    )

    home_win = 0
    draw = 0
    away_win = 0

    for item in top_scores:

        hg, ag = map(
            int,
            item["score"].split("-")
        )

        prob = item[
            "probability"
        ]

        if hg > ag:

            home_win += prob

        elif ag > hg:

            away_win += prob

        else:

            draw += prob

    return {

        "home_team":
            home_team,

        "away_team":
            away_team,

        "home_xg":
            round(home_xg, 2),

        "away_xg":
            round(away_xg, 2),

        "home_win":
            round(home_win, 2),

        "draw":
            round(draw, 2),

        "away_win":
            round(away_win, 2),

        "predicted_score":
            top_scores[0]["score"],

        "top_scores":
            top_scores,

        "matches_analyzed":
            20,

        "h2h_matches":
            len(h2h_matches),

        "simulations":
            1000000
    }