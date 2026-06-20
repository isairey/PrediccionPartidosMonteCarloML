import numpy as np


def simulate_scores(
    home_xg,
    away_xg,
    simulations=100000  # 🔥 balance real
):

    # =========================
    # SIMULACIÓN POISSON (vectorizada)
    # =========================
    home_goals = np.random.poisson(home_xg, simulations)
    away_goals = np.random.poisson(away_xg, simulations)

    # =========================
    # CONTAR RESULTADOS MÁS RÁPIDO
    # =========================
    unique, counts = np.unique(
        list(zip(home_goals, away_goals)),
        axis=0,
        return_counts=True
    )

    total = simulations

    results = []

    for (h, a), count in zip(unique, counts):

        results.append({
            "score": f"{h}-{a}",
            "probability": round((count / total) * 100, 2)
        })

    # =========================
    # ORDENAR
    # =========================
    results.sort(
        key=lambda x: x["probability"],
        reverse=True
    )

    return results[:10]