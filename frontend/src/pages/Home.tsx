import { useState } from "react";
import { api } from "../services/api";

import Navbar from "../components/Navbar";
import MatchForm from "../components/MatchForm";
import PredictionCard from "../components/PredictionCard";
import TopScores from "../components/TopScores";

export default function Home() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const predict = async (home: string, away: string) => {
    setLoading(true);

    try {
      const res = await api.post("/predict", {
        home_team: home,
        away_team: away,
      });

      setData(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#f5f5f7]">
        <div className="max-w-6xl mx-auto px-6 py-16">

          <div className="text-center mb-16">
            <span className="inline-block px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200 text-sm font-medium">
              ⚽ Predicción Inteligente
            </span>

            <h1 className="mt-6 text-6xl font-bold tracking-tight text-gray-900">
              Football Predictor
            </h1>

            <p className="mt-4 text-xl text-gray-500 max-w-2xl mx-auto">
              Predicciones de partidos mediante
              simulaciones Monte Carlo y análisis estadístico.
            </p>
          </div>

          <MatchForm
            onPredict={predict}
            loading={loading}
          />

          {data && (
            <div className="mt-10 space-y-6">
              <PredictionCard data={data} />
              <TopScores scores={data.top_scores} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}