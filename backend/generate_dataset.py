import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
HOST = os.getenv("API_FOOTBALL_HOST")

headers = {
    "x-apisports-key": API_KEY
}

OUTPUT_FILE = "datasets/national_matches.csv"


# ==================================
# OBTENER PARTIDOS
# ==================================
def get_fixtures(league_id, season):

    url = (
        f"https://{HOST}/fixtures"
        f"?league={league_id}"
        f"&season={season}"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        data = response.json()

        return data.get(
            "response",
            []
        )

    except Exception as e:

        print("ERROR:", e)

        return []


# ==================================
# FEATURES EQUIPO
# ==================================
def build_team_features(
    matches,
    team_id
):

    goals_for = 0
    goals_against = 0

    wins = 0
    draws = 0

    form_points = 0

    played = 0

    for match in matches:

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        if (
            home_id != team_id
            and
            away_id != team_id
        ):
            continue

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        is_home = home_id == team_id

        gf = hg if is_home else ag
        ga = ag if is_home else hg

        goals_for += gf
        goals_against += ga

        if gf > ga:

            wins += 1
            form_points += 3

        elif gf == ga:

            draws += 1
            form_points += 1

        played += 1

    if played == 0:
        return None

    return {

        "avg_gf":
            goals_for / played,

        "avg_ga":
            goals_against / played,

        "win_rate":
            wins / played,

        "form":
            form_points / (played * 3)
    }


# ==================================
# DATASET
# ==================================
def main():

    rows = []

    competitions = [

        # Mundial
        1,

        # Eliminatorias Mundial
        32,
        33,
        34,
        35,
        36,
        37,

        # Euro
        4,

        # Nations League
        5,

        # Copa América
        9,

        # Copa Oro
        6
    ]

    seasons = [

        2018,
        2019,
        2020,
        2021,
        2022,
        2023,
        2024,
        2025
    ]

    for competition in competitions:

        for season in seasons:

            print(
                f"Competition {competition} - {season}"
            )

            fixtures = get_fixtures(
                competition,
                season
            )

            for i, fixture in enumerate(fixtures):

                try:

                    home_id = fixture["teams"]["home"]["id"]
                    away_id = fixture["teams"]["away"]["id"]

                    home_goals = fixture["goals"]["home"]
                    away_goals = fixture["goals"]["away"]

                    if (
                        home_goals is None
                        or
                        away_goals is None
                    ):
                        continue

                    previous_matches = fixtures[
                        max(0, i - 20):i
                    ]

                    home_features = (
                        build_team_features(
                            previous_matches,
                            home_id
                        )
                    )

                    away_features = (
                        build_team_features(
                            previous_matches,
                            away_id
                        )
                    )

                    if (
                        not home_features
                        or
                        not away_features
                    ):
                        continue

                    # Equipo local

                    rows.append([

                        round(
                            home_features["avg_gf"],
                            3
                        ),

                        round(
                            home_features["avg_ga"],
                            3
                        ),

                        round(
                            home_features["win_rate"],
                            3
                        ),

                        round(
                            home_features["form"],
                            3
                        ),

                        home_goals

                    ])

                    # Equipo visitante

                    rows.append([

                        round(
                            away_features["avg_gf"],
                            3
                        ),

                        round(
                            away_features["avg_ga"],
                            3
                        ),

                        round(
                            away_features["win_rate"],
                            3
                        ),

                        round(
                            away_features["form"],
                            3
                        ),

                        away_goals

                    ])

                except Exception as e:

                    print(
                        "ERROR MATCH:",
                        e
                    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "avg_gf",
            "avg_ga",
            "win_rate",
            "form",
            "goals_scored"

        ])

        writer.writerows(rows)

    print(
        f"\nDATASET GENERADO: {len(rows)} FILAS"
    )


if __name__ == "__main__":
    main()