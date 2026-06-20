import type { TopScore } from "../types/Prediction";

interface Props {
  scores: TopScore[];
}

export default function TopScores({ scores }: Props) {
  return (
    <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-200">

      <h2 className="text-2xl font-semibold mb-6">
        Resultados más probables
      </h2>

      <div className="space-y-3">
        {scores?.map((item, index) => (
          <div
            key={index}
            className="
              flex
              items-center
              justify-between
              bg-gray-50
              rounded-2xl
              px-5
              py-4
            "
          >
            <span className="font-medium">
              {item.score}
            </span>

            <span className="text-gray-500">
              {item.probability}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}