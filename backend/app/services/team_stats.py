import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
HOST = os.getenv("API_FOOTBALL_HOST")

headers = {
    "x-apisports-key": API_KEY
}


# =========================
# BUSCAR EQUIPO
# =========================
def search_team(team_name):

    url = f"https://{HOST}/teams?search={team_name}"

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if data.get("results", 0) > 0:

            return data["response"][0]["team"]["id"]

        return None

    except Exception as e:

        print("search_team:", e)

        return None


# =========================
# ÚLTIMOS PARTIDOS
# =========================
def get_last_matches(
    team_id,
    last=20
):

    url = (
        f"https://{HOST}/fixtures"
        f"?team={team_id}"
        f"&last={last}"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        return data.get(
            "response",
            []
        )

    except Exception as e:

        print(
            "get_last_matches:",
            e
        )

        return []


# =========================
# HEAD TO HEAD
# =========================
def get_h2h(
    home_id,
    away_id
):

    url = (
        f"https://{HOST}/fixtures/headtohead"
        f"?h2h={home_id}-{away_id}"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        return data.get(
            "response",
            []
        )

    except Exception as e:

        print(
            "get_h2h:",
            e
        )

        return []


# =========================
# FEATURES
# =========================
def build_features(
    matches,
    team_id
):

    if not matches:

        return {
            "avg_gf": 1.5,
            "avg_ga": 1.2,
            "win_rate": 0.5,
            "form": 0.5,
            "home_avg": 1.5,
            "away_avg": 1.2
        }

    goals_for = 0
    goals_against = 0

    wins = 0
    draws = 0
    losses = 0

    home_goals = 0
    away_goals = 0

    home_games = 0
    away_games = 0

    form_points = 0

    for match in matches:

        try:

            is_home = (
                match["teams"]["home"]["id"]
                == team_id
            )

            hg = (
                match["goals"]["home"] or 0
            )

            ag = (
                match["goals"]["away"] or 0
            )

            if is_home:

                gf = hg
                ga = ag

                home_goals += gf
                home_games += 1

            else:

                gf = ag
                ga = hg

                away_goals += gf
                away_games += 1

            goals_for += gf
            goals_against += ga

            if gf > ga:

                wins += 1
                form_points += 3

            elif gf == ga:

                draws += 1
                form_points += 1

            else:

                losses += 1

        except:
            pass

    played = max(
        len(matches),
        1
    )

    return {

        "avg_gf":
            goals_for / played,

        "avg_ga":
            goals_against / played,

        "win_rate":
            wins / played,

        "form":
            form_points / (played * 3),

        "home_avg":
            home_goals / max(home_games, 1),

        "away_avg":
            away_goals / max(away_games, 1)
    }