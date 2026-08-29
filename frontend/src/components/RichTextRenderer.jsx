import React, { useState } from "react"

/* =========================================
   CATEGORY DETECTION
========================================= */
function detectCategory(text) {
  const t = text.toLowerCase()

  if (t.includes("performance") || t.includes("benchmark") || t.includes("accuracy")) {
    return { label: "Performance", color: "bg-emerald-400" }
  }
  if (t.includes("deployment") || t.includes("hardware") || t.includes("inference")) {
    return { label: "Infrastructure", color: "bg-cyan-400" }
  }
  if (t.includes("bias") || t.includes("limitations") || t.includes("risk")) {
    return { label: "Risk", color: "bg-red-400" }
  }
  if (t.includes("tool") || t.includes("agent")) {
    return { label: "Agents", color: "bg-violet-400" }
  }
  if (t.includes("efficient") || t.includes("optimization")) {
    return { label: "Optimization", color: "bg-sky-400" }
  }
  return { label: "Research", color: "bg-zinc-400" }
}

/* =========================================
   SECTION ICONS
========================================= */
function getSectionIcon(title) {
  const map = {
    "Key Insights": "◈",
    "Common Themes": "◎",
    "Emerging Focus Areas": "△",
    "Summary": "—",
    "Key Patterns": "◉",
    "Emerging Trends": "↗",
    "Research Agreements": "⊕",
    "Research Disagreements": "⊗",
    "Methodological Observations": "◇",
    "Strategic Insights": "✦",
    "Research Limitations": "◌",
    "Research Gaps": "⊘",
    "Future Research Directions": "→",
    "Methodological Weaknesses": "⌁",
    "Deployment Challenges": "▣",
    "Strategic Opportunities": "◬",
    "Cluster Relationships": "⟡",
    "Contrasting Research Directions": "⋈",
    "Cross-Domain Insights": "◎",
    "Strategic Observations": "◍",
    "Unified Research Understanding": "⊕"
  }
  return map[title] || "◈"
}

/* =========================================
   KEYWORD HIGHLIGHTING
========================================= */
function highlightKeywords(text) {
  const keywords = [
    "LLM", "LLMs", "deployment", "agents", "tool use", "benchmarking",
    "efficiency", "inference", "performance", "bias", "multitask",
    "optimization", "reasoning", "alignment", "warfare", "autonomous",
    "military", "safety", "human oversight"
  ]

  let output = text
  keywords.forEach(keyword => {
    const regex = new RegExp(`(${keyword})`, "gi")
    output = output.replace(regex, `<span class="text-cyan-300 font-semibold">$1</span>`)
  })

  return <span dangerouslySetInnerHTML={{ __html: output }} />
}

/* =========================================
   HORIZONTAL CARD CAROUSEL (Side Keys Navigation)
========================================= */
const CardCarousel = ({ items, theme }) => {
  const [currentIndex, setCurrentIndex] = useState(0)

  if (!items || items.length === 0) return null

  const prevCard = () => {
    setCurrentIndex(prev => (prev === 0 ? items.length - 1 : prev - 1))
  }

  const nextCard = () => {
    setCurrentIndex(prev => (prev === items.length - 1 ? 0 : prev + 1))
  }

  const currentText = items[currentIndex]
  const category = detectCategory(currentText)

  return (
    <div className="relative my-6 space-y-3">
      {/* Side Key Controls Header */}
      <div className="flex items-center justify-between px-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-zinc-400">
            Card <strong className="text-cyan-300 font-bold">{currentIndex + 1}</strong> of {items.length}
          </span>
          <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-mono">
            (Use side keys ◀ ▶ to navigate)
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={prevCard}
            className="carousel-side-key"
            title="Previous Card (Left Key ◀)"
          >
            ◀
          </button>
          <button
            onClick={nextCard}
            className="carousel-side-key"
            title="Next Card (Right Key ▶)"
          >
            ▶
          </button>
        </div>
      </div>

      {/* Active Card Body */}
      <div className={`relative overflow-hidden rounded-[28px] border ${theme.border} bg-gradient-to-b from-white/[0.04] to-white/[0.01] backdrop-blur-2xl p-7 shadow-2xl transition-all duration-300`}>
        <div className="flex items-center gap-3 mb-4">
          <div className={`w-3 h-3 rounded-full ${category.color} shadow-[0_0_12px_rgba(255,255,255,0.4)]`} />
          <div className="text-[10px] uppercase tracking-[0.24em] text-zinc-400 font-bold">
            {category.label}
          </div>
        </div>

        <div className="text-zinc-100 text-base leading-relaxed">
          {highlightKeywords(currentText)}
        </div>
      </div>

      {/* Dots Indicator Bar */}
      <div className="flex items-center justify-center gap-1.5 pt-1">
        {items.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentIndex(idx)}
            className={`h-2 rounded-full transition-all duration-300 ${
              idx === currentIndex ? "w-6 bg-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.6)]" : "w-2 bg-zinc-700 hover:bg-zinc-500"
            }`}
          />
        ))}
      </div>
    </div>
  )
}

