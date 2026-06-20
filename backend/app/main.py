from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predictions import router
from app.services.team_stats import search_team

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Football Predictor API"
    }


# ==========================
# TEST BUSCAR EQUIPO
# ==========================
@app.get("/test-team/{name}")
def test_team(name: str):

    team_id = search_team(name)

    return {
        "team": name,
        "team_id": team_id
    }