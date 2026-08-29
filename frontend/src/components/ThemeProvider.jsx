import { createContext, useContext, useState, useEffect } from "react"

const ThemeContext = createContext()

export const useTheme = () => useContext(ThemeContext)

const STORAGE_KEY = "synaptrix-theme"

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) return stored
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"
  })

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme)
    localStorage.setItem(STORAGE_KEY, theme)
  }, [theme])

  /* Listen for system preference changes */
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)")
    const handler = (e) => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        setTheme(e.matches ? "dark" : "light")
      }
    }
    mq.addEventListener("change", handler)
    return () => mq.removeEventListener("change", handler)
  }, [])

  const toggleTheme = () => setTheme(prev => prev === "dark" ? "light" : "dark")
  const isDark = theme === "dark"

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, isDark }}>
      {children}
    </ThemeContext.Provider>
  )
}

/* ─── Theme Toggle Button Component ─── */
export const ThemeToggle = () => {
  const { isDark, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className="theme-toggle-btn"
      title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
      aria-label="Toggle theme"
    >
      <span className={`theme-icon ${isDark ? "rotate-0" : "rotate-180"}`}>
        {isDark ? "☀️" : "🌙"}
      </span>
    </button>
  )
}

export default ThemeProvider
