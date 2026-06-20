import { useEffect, useState } from "react";
import { api } from "../services/api";

type Prediction = {
  home_team: string;
  away_team: string;
  home_xg: number;
  away_xg: number;
  predicted_score: string;
};

export default function History() {
  const [history, setHistory] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get("/history"); // 👈 tu endpoint futuro
        setHistory(res.data);
      } catch (error) {
        console.log("Error loading history:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-10">
      {/* Header */}
      <div className="max-w-5xl mx-auto mb-8">
        <h1 className="text-3xl font-semibold text-gray-900">
          Historial de Predicciones
        </h1>
        <p className="text-gray-500 mt-1">
          Últimos partidos simulados por el modelo
        </p>
      </div>

      {/* Content */}
      <div className="max-w-5xl mx-auto">
        {loading ? (
          <p className="text-gray-500">Cargando historial...</p>
        ) : history.length === 0 ? (
          <div className="bg-white border rounded-2xl p-6 text-gray-500">
            No hay predicciones aún
          </div>
        ) : (
          <div className="grid gap-4">
            {history.map((item, index) => (
              <div
                key={index}
                className="bg-white border rounded-2xl p-5 flex justify-between items-center shadow-sm hover:shadow-md transition"
              >
                {/* Equipos */}
                <div>
                  <p className="text-gray-900 font-medium">
                    {item.home_team} vs {item.away_team}
                  </p>
                  <p className="text-sm text-gray-500">
                    xG: {item.home_xg} - {item.away_xg}
                  </p>
                </div>

                {/* Score */}
                <div className="text-right">
                  <span className="text-xl font-semibold text-gray-900">
                    {item.predicted_score}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}