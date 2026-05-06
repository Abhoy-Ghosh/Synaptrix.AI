import { useState, useEffect, useRef } from "react"

import {
  generateResearch,
  submitGlobalFeedback
} from "../services/api"

import PaperCard from "../components/PaperCard"
import PipelineStatus from "../components/PipelineStatus"
import LoadingSkeleton from "../components/LoadingSkeleton"
import RichTextRenderer from "../components/RichTextRenderer"

import { downloadResearchPDF } from "../services/api"
/* ── tiny helpers ── */
const TAB_META = {
  summary:   { label: "Summary",   icon: "◈", desc: "AI-generated synthesis" },
  analysis:  { label: "Analysis",  icon: "⬡", desc: "Deep pattern analysis" },
  gaps:      { label: "Gaps",      icon: "◇", desc: "Research opportunities" },
  synthesis: { label: "Synthesis", icon: "⊕", desc: "Cross-paper reasoning" },
  papers:    { label: "Papers",    icon: "◉", desc: "Source documents" },
}

const Home = () => {

  const [topic, setTopic]               = useState("")
  const [mode, setMode]                 = useState("fast")
  const [loading, setLoading]           = useState(false)
  const [result, setResult]             = useState(null)
  const [activeTab, setActiveTab]       = useState("summary")
  const [currentStep, setCurrentStep]   = useState(-1)
  const [globalFeedback, setGlobalFeedback] = useState("")

  const [generationTime, setGenerationTime] = useState(null)

const [credits, setCredits] = useState(300)

  /* navbar scroll state */
  const [scrolled, setScrolled]         = useState(false)
  const [charCount, setCharCount]       = useState(0)
  const resultsRef                      = useRef(null)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  /* ─── GENERATE ─── */
 /* ─── GENERATE ─── */

const handleGenerate = async () => {

  if (!topic.trim()) return

  if (credits <= 0) {

    alert("No credits remaining")

    return
  }

  try {

    setLoading(true)

    setResult(null)

    setGlobalFeedback("")

    const startTime =
      performance.now()

    /* pipeline status */

/* pipeline animation */

let step = 0

setCurrentStep(step)

const interval = setInterval(() => {

  step++

  if (step <= 5) {
    setCurrentStep(step)
  }

}, 1400)

/* backend call */

const data =
  await generateResearch(
    topic,
    mode
  )

/* stop animation */

clearInterval(interval)

setCurrentStep(5)

    setResult(data)

    /* timing */

    const endTime =
      performance.now()

    const totalSeconds =
      (
        (endTime - startTime) / 1000
      ).toFixed(1)

    setGenerationTime(totalSeconds)

    /* credits */

    if (mode === "fast") {
      setCredits(prev => prev - 1)
    }

    if (mode === "parallel") {
      setCredits(prev => prev - 3)
    }

    if (mode === "research") {
      setCredits(prev => prev - 6)
    }

    /* scroll */

    setTimeout(() => {

      resultsRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start"
      })

    }, 120)

  } catch (err) {

    console.log(err)

  } finally {

    setLoading(false)

    setCurrentStep(-1)
  }
}
  /* ─── GLOBAL FEEDBACK ─── */
  const handleGlobalFeedback = async (type) => {
    try {
      await submitGlobalFeedback(topic, type)
      setGlobalFeedback(type)
    } catch (err) {
      console.log(err)
    }
  }

  const handleTopicChange = (e) => {
    setTopic(e.target.value)
    setCharCount(e.target.value.length)
  }

  const tabs = Object.keys(TAB_META)

  return (
    <div className="min-h-screen text-white overflow-x-hidden" style={{ background: 'var(--bg-deep)' }}>

      {/* ─── AMBIENT BACKGROUND ─── */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        <div className="ambient-orb orb-1" />
        <div className="ambient-orb orb-2" />
        <div className="ambient-orb orb-3" />
        <div className="absolute inset-0 neural-bg opacity-60" />
        {/* subtle vignette */}
        <div className="absolute inset-0" style={{
          background: 'radial-gradient(ellipse 120% 80% at 50% 0%, transparent 40%, rgba(5,8,16,0.8) 100%)'
        }} />
      </div>

      {/* ─── STICKY NAVBAR ─── */}
      <nav className={`sticky top-0 z-50 navbar-glass ${scrolled ? "scrolled" : ""}`}
           style={{ height: 'var(--nav-height)' }}>
        <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">

          {/* LEFT — logo + brand */}
          <div className="flex items-center gap-4">
            <div className="logo-container bg-white rounded-[22px] p-1.5 shadow-xl shadow-blue-500/10">
              <img
                src="/logo.png"
                alt="Synaptrix AI"
                className="w-12 h-12 object-contain"
              />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-black tracking-wide gradient-text-animated"
                  style={{ fontFamily: 'var(--font-display)' }}>
                Synaptrix AI
              </h1>
              <p className="text-zinc-500 text-[10px] tracking-[0.22em] uppercase"
                 style={{ fontFamily: 'var(--font-display)' }}>
                Adaptive Research Intelligence
              </p>
            </div>
          </div>

          {/* RIGHT — nav actions */}
          <div className="flex items-center gap-3">

            {/* credits */}

<div
  className="
    hidden
    md:flex

    items-center
    gap-2

    px-4
    py-2

    rounded-full
  "
  style={{
    background:
      'rgba(59,130,246,0.08)',

    border:
      '1px solid rgba(59,130,246,0.12)',
  }}
>

  <div
    className="
      w-1.5
      h-1.5
      rounded-full
      bg-cyan-400
    "
  />

  <span
    className="
      text-xs
      text-zinc-300
    "
    style={{
      fontFamily:
        'var(--font-display)',

      letterSpacing:
        '0.06em'
    }}
  >
    {credits} Credits
  </span>

</div>

            {/* mode indicator pill */}
            <div className="hidden sm:flex items-center gap-2 counter-badge px-4 py-2 rounded-full">
              <span className="text-zinc-400">
                {mode === "fast" ? "⚡" : mode === "parallel" ? "🔄" : "🧠"}
              </span>
              <span className="text-zinc-300 text-xs capitalize"
                    style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
                {mode} mode
              </span>
            </div>

            {/* status badge */}
            <div className="status-badge flex items-center gap-2.5 px-4 py-2 rounded-full">
              <span className="relative flex w-2 h-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-60" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-400" />
              </span>
              <span className="text-xs text-zinc-300 hidden md:inline"
                    style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
                Neural Active
              </span>
            </div>
          </div>
        </div>

        {/* thin gradient underline */}
        <div className="absolute bottom-0 left-0 right-0 h-px"
             style={{
               background: 'linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.2) 30%, rgba(6,182,212,0.15) 50%, rgba(139,92,246,0.2) 70%, transparent 100%)'
             }} />
      </nav>

      {/* ─── MAIN ─── */}
      <div
  className="
    w-full

    max-w-[1400px]

    mx-auto

    px-6
    sm:px-8
    md:px-10
    lg:px-14
    xl:px-20

    py-16
  "
>

        {/* ─── HERO ─── */}
        <div className="mb-20 relative">

          {/* floating badge */}
          <div className="anim-fade-up delay-1 inline-flex items-center gap-3 hero-badge px-5 py-2.5 rounded-full mb-10 cursor-default select-none">
            <div className="w-1.5 h-1.5 rounded-full bg-cyan-400"
                 style={{ animation: 'neural-pulse 1.8s ease infinite' }} />
            <span className="text-cyan-300 text-xs tracking-widest uppercase"
                  style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.15em' }}>
              Multi-Agent AI Research Platform
            </span>
            <div className="w-px h-3 bg-cyan-500/30 mx-1" />
            <span className="text-cyan-500/60 text-xs" style={{ fontFamily: 'var(--font-display)' }}>v2.0</span>
          </div>

          {/* headline */}
          <div className="anim-fade-up delay-2 mb-8">
            <h2 className="hero-title font-black leading-[1.04] mb-3"
                style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', fontFamily: 'var(--font-display)' }}>
              <span className="hero-title-glow">Neural Research</span>
              <br />
              <span className="gradient-text-animated">Intelligence</span>
              <br />
              <span className="hero-title-glow">Engine</span>
            </h2>
          </div>

          {/* sub-headline */}
          <p className="anim-fade-up delay-3 text-zinc-400 text-lg leading-8 max-w-xl mb-12"
             style={{ fontFamily: 'var(--font-body)', fontWeight: 300 }}>
            Adaptive multi-agent synthesis, semantic retrieval,
            cross-paper reasoning, intelligent clustering,
            and feedback-driven research generation.
          </p>

          {/* stat pills row */}
          <div className="anim-fade-up delay-4 flex flex-wrap gap-3">
            {[
              { label: "Agents", value: "8+" },
              { label: "Sources", value: "50K+" },
              { label: "Modes", value: "3" },
              { label: "Latency", value: "< 7s" },
            ].map((stat) => (
              <div key={stat.label}
                   className="flex items-center gap-2 px-4 py-2 rounded-full"
                   style={{
                     background: 'rgba(255,255,255,0.025)',
                     border: '1px solid rgba(255,255,255,0.06)',
                   }}>
                <span className="text-zinc-300 text-sm font-semibold"
                      style={{ fontFamily: 'var(--font-display)' }}>
                  {stat.value}
                </span>
                <span className="text-zinc-600 text-xs">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ─── INPUT PANEL ─── */}
        <div className="anim-fade-up delay-3 input-panel rounded-[36px] p-8 md:p-10 mb-6">

          {/* panel top bar */}
          <div className="input-top-bar flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl flex items-center justify-center"
                   style={{
                     background: 'rgba(59,130,246,0.1)',
                     border: '1px solid rgba(59,130,246,0.18)',
                   }}>
                <span style={{ fontSize: '14px' }}>◈</span>
              </div>
              <div>
                <p className="text-xl text-zinc-400 uppercase tracking-widest"
                   style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.14em' }}>
                  Research Query
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {charCount > 0 && (
                <span className="text-xs text-zinc-600 tabular-nums"
                      style={{ fontFamily: 'var(--font-display)' }}>
                  {charCount} chars
                </span>
              )}
              <div className="w-1.5 h-1.5 rounded-full"
                   style={{
                     background: topic.trim() ? '#22c55e' : '#374151',
                     boxShadow: topic.trim() ? '0 0 8px rgba(34,197,94,0.4)' : 'none',
                     transition: 'all 0.3s ease',
                   }} />
            </div>
          </div>

          {/* textarea */}
          <textarea
            value={topic}
            onChange={handleTopicChange}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleGenerate()
            }}
            placeholder="Describe your research topic in detail… e.g. 'Recent advances in transformer architectures for long-context understanding'"
            className="ai-textarea w-full p-6 min-h-[180px] text-base mb-6"
          />

          {/* bottom bar */}
          <div className="flex flex-wrap items-center justify-between gap-4">

            <div className="flex items-center gap-3 flex-wrap">
              {/* mode select */}
              <div className="relative">
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="mode-select px-5 py-3.5 rounded-2xl text-sm"
                >
<option value="fast"  
style={{
    background: '#0f172a',
    color: 'white'
  }}>
  ⚡ Fast Mode • 1 Credit
</option>

<option value="parallel"
 style={{
    background: '#0f172a',
    color: 'white'
  }}>
  🔄 Parallel Mode • 3 Credits
</option>

<option value="research"
 style={{
    background: '#0f172a',
    color: 'white'
  }}>
  🧠 Research Mode • 6 Credits
</option>
                </select>
              </div>

              {/* cmd shortcut hint */}
              <div className="hidden md:flex items-center gap-1.5 px-3 py-2 rounded-xl"
                   style={{
                     background: 'rgba(255,255,255,0.025)',
                     border: '1px solid rgba(255,255,255,0.05)',
                   }}>
                <kbd className="text-[10px] text-zinc-500 px-1.5 py-0.5 rounded"
                    style={{ background: 'rgba(255,255,255,0.04)', fontFamily: 'var(--font-display)' }}>
                  ⌘
                </kbd>
                <span className="text-[10px] text-zinc-600">+</span>
                <kbd className="text-[10px] text-zinc-500 px-1.5 py-0.5 rounded"
                    style={{ background: 'rgba(255,255,255,0.04)', fontFamily: 'var(--font-display)' }}>
                  ↵
                </kbd>
                <span className="text-[10px] text-zinc-600 ml-1">to generate</span>
              </div>
            </div>

            {/* generate button */}
            <button
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
              className="btn-generate px-10 py-4 rounded-2xl text-base text-white disabled:opacity-40 disabled:cursor-not-allowed disabled:transform-none disabled:animation-none"
              style={{ minWidth: '200px' }}
            >
              <span className="relative z-10 flex items-center justify-center gap-3">
                {loading ? (
                  <>
                    <span className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white animate-spin" />
                    <span>Generating…</span>
                  </>
                ) : (
                  <>
                    <span>Generate Research</span>
                    <span style={{ fontSize: '18px' }}>→</span>
                  </>
                )}
              </span>
            </button>
          </div>
        </div>

        {/* ─── PIPELINE ─── */}
        {loading && (
          <div className="anim-slide-down">
            <PipelineStatus currentStep={currentStep} />
          </div>
        )}

        {/* ─── SKELETON ─── */}
        {loading && <LoadingSkeleton />}

        {/* ─── RESULTS ─── */}
        {result && (
          <div className="mt-20 anim-fade-up" ref={resultsRef}>

            {/* results header */}
           

<div className="flex items-center justify-between gap-6 mb-10">

  {/* LEFT SIDE */}

  <div className="flex items-center gap-4 flex-1">

    <div className="h-px flex-1 divider-glow" />

    <div
      className="
        flex
        items-center
        gap-3

        px-5
        py-2.5

        rounded-full
      "
      style={{
        background:
          'rgba(59,130,246,0.06)',

        border:
          '1px solid rgba(59,130,246,0.12)',
      }}
    >

      <div
        className="
          w-1.5
          h-1.5
          rounded-full
          bg-blue-400
        "
        style={{
          animation:
            'neural-pulse 2s ease infinite'
        }}
      />

      <span
        className="
          text-xs
          text-blue-300
          uppercase
          tracking-widest
        "
        style={{
          fontFamily:
            'var(--font-display)',

          letterSpacing:
            '0.14em'
        }}
      >
        Research Complete
      </span>

    </div>

    <div className="h-px flex-1 divider-glow" />

  </div>


  {/* PDF BUTTON */}

  <button
    onClick={() =>
      downloadResearchPDF({
        topic,
        ...result
      })
    }

    className="
      px-5
      py-3

      rounded-2xl

      text-sm
      font-medium

      transition-all
      duration-300

      hover:scale-[1.02]
     
    "

    style={{
      background:
        'rgba(59,130,246,0.10)',

      border:
        '1px solid rgba(59,130,246,0.18)',

      backdropFilter:
        'blur(20px)',

      color:
        'white'
    }}
  >
    Download PDF
  </button>

</div>

            {/* TABS */}
            <div className="flex flex-wrap gap-2 mb-10">
              {tabs.map((tab, i) => {
                const meta = TAB_META[tab]
                const isActive = activeTab === tab
                return (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`tab-btn px-5 py-3 rounded-2xl flex items-center gap-2.5 ${
                      isActive ? "tab-btn-active" : "tab-btn-inactive"
                    }`}
                    style={{ animationDelay: `${i * 0.06}s` }}
                  >
                    <span style={{
                      color: isActive ? '#60a5fa' : 'rgba(148,163,184,0.5)',
                      fontSize: '14px',
                      transition: 'color 0.25s ease',
                    }}>
                      {meta.icon}
                    </span>
                    <span>{meta.label}</span>
                    {isActive && (
                      <span className="w-1 h-1 rounded-full bg-blue-400 ml-0.5"
                            style={{ animation: 'neural-pulse 1.5s ease infinite' }} />
                    )}
                  </button>
                )
              })}
            </div>

            {/* TAB CONTENT */}
            <div className="tab-content">

              {/* ── SUMMARY ── */}
              {activeTab === "summary" && (
                <div className="result-card rounded-[var(--radius-xl)] overflow-hidden">
                  {/* card header accent */}
                  <div className="h-px w-full"
                       style={{ background: 'linear-gradient(90deg, transparent, rgba(59,130,246,0.4), rgba(6,182,212,0.3), transparent)' }} />
                  <div className="p-10">
                    <div className="flex items-start justify-between mb-10">
                      <div>
                        <p className="section-label mb-2">AI Synthesis</p>
                        <h2 className="result-section-title">Research Summary</h2>
                      </div>
                      <div className="w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0"
                           style={{
                             background: 'rgba(59,130,246,0.1)',
                             border: '1px solid rgba(59,130,246,0.18)',
                           }}>
                        <span>◈</span>
                      </div>
                    </div>

                  <div style={{ maxWidth: '90ch' }}>
    <RichTextRenderer
        text={result.summary}
        type="summary"
    />
</div>

                    {/* FEEDBACK */}
                    <div className="feedback-section rounded-2xl p-8 mt-10 -mx-2">
                      <div className="flex items-center gap-3 mb-6">
                        <div className="h-px flex-1"
                             style={{ background: 'rgba(255,255,255,0.04)' }} />
                        <p className="text-xs text-zinc-500 uppercase tracking-widest"
                           style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.14em' }}>
                          Relevance Signal
                        </p>
                        <div className="h-px flex-1"
                             style={{ background: 'rgba(255,255,255,0.04)' }} />
                      </div>

                      <p className="text-sm text-zinc-400 mb-5"
                         style={{ fontFamily: 'var(--font-body)' }}>
                        Was this research result useful?
                      </p>

                      <div className="flex gap-3 flex-wrap">
                        <button
                          onClick={() => handleGlobalFeedback("good")}
                          className={`feedback-btn-good px-6 py-3 rounded-2xl text-sm font-semibold flex items-center gap-2.5 ${
                            globalFeedback === "good" ? "active" : ""
                          }`}
                          style={{ fontFamily: 'var(--font-body)' }}
                        >
                          <span>👍</span>
                          <span>Good Result</span>
                          {globalFeedback === "good" && (
                            <span className="w-1.5 h-1.5 rounded-full bg-green-400 ml-1"
                                  style={{ animation: 'neural-pulse 1.5s ease infinite' }} />
                          )}
                        </button>

                        <button
                          onClick={() => handleGlobalFeedback("bad")}
                          className={`feedback-btn-bad px-6 py-3 rounded-2xl text-sm font-semibold flex items-center gap-2.5 ${
                            globalFeedback === "bad" ? "active" : ""
                          }`}
                          style={{ fontFamily: 'var(--font-body)' }}
                        >
                          <span>👎</span>
                          <span>Bad Result</span>
                          {globalFeedback === "bad" && (
                            <span className="w-1.5 h-1.5 rounded-full bg-red-400 ml-1"
                                  style={{ animation: 'neural-pulse 1.5s ease infinite' }} />
                          )}
                        </button>
                      </div>

                      {globalFeedback && (
                        <div className="mt-5 flex items-center gap-2">
                          <span className="w-1.5 h-1.5 rounded-full inline-block"
                                style={{ background: globalFeedback === 'good' ? '#22c55e' : '#ef4444' }} />
                          <p className="text-xs text-zinc-500"
                             style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
                            Signal recorded — thank you
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* ── ANALYSIS ── */}
              {activeTab === "analysis" && (
                <div className="result-card rounded-[var(--radius-xl)] overflow-hidden">
                  <div className="h-px w-full"
                       style={{ background: 'linear-gradient(90deg, transparent, rgba(6,182,212,0.4), rgba(139,92,246,0.3), transparent)' }} />
                  <div className="p-10">
                    <div className="flex items-start justify-between mb-10">
                      <div>
                        <p className="section-label mb-2">Pattern Recognition</p>
                        <h2 className="result-section-title">Research Analysis</h2>
                      </div>
                      <div className="w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0"
                           style={{
                             background: 'rgba(6,182,212,0.1)',
                             border: '1px solid rgba(6,182,212,0.18)',
                           }}>
                        <span>⬡</span>
                      </div>
                    </div>
                   <div style={{ maxWidth: '90ch' }}>
    <RichTextRenderer text={result.analysis} />
</div>
                  </div>
                </div>
              )}

              {/* ── GAPS ── */}
              {activeTab === "gaps" && (
                <div className="result-card rounded-[var(--radius-xl)] overflow-hidden">
                  <div className="h-px w-full"
                       style={{ background: 'linear-gradient(90deg, transparent, rgba(139,92,246,0.4), rgba(59,130,246,0.3), transparent)' }} />
                  <div className="p-10">
                    <div className="flex items-start justify-between mb-10">
                      <div>
                        <p className="section-label mb-2">Opportunity Mapping</p>
                        <h2 className="result-section-title">Research Gaps</h2>
                      </div>
                      <div className="w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0"
                           style={{
                             background: 'rgba(139,92,246,0.1)',
                             border: '1px solid rgba(139,92,246,0.18)',
                           }}>
                        <span>◇</span>
                      </div>
                    </div>
                    <div style={{ maxWidth: '90ch' }}>
    <RichTextRenderer
        text={result.gaps}
        type="gaps"
    />
</div>
                  </div>
                </div>
              )}

              {/* ── SYNTHESIS ── */}
              {activeTab === "synthesis" && (
                <div className="result-card rounded-[var(--radius-xl)] overflow-hidden">
                  <div className="h-px w-full"
                       style={{ background: 'linear-gradient(90deg, transparent, rgba(59,130,246,0.3), rgba(6,182,212,0.4), rgba(139,92,246,0.3), transparent)' }} />
                  <div className="p-10">
                    <div className="flex items-start justify-between mb-10">
                      <div>
                        <p className="section-label mb-2">Cross-Paper Reasoning</p>
                        <h2 className="result-section-title">Synthesis</h2>
                      </div>
                      <div className="w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0"
                           style={{
                             background: 'rgba(59,130,246,0.08)',
                             border: '1px solid rgba(59,130,246,0.15)',
                           }}>
                        <span>⊕</span>
                      </div>
                    </div>
                    <div style={{ maxWidth: '90ch' }}>
   <RichTextRenderer
      text={result.synthesis}
      type="synthesis"
   />
</div>
                  </div>
                </div>
              )}

              {/* ── PAPERS ── */}
              {activeTab === "papers" && (
                <div>
                  <div className="flex items-center justify-between mb-10">
                    <div>
                      <p className="section-label mb-2">Source Documents</p>
                      <h2 className="result-section-title">Top Research Papers</h2>
                    </div>
                    {result.top_papers?.length > 0 && (
                      <div className="counter-badge px-4 py-2 rounded-full flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-400"
                              style={{ animation: 'neural-pulse 2s ease infinite' }} />
                        <span className="text-zinc-300 text-xs"
                              style={{ fontFamily: 'var(--font-display)' }}>
                          {result.top_papers.length} papers
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="grid xl:grid-cols-2 gap-8">
                    {result.top_papers?.map((paper, idx) => (
                      <PaperCard key={idx} paper={paper} index={idx} />
                    ))}
                  </div>
                </div>
              )}

            </div>
          </div>
        )}

        {/* ─── FOOTER ─── */}
        <footer className="mt-32 pb-10">
          <div className="divider-glow mb-8" />
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="bg-white/90 rounded-xl p-1">
                <img src="/logo.png" alt="" className="w-6 h-6 object-contain" />
              </div>
              <span className="text-xs text-zinc-600"
                    style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.08em' }}>
                Synaptrix AI — Adaptive Research Intelligence System
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-green-400"
                   style={{ animation: 'neural-pulse 2s ease infinite' }} />
              <span className="text-xs text-zinc-600"
                    style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
                All systems operational
              </span>
            </div>
          </div>
        </footer>

      </div>
    </div>
  )
}

export default Home