import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

        <Link
          to="/"
          className="font-semibold text-xl text-gray-900"
        >
          Football Predictor
        </Link>

        <nav className="flex items-center gap-8">
          <Link
            to="/"
            className="text-gray-600 hover:text-black transition"
          >
            Inicio
          </Link>

          <Link
            to="/history"
            className="text-gray-600 hover:text-black transition"
          >
            Historial
          </Link>
        </nav>
      </div>
    </header>
  );
}