import numpy as np

from collections import Counter


def simulate_scores(

    home_xg,
    away_xg,

    simulations=100000

):

    scores = []

    for _ in range(simulations):

        # =====================
        # GAUSSIANA
        # =====================

        home_xg_sim = np.random.normal(
            loc=home_xg,
            scale=0.30
        )

        away_xg_sim = np.random.normal(
            loc=away_xg,
            scale=0.30
        )

        home_xg_sim = max(
            0.1,
            home_xg_sim
        )

        away_xg_sim = max(
            0.1,
            away_xg_sim
        )

        # =====================
        # POISSON
        # =====================

        home_goals = np.random.poisson(
            home_xg_sim
        )

        away_goals = np.random.poisson(
            away_xg_sim
        )

        scores.append(
            f"{home_goals}-{away_goals}"
        )

    counter = Counter(scores)

    top_scores = []

    for score, count in counter.most_common(10):

        probability = (
            count / simulations
        ) * 100

        top_scores.append({

            "score": score,

            "probability": round(
                probability,
                2
            )

        })

    return top_scores