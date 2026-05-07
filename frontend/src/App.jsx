import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"

import Home from "./pages/Home"
import Guide from "./pages/Guide"

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/guide"
          element={<Guide />}
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App