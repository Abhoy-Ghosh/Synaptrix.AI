import { useState, useRef, useEffect } from "react"

/* ─── Export Helpers ─── */

function generateMarkdown(research) {
  if (!research) return ""

  let md = `# Research Report: ${research.topic || "Untitled"}\n\n`
  md += `**Mode:** ${research.mode_used || "N/A"}\n`
  md += `**Papers Analyzed:** ${research.top_papers?.length || 0}\n\n`
  md += `---\n\n`

  if (research.summary) {
    md += `## Summary\n\n${research.summary}\n\n`
  }
  if (research.analysis) {
    md += `## Analysis\n\n${research.analysis}\n\n`
  }
  if (research.gaps) {
    md += `## Research Gaps\n\n${research.gaps}\n\n`
  }
  if (research.synthesis) {
    md += `## Synthesis\n\n${research.synthesis}\n\n`
  }

  if (research.top_papers?.length) {
    md += `## Papers\n\n`
    research.top_papers.forEach((p, i) => {
      md += `### ${i + 1}. ${p.title}\n`
      if (p.authors) md += `**Authors:** ${Array.isArray(p.authors) ? p.authors.join(", ") : p.authors}\n`
      if (p.year) md += `**Year:** ${p.year}\n`
      if (p.citations !== undefined) md += `**Citations:** ${p.citations}\n`
      if (p.abstract) md += `\n${p.abstract}\n`
      md += `\n---\n\n`
    })
  }

  return md
}

function generateBibTeX(papers) {
  if (!papers?.length) return ""

  return papers.map((p, i) => {
    const key = (p.title || "unknown")
      .split(/\s+/)
      .slice(0, 3)
      .join("")
      .replace(/[^a-zA-Z0-9]/g, "")
      .toLowerCase()

    const authors = Array.isArray(p.authors)
      ? p.authors.join(" and ")
      : p.authors || "Unknown"

    return `@article{${key}${i + 1},
  title     = {${p.title || "Untitled"}},
  author    = {${authors}},
  year      = {${p.year || "N/A"}},
  journal   = {${p.journal || p.source || "N/A"}},
  abstract  = {${(p.abstract || "").slice(0, 300)}}
}`
  }).join("\n\n")
}

function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

/* ─── ExportMenu Component ─── */

const ExportMenu = ({ research, onDownloadPDF }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [toast, setToast] = useState(null)
  const menuRef = useRef(null)

  /* Close on outside click */
  useEffect(() => {
    const handleClick = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    if (isOpen) document.addEventListener("mousedown", handleClick)
    return () => document.removeEventListener("mousedown", handleClick)
  }, [isOpen])

  const showToast = (msg) => {
    setToast(msg)
    setTimeout(() => setToast(null), 2500)
  }

  const handleCopy = async () => {
    const md = generateMarkdown(research)
    await navigator.clipboard.writeText(md)
    showToast("Copied to clipboard!")
    setIsOpen(false)
  }

  const handleMarkdown = () => {
    const md = generateMarkdown(research)
    const safeTopic = (research?.topic || "research").replace(/[^a-z0-9]/gi, "_").slice(0, 30)
    downloadFile(md, `synaptrix_${safeTopic}.md`, "text/markdown")
    showToast("Markdown downloaded!")
    setIsOpen(false)
  }

  const handleBibTeX = () => {
    const bib = generateBibTeX(research?.top_papers)
    if (!bib) {
      showToast("No papers to export")
      return
    }
    const safeTopic = (research?.topic || "research").replace(/[^a-z0-9]/gi, "_").slice(0, 30)
    downloadFile(bib, `synaptrix_${safeTopic}.bib`, "application/x-bibtex")
    showToast("BibTeX downloaded!")
    setIsOpen(false)
  }

  const handlePDF = () => {
    if (onDownloadPDF) onDownloadPDF(research)
    setIsOpen(false)
  }

  if (!research) return null

  return (
    <div className="export-menu-container" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="export-trigger-btn"
        title="Export Research"
      >
        <span>📤</span>
        <span>Export</span>
        <span className={`export-chevron ${isOpen ? "open" : ""}`}>▾</span>
      </button>

      {isOpen && (
        <div className="export-dropdown">
          <button onClick={handleCopy} className="export-option">
            <span className="export-option-icon">📋</span>
            <div>
              <div className="export-option-title">Copy to Clipboard</div>
              <div className="export-option-desc">Copy as formatted text</div>
            </div>
          </button>

          <button onClick={handleMarkdown} className="export-option">
            <span className="export-option-icon">📝</span>
            <div>
              <div className="export-option-title">Markdown (.md)</div>
              <div className="export-option-desc">Download full report</div>
            </div>
          </button>

          <button onClick={handleBibTeX} className="export-option">
            <span className="export-option-icon">📚</span>
            <div>
              <div className="export-option-title">BibTeX (.bib)</div>
              <div className="export-option-desc">Paper citations for LaTeX</div>
            </div>
          </button>

          <div className="export-divider" />

          <button onClick={handlePDF} className="export-option">
            <span className="export-option-icon">📄</span>
            <div>
              <div className="export-option-title">PDF Report</div>
              <div className="export-option-desc">Formatted research document</div>
            </div>
          </button>
        </div>
      )}

      {toast && (
        <div className="export-toast">
          <span>✓</span> {toast}
        </div>
      )}
    </div>
  )
}

export default ExportMenu
