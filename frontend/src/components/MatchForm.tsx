import { useState } from "react";

interface Props {
  onPredict: (home: string, away: string) => void;
  loading: boolean;
}

export default function MatchForm({
  onPredict,
  loading,
}: Props) {
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");

  return (
    <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-200">

      <div className="grid md:grid-cols-2 gap-4">

        <input
          value={home}
          onChange={(e) => setHome(e.target.value)}
          placeholder="Equipo local"
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            border
            border-gray-200
            bg-gray-50
            focus:outline-none
            focus:ring-2
            focus:ring-black
          "
        />

        <input
          value={away}
          onChange={(e) => setAway(e.target.value)}
          placeholder="Equipo visitante"
          className="
            w-full
            px-5
            py-4
            rounded-2xl
            border
            border-gray-200
            bg-gray-50
            focus:outline-none
            focus:ring-2
            focus:ring-black
          "
        />
      </div>

      <button
        onClick={() => onPredict(home, away)}
        disabled={loading}
        className="
          mt-6
          w-full
          py-4
          rounded-2xl
          bg-black
          text-white
          font-medium
          hover:opacity-90
          transition
        "
      >
        {loading
          ? "Calculando predicción..."
          : "Predecir partido"}
      </button>
    </div>
  );
}