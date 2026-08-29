import { useState, useEffect, useRef } from "react"
import { searchGlobal } from "../services/api"

const SearchModal = ({ isOpen, onClose, onNavigate }) => {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState({ projects: [], chats: [], messages: [] })
  const [loading, setLoading] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(0)
  const inputRef = useRef(null)
  const debounceRef = useRef(null)

  /* Focus input when modal opens */
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100)
      setQuery("")
      setResults({ projects: [], chats: [], messages: [] })
      setSelectedIndex(0)
    }
  }, [isOpen])

  /* Debounced search */
  useEffect(() => {
    if (!query.trim()) {
      setResults({ projects: [], chats: [], messages: [] })
      return
    }

    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(async () => {
      setLoading(true)
      try {
        const data = await searchGlobal(query)
        setResults(data)
        setSelectedIndex(0)
      } catch (err) {
        console.error("Search failed:", err)
      } finally {
        setLoading(false)
      }
    }, 300)

    return () => clearTimeout(debounceRef.current)
  }, [query])

  /* Flatten results for keyboard navigation */
  const flatResults = [
    ...results.projects.map(p => ({ ...p, _type: "project" })),
    ...results.chats.map(c => ({ ...c, _type: "chat" })),
    ...results.messages.map(m => ({ ...m, _type: "message" })),
  ]

  /* Keyboard navigation */
  const handleKeyDown = (e) => {
    if (e.key === "Escape") {
      onClose()
    } else if (e.key === "ArrowDown") {
      e.preventDefault()
      setSelectedIndex(prev => Math.min(prev + 1, flatResults.length - 1))
    } else if (e.key === "ArrowUp") {
      e.preventDefault()
      setSelectedIndex(prev => Math.max(prev - 1, 0))
    } else if (e.key === "Enter" && flatResults[selectedIndex]) {
      handleSelect(flatResults[selectedIndex])
    }
  }

  const handleSelect = (item) => {
    if (onNavigate) {
      onNavigate(item._type, item)
    }
    onClose()
  }

  if (!isOpen) return null

  const hasResults = flatResults.length > 0
  const hasQuery = query.trim().length > 0

  return (
    <div className="search-modal-overlay" onClick={onClose}>
      <div className="search-modal" onClick={(e) => e.stopPropagation()} onKeyDown={handleKeyDown}>

        {/* Search Input */}
        <div className="search-input-row">
          <span className="search-icon">🔍</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search projects, chats, research insights..."
            className="search-input"
            autoComplete="off"
          />
          <kbd className="search-kbd">ESC</kbd>
        </div>

        {/* Results */}
        <div className="search-results">
          {loading && (
            <div className="search-loading">
              <span className="animate-spin">⚡</span> Searching...
            </div>
          )}

          {!loading && hasQuery && !hasResults && (
            <div className="search-empty">
              No results found for "<strong>{query}</strong>"
            </div>
          )}

          {!loading && !hasQuery && (
            <div className="search-hint">
              <div className="search-hint-title">Quick Search</div>
              <div className="search-hint-items">
                <div><kbd>↑↓</kbd> Navigate</div>
                <div><kbd>Enter</kbd> Select</div>
                <div><kbd>Esc</kbd> Close</div>
              </div>
            </div>
          )}

          {/* Projects */}
          {results.projects.length > 0 && (
            <div className="search-group">
              <div className="search-group-label">📁 Projects</div>
              {results.projects.map((p, i) => {
                const flatIdx = i
                return (
                  <button
                    key={p.id}
                    className={`search-result-item ${selectedIndex === flatIdx ? "selected" : ""}`}
                    onClick={() => handleSelect({ ...p, _type: "project" })}
                    onMouseEnter={() => setSelectedIndex(flatIdx)}
                  >
                    <span className="search-result-icon">📂</span>
                    <div className="search-result-text">
                      <div className="search-result-title">{p.name}</div>
                      <div className="search-result-meta">{p.topic}</div>
                    </div>
                  </button>
                )
              })}
            </div>
          )}

          {/* Chats */}
          {results.chats.length > 0 && (
            <div className="search-group">
              <div className="search-group-label">💬 Chats</div>
              {results.chats.map((c, i) => {
                const flatIdx = results.projects.length + i
                return (
                  <button
                    key={c.id}
                    className={`search-result-item ${selectedIndex === flatIdx ? "selected" : ""}`}
                    onClick={() => handleSelect({ ...c, _type: "chat" })}
                    onMouseEnter={() => setSelectedIndex(flatIdx)}
                  >
                    <span className="search-result-icon">💬</span>
                    <div className="search-result-text">
                      <div className="search-result-title">{c.title}</div>
                      <div className="search-result-meta">{c.mode} mode • {c.project_name || ""}</div>
                    </div>
                  </button>
                )
              })}
            </div>
          )}

          {/* Messages */}
          {results.messages.length > 0 && (
            <div className="search-group">
              <div className="search-group-label">📄 Research Insights</div>
              {results.messages.map((m, i) => {
                const flatIdx = results.projects.length + results.chats.length + i
                return (
                  <button
                    key={m.id}
                    className={`search-result-item ${selectedIndex === flatIdx ? "selected" : ""}`}
                    onClick={() => handleSelect({ ...m, _type: "message" })}
                    onMouseEnter={() => setSelectedIndex(flatIdx)}
                  >
                    <span className="search-result-icon">{m.role === "user" ? "👤" : "🤖"}</span>
                    <div className="search-result-text">
                      <div className="search-result-title">{(m.content || "").slice(0, 80)}...</div>
                      <div className="search-result-meta">{m.role} • {m.chat_title || ""}</div>
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="search-footer">
          <span className="text-zinc-500 text-xs">⌘K to toggle • Powered by Synaptrix Intelligence</span>
        </div>
      </div>
    </div>
  )
}

export default SearchModal
