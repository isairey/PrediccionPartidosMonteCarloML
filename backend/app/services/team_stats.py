import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
HOST = os.getenv("API_FOOTBALL_HOST")

headers = {
    "x-apisports-key": API_KEY
}


# ==================================
# CACHE SIMPLE (evita romper todo si API falla)
# ==================================
TEAM_CACHE = {
    "mexico": 769,
    "argentina": 779,
    "brazil": 777,
    "france": 657,
    "spain": 670,
    "germany": 165,
    "england": 770
}


# ==================================
# BUSCAR EQUIPO / SELECCIÓN
# ==================================
def search_team(team_name):

    key = team_name.lower()

    # 🔥 fallback inmediato
    if key in TEAM_CACHE:
        return TEAM_CACHE[key]

    url = f"https://{HOST}/teams?search={team_name}"

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        data = response.json()

        # 🔴 ERROR API LIMIT
        if "errors" in data and data["errors"]:
            print("API LIMIT:", data["errors"])
            return None

        if data.get("results", 0) > 0:
            return data["response"][0]["team"]["id"]

        return None

    except Exception as e:
        print("search_team error:", e)
        return None


# ==================================
# ÚLTIMOS PARTIDOS
# ==================================
def get_last_matches(team_id, last=15):

    if not team_id:
        return []

    url = f"https://{HOST}/fixtures?team={team_id}&last={last}"

    try:

        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()

        if "errors" in data and data["errors"]:
            print("API LIMIT fixtures:", data["errors"])
            return []

        return data.get("response", [])

    except:
        return []


# ==================================
# H2H
# ==================================
def get_h2h(home_id, away_id):

    if not home_id or not away_id:
        return []

    url = f"https://{HOST}/fixtures/headtohead?h2h={home_id}-{away_id}"

    try:

        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()

        if "errors" in data and data["errors"]:
            print("API LIMIT H2H:", data["errors"])
            return []

        return data.get("response", [])

    except:
        return []


# ==================================
# FEATURES
# ==================================
def build_features(matches, team_id):

    if not matches:
        return [1.5, 1.2, 0.5, 0.5]  # 🔥 fallback seguro

    gf = 0
    ga = 0
    wins = 0
    draws = 0
    form = 0
    played = 0

    for m in matches:

        try:
            home_id = m["teams"]["home"]["id"]

            hg = m["goals"]["home"] or 0
            ag = m["goals"]["away"] or 0

            is_home = home_id == team_id

            goals_for = hg if is_home else ag
            goals_against = ag if is_home else hg

            gf += goals_for
            ga += goals_against

            if goals_for > goals_against:
                wins += 1
                form += 3
            elif goals_for == goals_against:
                draws += 1
                form += 1

            played += 1

        except:
            continue

    if played == 0:
        return [1.5, 1.2, 0.5, 0.5]

    return [
        gf / played,
        ga / played,
        wins / played,
        form / (played * 3)
    ]