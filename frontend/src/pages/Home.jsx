import { useState, useEffect, useRef } from "react"

import {
  generateResearch,
  submitGlobalFeedback,
  fetchProjects,
  createProject,
  deleteProject,
  fetchProjectChats,
  createChat,
  fetchChatDetail,
  deleteChat,
  sendChatMessage,
  downloadResearchPDF
} from "../services/api"

import { useTheme, ThemeToggle } from "../components/ThemeProvider"
import Sidebar from "../components/Sidebar"
import PaperCard from "../components/PaperCard"
import PipelineStatus from "../components/PipelineStatus"
import RichTextRenderer from "../components/RichTextRenderer"
import ExportMenu from "../components/ExportMenu"
import SearchModal from "../components/SearchModal"
import KnowledgeGraph from "../components/KnowledgeGraph"

/* ── tiny helpers ── */
const TAB_META = {
  summary:   { label: "Summary",   icon: "◈" },
  analysis:  { label: "Analysis",  icon: "⬡" },
  gaps:      { label: "Gaps",      icon: "◇" },
  synthesis: { label: "Synthesis", icon: "⊕" },
  papers:    { label: "Papers",    icon: "◉" },
}

const Home = () => {
  const { isDark } = useTheme()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [projects, setProjects] = useState([])
  const [expandedProjects, setExpandedProjects] = useState({})
  const [projectChatsMap, setProjectChatsMap] = useState({})

  const [activeProjectId, setActiveProjectId] = useState(null)
  const [activeChatId, setActiveChatId] = useState(null)
  const [messages, setMessages] = useState([])
  const [turnActiveTabs, setTurnActiveTabs] = useState({}) // { msgId: 'summary' | 'analysis' | ... }

  const [topic, setTopic]               = useState("")
  const [mode, setMode]                 = useState("fast")
  const [loading, setLoading]           = useState(false)
  const [currentStep, setCurrentStep]   = useState(-1)
  const [globalFeedback, setGlobalFeedback] = useState("")

  const [scrolled, setScrolled]         = useState(false)
  const [charCount, setCharCount]       = useState(0)
  const chatStreamEndRef                = useRef(null)

  /* ── New feature states ── */
  const [searchOpen, setSearchOpen] = useState(false)
  const [showKnowledgeGraph, setShowKnowledgeGraph] = useState(false)

  /* ── Load Projects on Mount ── */
  useEffect(() => {
    loadProjectsList()
  }, [])

  const loadProjectsList = async () => {
    try {
      const data = await fetchProjects()
      setProjects(data)
    } catch (err) {
      console.error("Failed to load projects:", err)
    }
  }

  const loadChatsForProject = async (projId) => {
    try {
      const chats = await fetchProjectChats(projId)
      setProjectChatsMap(prev => ({ ...prev, [projId]: chats }))
    } catch (err) {
      console.error("Failed to load project chats:", err)
    }
  }

  const handleSelectProject = (projId) => {
    setActiveProjectId(projId)
    setExpandedProjects(prev => ({ ...prev, [projId]: !prev[projId] }))
    if (!projectChatsMap[projId]) {
      loadChatsForProject(projId)
    }
  }

  const handleSelectChat = async (projId, chatId) => {
    setActiveProjectId(projId)
    setActiveChatId(chatId)
    setShowKnowledgeGraph(false)
    setLoading(true)

    try {
      const detail = await fetchChatDetail(chatId)
      setMessages(detail.messages || [])
      setMode(detail.chat?.mode || "fast")
    } catch (err) {
      console.error("Failed to load chat details:", err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (name, topicArea) => {
    try {
      const proj = await createProject(name, topicArea)
      await loadProjectsList()
      setActiveProjectId(proj.id)
      setExpandedProjects(prev => ({ ...prev, [proj.id]: true }))
      const chat = await createChat(proj.id, "Session 1", "parallel")
      await loadChatsForProject(proj.id)
      handleSelectChat(proj.id, chat.id)
    } catch (err) {
      console.error("Failed to create project:", err)
    }
  }

  const handleDeleteProject = async (projId) => {
    try {
      await deleteProject(projId)
      if (activeProjectId === projId) {
        setActiveProjectId(null)
        setActiveChatId(null)
        setMessages([])
      }
      loadProjectsList()
    } catch (err) {
      console.error("Failed to delete project:", err)
    }
  }

  const handleCreateChat = async (projId, title, chatMode) => {
    try {
      const chat = await createChat(projId, title, chatMode)
      await loadChatsForProject(projId)
      handleSelectChat(projId, chat.id)
    } catch (err) {
      console.error("Failed to create chat:", err)
    }
  }

  const handleDeleteChat = async (projId, chatId) => {
    try {
      await deleteChat(chatId)
      if (activeChatId === chatId) {
        setActiveChatId(null)
        setMessages([])
      }
      loadChatsForProject(projId)
    } catch (err) {
      console.error("Failed to delete chat:", err)
    }
  }

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  /* Ctrl+K global search shortcut */
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault()
        setSearchOpen(prev => !prev)
      }
    }
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [])

  /* Scroll chat stream to bottom when new messages arrive */
  useEffect(() => {
    chatStreamEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  /* ─── GENERATE / SEND CHAT MESSAGE ─── */
  const handleGenerate = async () => {
    const queryText = topic.trim()
    if (!queryText) return

    try {
      setLoading(true)
      setGlobalFeedback("")

      let step = 0
      setCurrentStep(step)
      const interval = setInterval(() => {
        step++
        if (step <= 5) setCurrentStep(step)
      }, 1400)

      let targetChatId = activeChatId

      // Auto-create project and chat if user asks from landing page
      if (!targetChatId) {
        let projId = activeProjectId
        if (!projId) {
          const newProj = await createProject("Research Workspace", queryText.slice(0, 30))
          projId = newProj.id
          await loadProjectsList()
        }
        const newChat = await createChat(projId, queryText.slice(0, 25), mode)
        await loadChatsForProject(projId)
        targetChatId = newChat.id
        setActiveProjectId(projId)
        setActiveChatId(targetChatId)
      }

      // Optimistically add user message to screen immediately
      setMessages(prev => [
        ...prev,
        { id: `temp-user-${Date.now()}`, role: "user", content: queryText }
      ])
      setTopic("")

      // Send to backend
      await sendChatMessage(targetChatId, queryText, mode)

      clearInterval(interval)
      setCurrentStep(5)

      // Fetch official updated chat messages from backend database
      const detail = await fetchChatDetail(targetChatId)
      setMessages(detail.messages || [])

    } catch (err) {
      console.error("Generation error:", err)
    } finally {
      setLoading(false)
      setCurrentStep(-1)
    }
  }

  const handleGlobalFeedback = async (type) => {
    try {
      await submitGlobalFeedback("research", type)
      setGlobalFeedback(type)
    } catch (err) {
      console.error(err)
    }
  }

  const handleTopicChange = (e) => {
    setTopic(e.target.value)
    setCharCount(e.target.value.length)
  }

  const setTurnTab = (msgId, tabKey) => {
    setTurnActiveTabs(prev => ({ ...prev, [msgId]: tabKey }))
  }

  /* Search navigation handler */
  const handleSearchNavigate = (type, item) => {
    if (type === "project") {
      handleSelectProject(item.id)
    } else if (type === "chat") {
      const projId = item.project_id
      if (projId) {
        handleSelectChat(projId, item.id)
      }
    } else if (type === "message") {
      const chatId = item.chat_id
      if (chatId) {
        // Try to find the project for this chat and navigate
        setActiveChatId(chatId)
        fetchChatDetail(chatId).then(detail => {
          setMessages(detail.messages || [])
        })
      }
    }
  }

  const isChatActive = Boolean(activeChatId || messages.length > 0 || loading)

  return (
    <div className="min-h-screen text-white overflow-x-hidden" style={{ background: 'var(--bg-deep)' }}>

      {/* ─── AMBIENT BACKGROUND ─── */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        <div className="ambient-orb orb-1" />
        <div className="ambient-orb orb-2" />
        <div className="ambient-orb orb-3" />
        <div className="absolute inset-0 neural-bg opacity-60" />
        <div className="absolute inset-0" style={{
          background: 'radial-gradient(ellipse 120% 80% at 50% 0%, transparent 40%, rgba(5,8,16,0.8) 100%)'
        }} />
      </div>

      {/* ─── GLOBAL SEARCH MODAL ─── */}
      <SearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        onNavigate={handleSearchNavigate}
      />

      {/* ─── STICKY NAVBAR ─── */}
      <nav className={`sticky top-0 z-50 navbar-glass ${scrolled ? "scrolled" : ""}`}
           style={{ height: 'var(--nav-height)' }}>
        <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">

          {/* LEFT — logo + brand */}
          <div className="flex items-center gap-4 cursor-pointer" onClick={() => { setActiveChatId(null); setMessages([]); setShowKnowledgeGraph(false); }}>
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

            {/* Search Button */}
            <button
              onClick={() => setSearchOpen(true)}
              className="nav-action-btn"
              title="Search (Ctrl+K)"
            >
              🔍 <span className="hidden sm:inline text-xs">Search</span>
              <kbd className="nav-kbd">⌘K</kbd>
            </button>

            {/* Knowledge Graph Toggle */}
            <button
              onClick={() => setShowKnowledgeGraph(!showKnowledgeGraph)}
              className={`nav-action-btn ${showKnowledgeGraph ? "active" : ""}`}
              title="Knowledge Graph"
            >
              🧠 <span className="hidden sm:inline text-xs">Graph</span>
            </button>

            {/* Dashboard Link */}
            <a
              href="/dashboard"
              className="nav-action-btn"
              title="Research Dashboard"
            >
              📊 <span className="hidden sm:inline text-xs">Dashboard</span>
            </a>

            <a
              href="/guide"
              className="nav-action-btn"
            >
              📖 <span className="hidden sm:inline text-xs">Guide</span>
            </a>

            <div className="hidden sm:flex items-center gap-2 counter-badge px-4 py-2 rounded-full">
              <span className="text-zinc-400">
                {mode === "fast" ? "⚡" : mode === "parallel" ? "🔄" : "🧠"}
              </span>
              <span className="text-zinc-300 text-xs capitalize"
                    style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
                {mode} mode
              </span>
            </div>

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

            {/* Theme Toggle */}
            <ThemeToggle />
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 h-px"
             style={{
               background: 'linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.2) 30%, rgba(6,182,212,0.15) 50%, rgba(139,92,246,0.2) 70%, transparent 100%)'
             }} />
      </nav>

      {/* ─── WORKSPACE LAYOUT WITH SIDEBAR ─── */}
      <div className="app-workspace-layout">
        <Sidebar
          projects={projects}
          activeProjectId={activeProjectId}
          activeChatId={activeChatId}
          expandedProjects={expandedProjects}
          projectChatsMap={projectChatsMap}
          onSelectProject={handleSelectProject}
          onSelectChat={handleSelectChat}
          onCreateProject={handleCreateProject}
          onDeleteProject={handleDeleteProject}
          onCreateChat={handleCreateChat}
          onDeleteChat={handleDeleteChat}
          isOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        {/* ─── MAIN WORKSPACE CONTENT ─── */}
        <div className="flex-1 max-w-[1400px] mx-auto px-6 sm:px-8 md:px-10 py-10">

          {/* ─── KNOWLEDGE GRAPH VIEW ─── */}
          {showKnowledgeGraph && (
            <KnowledgeGraph isVisible={showKnowledgeGraph} />
          )}

          {/* ─── LANDING PAGE HERO SECTION (Shown when no chat is active) ─── */}
          {!isChatActive && !showKnowledgeGraph && (
            <div className="mb-16 relative overflow-hidden">
              <div className="grid lg:grid-cols-1 2xl:grid-cols-[1fr_600px] gap-16 items-center">
                <div>
                  <div className="inline-flex items-center gap-3 hero-badge px-5 py-2.5 rounded-full mb-8">
                    <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
                    <span className="text-cyan-300 text-xs tracking-widest uppercase" style={{ fontFamily: 'var(--font-display)' }}>
                      Multi-Agent AI Research Platform v2.0
                    </span>
                  </div>

                  <h2 className="hero-title font-black leading-[0.98] mb-6" style={{ fontSize: 'clamp(2.8rem, 6vw, 5.5rem)', fontFamily: 'var(--font-display)' }}>
                    <span className="hero-title-glow">Neural</span><br />
                    <span className="gradient-text-animated">Research</span><br />
                    <span className="hero-title-glow">Intelligence</span><br />
                    <span className="gradient-text-animated">Engine</span>
                  </h2>

                  <p className="text-zinc-400 text-lg leading-8 max-w-xl mb-8 font-light">
                    Adaptive multi-agent synthesis, semantic retrieval, cross-paper reasoning, intelligent clustering, and persistent chat history memory.
                  </p>

                  <div className="flex flex-wrap gap-3">
                    {[
                      { label: "Agents", value: "8+" },
                      { label: "Memory", value: "SQLite" },
                      { label: "Modes", value: "3" },
                      { label: "Latency", value: "< 7s" },
                    ].map((stat) => (
                      <div key={stat.label} className="flex items-center gap-2 px-4 py-2 rounded-full border border-white/5 bg-transparent backdrop-blur-xl">
                        <span className="text-zinc-300 text-sm font-semibold">{stat.value}</span>
                        <span className="text-zinc-600 text-xs">{stat.label}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* ARCHITECTURE GRAPH IFRAME */}
                <div className="relative overflow-hidden rounded-[32px] border border-white/5 bg-black/40 backdrop-blur-xl shadow-2xl">
                  <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                      <span className="text-xs uppercase tracking-widest text-cyan-300 font-mono">Neural Architecture</span>
                    </div>
                    <span className="text-xs text-zinc-500 uppercase font-mono">Live System</span>
                  </div>
                  <iframe src="/codegraph.html" title="Architecture Graph" className="w-full h-[400px]" />
                </div>
              </div>
            </div>
          )}

          {/* ─── CHAT SESSION TURN STREAM (Renders prior turns + live responses) ─── */}
          {messages.length > 0 && (
            <div className="chat-turns-stream mb-10 space-y-8">
              <div className="flex items-center justify-between pb-2 border-b border-white/5">
                <h4 className="text-xs font-mono uppercase text-cyan-400 tracking-wider flex items-center gap-2">
                  <span>💬</span> Session Stream ({messages.length} turns recorded)
                </h4>
              </div>

              {messages.map((msg) => {
                const isUser = msg.role === "user"
                const research = msg.research_data
                const isFollowup = research?.followup === true
                const activeTurnTab = turnActiveTabs[msg.id] || "summary"

                if (isUser) {
                  return (
                    <div key={msg.id} className="chat-turn-user">
                      <span className="font-bold text-cyan-300">You:</span> {msg.content}
                    </div>
                  )
                }

                /* ── Follow-up response (lightweight, no tabs) ── */
                if (isFollowup) {
                  return (
                    <div key={msg.id} className="glass-card rounded-[32px] p-8 border-l-4 border-l-emerald-400 space-y-4">
                      <div className="flex items-center gap-3 pb-3 border-b border-white/5">
                        <div className="w-8 h-8 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
                          <span className="text-emerald-300 text-sm">💬</span>
                        </div>
                        <div>
                          <h4 className="text-white font-bold text-base" style={{ fontFamily: 'var(--font-display)' }}>
                            Follow-up Response
                          </h4>
                          <p className="text-emerald-400 text-xs font-mono">Conversational • context-aware reasoning</p>
                        </div>
                      </div>
                      <RichTextRenderer text={research?.content || msg.content} type="default" />
                    </div>
                  )
                }

                /* ── Full research response (with tabs) ── */
                return (
                  <div key={msg.id} className="glass-card rounded-[32px] p-8 border-l-4 border-l-cyan-400 space-y-6">
                    {/* ASSISTANT HEADER */}
                    <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-white/5">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center">
                          <span className="text-cyan-300 text-sm">🤖</span>
                        </div>
                        <div>
                          <h4 className="text-white font-bold text-base" style={{ fontFamily: 'var(--font-display)' }}>
                            Synaptrix AI Research Intelligence
                          </h4>
                          <p className="text-zinc-500 text-xs font-mono">
                            {research?.mode_used ? `${research.mode_used} mode` : "multi-agent reasoning"} • {research?.top_papers?.length || 0} papers analyzed
                          </p>
                        </div>
                      </div>

                      {/* Export Menu (replaces old PDF-only button) */}
                      {research && (
                        <ExportMenu
                          research={research}
                          onDownloadPDF={downloadResearchPDF}
                        />
                      )}
                    </div>

                    {/* TURN TABS SELECTOR (Summary, Analysis, Gaps, Synthesis, Source Papers) */}
                    {research && (
                      <div className="flex flex-wrap gap-2 pt-1">
                        {Object.keys(TAB_META).map((tabKey) => {
                          const meta = TAB_META[tabKey]
                          const isActive = activeTurnTab === tabKey
                          return (
                            <button
                              key={tabKey}
                              onClick={() => setTurnTab(msg.id, tabKey)}
                              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
                                isActive ? "bg-cyan-500/20 border border-cyan-500/40 text-cyan-200" : "bg-white/5 text-zinc-400 hover:text-white"
                              }`}
                            >
                              <span>{meta.icon}</span>
                              <span className="capitalize">{meta.label}</span>
                            </button>
                          )
                        })}
                      </div>
                    )}

                    {/* TAB CONTENT DISPLAY */}
                    {research ? (
                      <div className="pt-2">
                        {activeTurnTab === "summary" && (
                          <RichTextRenderer text={research.summary || msg.content} type="summary" />
                        )}
                        {activeTurnTab === "analysis" && (
                          <RichTextRenderer text={research.analysis || "No analysis generated."} type="analysis" />
                        )}
                        {activeTurnTab === "gaps" && (
                          <RichTextRenderer text={research.gaps || "No research gaps found."} type="gaps" />
                        )}
                        {activeTurnTab === "synthesis" && (
                          <RichTextRenderer text={research.synthesis || "No cluster synthesis available."} type="synthesis" />
                        )}
                        {activeTurnTab === "papers" && (
                          <div className="grid grid-cols-1 gap-6 mt-4">
                            {(research.top_papers || []).map((paper, idx) => (
                              <PaperCard key={idx} paper={paper} />
                            ))}
                          </div>
                        )}
                      </div>
                    ) : (
                      /* Fallback raw text content if no research_data object */
                      <div className="pt-2">
                        <RichTextRenderer text={msg.content} type="default" />
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}

          {/* ─── LIVE PIPELINE LOADING CARD IN CHAT STREAM ─── */}
          {loading && (
            <div className="glass-card rounded-[32px] p-8 border-l-4 border-l-blue-500 mb-10 space-y-4 animate-pulse">
              <div className="flex items-center gap-3">
                <span className="animate-spin text-xl text-cyan-400">⚡</span>
                <div>
                  <h4 className="text-white font-bold text-base">Synaptrix AI is Synthesizing Research...</h4>
                  <p className="text-zinc-400 text-xs font-mono">Running multi-agent retrieval, embedding search & LLM reasoning</p>
                </div>
              </div>
              <PipelineStatus currentStep={currentStep} />
            </div>
          )}

          <div ref={chatStreamEndRef} />

          {/* ─── INPUT PROMPT PANEL (Always accessible at bottom for follow-ups) ─── */}
          <div className="anim-fade-up input-panel rounded-[36px] p-8 md:p-10 mb-8">
            <div className="input-top-bar flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl flex items-center justify-center"
                     style={{ background: 'rgba(59,130,246,0.1)', border: '1px solid rgba(59,130,246,0.2)' }}>
                  <span className="text-blue-400 text-sm">💡</span>
                </div>
                <div>
                  <h3 className="text-white font-semibold text-base" style={{ fontFamily: 'var(--font-display)' }}>
                    {isChatActive ? "Ask Follow-up or Deepen Research Session" : "Start Research Intelligence Query"}
                  </h3>
                  <p className="text-zinc-500 text-xs">
                    {isChatActive ? "Persistent context memory active • follow-up questions auto-detected" : "Enter a research query below to transition into Chat Mode"}
                  </p>
                </div>
              </div>

              {/* MODE SELECTOR */}
              <div className="flex items-center gap-2 p-1.5 rounded-full"
                   style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.06)' }}>
                {["fast", "parallel", "research"].map((m) => (
                  <button
                    key={m}
                    onClick={() => setMode(m)}
                    className={`px-3 py-1.5 rounded-full text-xs font-medium capitalize transition-all duration-300 ${
                      mode === m ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30" : "text-zinc-400 hover:text-white"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            {/* TEXTAREA INPUT */}
            <div className="relative">
              <textarea
                value={topic}
                onChange={handleTopicChange}
                placeholder="Enter research topic, paper title, or follow-up question (e.g. Compare transformer architectures vs Mamba for long-context memory)..."
                rows={3}
                className="w-full ai-textarea p-5 text-zinc-100 placeholder-zinc-500 text-base"
              />
              
              <div className="flex items-center justify-between mt-4">
                <span className="text-xs text-zinc-500 font-mono">
                  {charCount} characters
                </span>
                <button
                  onClick={handleGenerate}
                  disabled={loading || !topic.trim()}
                  className="btn-generate px-8 py-3.5 rounded-2xl font-bold text-sm text-white flex items-center gap-3 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <span className="animate-spin text-base">⏳</span>
                      <span>Processing Neural Pipeline...</span>
                    </>
                  ) : (
                    <>
                      <span>Send Research Prompt</span>
                      <span className="text-base">🚀</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home