import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"

import { ThemeProvider } from "./components/ThemeProvider"
import Home from "./pages/Home"
import Guide from "./pages/Guide"
import Dashboard from "./pages/Dashboard"

function App() {

  return (

    <ThemeProvider>
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

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

        </Routes>

      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App