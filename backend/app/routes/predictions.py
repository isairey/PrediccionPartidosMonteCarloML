from fastapi import APIRouter
from app.schemas.match_schema import MatchRequest
from app.services.predictor import predict_match

router = APIRouter()

@router.post("/predict")
def predict(data: MatchRequest):

    return predict_match(
        data.home_team,
        data.away_team
    )