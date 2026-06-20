import type { Prediction } from "../types/Prediction";

interface Props {
  data: Prediction;
}

export default function PredictionCard({ data }: Props) {
  return (
    <div className="bg-white rounded-[32px] p-10 shadow-sm border border-gray-200">

      <div className="text-center">

        <h2 className="text-3xl font-semibold text-gray-900">
          {data.home_team}
        </h2>

        <div className="my-6 text-gray-400 text-xl">
          VS
        </div>

        <h2 className="text-3xl font-semibold text-gray-900">
          {data.away_team}
        </h2>

        <div className="mt-10">

          <p className="text-gray-500">
            Marcador más probable
          </p>

          <h1 className="text-8xl font-bold tracking-tight text-gray-900 mt-2">
            {data.predicted_score}
          </h1>

          <p className="mt-4 text-gray-500">
            xG: {data.home_xg} • {data.away_xg}
          </p>
        </div>

      </div>
    </div>
  );
}