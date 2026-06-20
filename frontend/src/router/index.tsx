import { createBrowserRouter } from "react-router-dom";

import Home from "../pages/Home";
import History from "../pages/History";
import NotFound from "../pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/history",
    element: <History />,
  },
  {
    path: "*",
    element: <NotFound />,
  },
]);