/* =========================================
   MAIN RICH TEXT RENDERER
========================================= */
const RichTextRenderer = ({ text, content, type = "default" }) => {
  const rawText = text || content
  if (!rawText) return null

  const THEMES = {
    summary: { border: "border-cyan-500/30", glow: "bg-cyan-500/10", accent: "text-cyan-300", icon: "◈" },
    analysis: { border: "border-violet-500/30", glow: "bg-violet-500/10", accent: "text-violet-300", icon: "⬡" },
    gaps: { border: "border-red-500/30", glow: "bg-red-500/10", accent: "text-red-300", icon: "◇" },
    synthesis: { border: "border-emerald-500/30", glow: "bg-emerald-500/10", accent: "text-emerald-300", icon: "⊕" },
    default: { border: "border-white/10", glow: "bg-white/5", accent: "text-white", icon: "•" }
  }

  const theme = THEMES[type] || THEMES.default

  // Parse text into section blocks
  const lines = String(rawText).trim().split("\n")
  const blocks = []
  let currentHeader = null
  let currentBullets = []
  let currentParagraphs = []

  const flushBullets = () => {
    if (currentBullets.length > 0) {
      blocks.push({ type: "carousel", items: [...currentBullets] })
      currentBullets = []
    }
  }

  lines.forEach((line) => {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith("```")) return

    if (trimmed.startsWith("# ")) {
      flushBullets()
      blocks.push({ type: "h1", text: trimmed.replace("# ", "") })
    } else if (trimmed.startsWith("## ")) {
      flushBullets()
      blocks.push({ type: "h2", text: trimmed.replace("## ", "") })
    } else if (trimmed.startsWith("### ")) {
      flushBullets()
      blocks.push({ type: "h3", text: trimmed.replace("### ", "") })
    } else if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
      const bulletText = trimmed.replace("- ", "").replace("* ", "")
      currentBullets.push(bulletText)
    } else {
      flushBullets()
      blocks.push({ type: "p", text: trimmed.replace(/\*\*/g, "") })
    }
  })

  flushBullets()

  return (
    <div className="relative space-y-4 fade-in">
      {/* AGENT HEADER */}
      <div className="flex items-center gap-4 mb-6">
        <div className={`flex items-center justify-center w-10 h-10 rounded-xl border ${theme.border} bg-white/[0.03] backdrop-blur-xl shadow-lg text-lg ${theme.accent}`}>
          {theme.icon}
        </div>
        <div>
          <div className="uppercase tracking-[0.24em] text-[10px] text-zinc-500 font-mono">
            {type} intelligence
          </div>
          <div className={`text-xs font-semibold ${theme.accent}`}>
            Multi-agent semantic reasoning layer
          </div>
        </div>
      </div>

      {/* BLOCKS RENDER */}
      {blocks.map((block, idx) => {
        if (block.type === "h1") {
          return (
            <h1 key={idx} className="text-3xl md:text-4xl font-bold text-white mb-6 tracking-tight">
              {block.text}
            </h1>
          )
        }

        if (block.type === "h2") {
          return (
            <div key={idx} className="pt-6 pb-2">
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-2.5 h-2.5 rounded-full ${theme.glow}`} />
                <h2 className={`text-xl md:text-2xl font-bold tracking-tight ${theme.accent}`}>
                  {getSectionIcon(block.text)} {block.text}
                </h2>
              </div>
              <div className="h-px w-full bg-gradient-to-r from-white/15 via-white/5 to-transparent" />
            </div>
          )
        }

        if (block.type === "h3") {
          return (
            <h3 key={idx} className="text-lg font-semibold text-zinc-200 mt-4 mb-2">
              {block.text}
            </h3>
          )
        }

        if (block.type === "carousel") {
          return <CardCarousel key={idx} items={block.items} theme={theme} />
        }

        if (block.type === "p") {
          return (
            <p key={idx} className="text-zinc-300 text-sm leading-relaxed max-w-4xl font-light">
              {block.text}
            </p>
          )
        }

        return null
      })}
    </div>
  )
}

export default RichTextRenderer