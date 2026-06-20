export interface TopScore {
  score: string;
  probability: number;
}

export interface Prediction {
  home_team: string;
  away_team: string;
  home_xg: number;
  away_xg: number;
  predicted_score: string;
  top_scores: TopScore[];
}