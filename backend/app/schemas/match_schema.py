from pydantic import BaseModel

class MatchRequest(BaseModel):
    home_team: str
    away_team: str