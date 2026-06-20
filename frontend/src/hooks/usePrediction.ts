import { useState } from "react";
import { api } from "../services/api";

export function usePrediction() {
  const [loading, setLoading] = useState(false);

  const predict = async (
    home_team: string,
    away_team: string
  ) => {
    setLoading(true);

    try {
      const response = await api.post("/predict", {
        home_team,
        away_team,
      });

      return response.data;
    } finally {
      setLoading(false);
    }
  };

  return { predict, loading };
}