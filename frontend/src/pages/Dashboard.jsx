import { useState, useEffect, useRef } from "react"
import { useTheme } from "../components/ThemeProvider"
import { fetchDashboardStats } from "../services/api"

/* ═══════════════════════════════════════════
   CANVAS CHART HELPERS
═══════════════════════════════════════════ */

function drawDonutChart(canvas, data, colors, isDark) {
  if (!canvas || !data?.length) return
  const ctx = canvas.getContext("2d")
  const w = canvas.width
  const h = canvas.height
  const cx = w / 2
  const cy = h / 2
  const r = Math.min(w, h) / 2 - 20
  const innerR = r * 0.6

  ctx.clearRect(0, 0, w, h)

  const total = data.reduce((s, d) => s + d.value, 0)
  if (total === 0) return

  let startAngle = -Math.PI / 2

  data.forEach((d, i) => {
    const sliceAngle = (d.value / total) * Math.PI * 2
    ctx.beginPath()
    ctx.arc(cx, cy, r, startAngle, startAngle + sliceAngle)
    ctx.arc(cx, cy, innerR, startAngle + sliceAngle, startAngle, true)
    ctx.closePath()
    ctx.fillStyle = colors[i % colors.length]
    ctx.fill()
    startAngle += sliceAngle
  })

  // Center text
  ctx.fillStyle = isDark ? "#f8fafc" : "#0f172a"
  ctx.font = "bold 22px Inter, system-ui"
  ctx.textAlign = "center"
  ctx.textBaseline = "middle"
  ctx.fillText(total, cx, cy - 8)
  ctx.font = "11px Inter, system-ui"
  ctx.fillStyle = isDark ? "#94a3b8" : "#64748b"
  ctx.fillText("total", cx, cy + 12)
}

function drawBarChart(canvas, data, color, isDark) {
  if (!canvas || !data?.length) return
  const ctx = canvas.getContext("2d")
  const w = canvas.width
  const h = canvas.height
  const padding = { top: 20, right: 20, bottom: 40, left: 50 }
  const chartW = w - padding.left - padding.right
  const chartH = h - padding.top - padding.bottom

  ctx.clearRect(0, 0, w, h)

  const maxVal = Math.max(...data.map(d => d.value), 1)
  const barW = Math.min(40, (chartW / data.length) * 0.7)
  const gap = (chartW - barW * data.length) / (data.length + 1)

  // Grid lines
  ctx.strokeStyle = isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)"
  ctx.lineWidth = 1
  for (let i = 0; i <= 4; i++) {
    const y = padding.top + (chartH / 4) * i
    ctx.beginPath()
    ctx.moveTo(padding.left, y)
    ctx.lineTo(w - padding.right, y)
    ctx.stroke()
  }

  // Bars
  data.forEach((d, i) => {
    const barH = (d.value / maxVal) * chartH
    const x = padding.left + gap + i * (barW + gap)
    const y = padding.top + chartH - barH

    // Gradient bar
    const grad = ctx.createLinearGradient(x, y, x, y + barH)
    grad.addColorStop(0, color)
    grad.addColorStop(1, color + "60")
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.moveTo(x + 4, y)
    ctx.lineTo(x + barW - 4, y)
    ctx.quadraticCurveTo(x + barW, y, x + barW, y + 4)
    ctx.lineTo(x + barW, y + barH)
    ctx.lineTo(x, y + barH)
    ctx.lineTo(x, y + 4)
    ctx.quadraticCurveTo(x, y, x + 4, y)
    ctx.fill()

    // Label
    ctx.fillStyle = isDark ? "#94a3b8" : "#64748b"
    ctx.font = "9px Inter, system-ui"
    ctx.textAlign = "center"
    const label = d.label.length > 10 ? d.label.slice(0, 8) + ".." : d.label
    ctx.fillText(label, x + barW / 2, h - padding.bottom + 16)
  })
}

function drawLineChart(canvas, data, color, isDark) {
  if (!canvas || !data?.length) return
  const ctx = canvas.getContext("2d")
  const w = canvas.width
  const h = canvas.height
  const padding = { top: 20, right: 20, bottom: 40, left: 40 }
  const chartW = w - padding.left - padding.right
  const chartH = h - padding.top - padding.bottom

  ctx.clearRect(0, 0, w, h)

  const maxVal = Math.max(...data.map(d => d.count), 1)

  // Grid
  ctx.strokeStyle = isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)"
  for (let i = 0; i <= 4; i++) {
    const y = padding.top + (chartH / 4) * i
    ctx.beginPath()
    ctx.moveTo(padding.left, y)
    ctx.lineTo(w - padding.right, y)
    ctx.stroke()
  }

  if (data.length < 2) return

  // Area fill
  const stepX = chartW / (data.length - 1)
  ctx.beginPath()
  ctx.moveTo(padding.left, padding.top + chartH)
  data.forEach((d, i) => {
    const x = padding.left + i * stepX
    const y = padding.top + chartH - (d.count / maxVal) * chartH
    ctx.lineTo(x, y)
  })
  ctx.lineTo(padding.left + (data.length - 1) * stepX, padding.top + chartH)
  ctx.closePath()
  const areaGrad = ctx.createLinearGradient(0, padding.top, 0, h)
  areaGrad.addColorStop(0, color + "30")
  areaGrad.addColorStop(1, "transparent")
  ctx.fillStyle = areaGrad
  ctx.fill()

  // Line
  ctx.beginPath()
  data.forEach((d, i) => {
    const x = padding.left + i * stepX
    const y = padding.top + chartH - (d.count / maxVal) * chartH
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  })
  ctx.strokeStyle = color
  ctx.lineWidth = 2.5
  ctx.lineJoin = "round"
  ctx.stroke()

  // Dots
  data.forEach((d, i) => {
    const x = padding.left + i * stepX
    const y = padding.top + chartH - (d.count / maxVal) * chartH
    ctx.beginPath()
    ctx.arc(x, y, 3, 0, Math.PI * 2)
    ctx.fillStyle = color
    ctx.fill()
  })

  // Date labels (show every Nth)
  const labelEvery = Math.max(1, Math.floor(data.length / 6))
  ctx.fillStyle = isDark ? "#64748b" : "#94a3b8"
  ctx.font = "9px Inter, system-ui"
  ctx.textAlign = "center"
  data.forEach((d, i) => {
    if (i % labelEvery === 0) {
      const x = padding.left + i * stepX
      const label = d.date?.slice(5) || ""
      ctx.fillText(label, x, h - 8)
    }
  })
}

/* ═══════════════════════════════════════════
   DASHBOARD PAGE
═══════════════════════════════════════════ */

const Dashboard = () => {
  const { isDark } = useTheme()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  const donutRef = useRef(null)
  const barRef = useRef(null)
  const lineRef = useRef(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await fetchDashboardStats()
        setStats(data)
      } catch (err) {
        console.error("Dashboard stats error:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  /* Render charts when data is ready */
  useEffect(() => {
    if (!stats) return

    // Donut: mode distribution
    if (donutRef.current && stats.mode_distribution) {
      const data = Object.entries(stats.mode_distribution).map(([k, v]) => ({ label: k, value: v }))
      drawDonutChart(donutRef.current, data, ["#06b6d4", "#8b5cf6", "#10b981", "#f59e0b"], isDark)
    }

    // Bar: top topics
    if (barRef.current && stats.top_topics) {
      const topicsArr = Array.isArray(stats.top_topics)
        ? stats.top_topics
        : Object.entries(stats.top_topics).map(([topic, count]) => ({ topic, count }))
      const data = topicsArr.slice(0, 8).map(t => ({ label: t.topic || t[0], value: t.count || t[1] }))
      drawBarChart(barRef.current, data, "#3b82f6", isDark)
    }

    // Line: activity timeline
    if (lineRef.current && stats.activity_timeline) {
      drawLineChart(lineRef.current, stats.activity_timeline, "#06b6d4", isDark)
    }
  }, [stats, isDark])

  if (loading) {
    return (
      <div className="dashboard-loading">
        <span className="animate-spin text-3xl">⚡</span>
        <p>Loading dashboard analytics...</p>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="dashboard-loading">
        <p>Failed to load dashboard data.</p>
      </div>
    )
  }

  return (
    <div className="dashboard-page">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Research Dashboard</h1>
          <p className="dashboard-subtitle">Analytics & insights across your research workspace</p>
        </div>
      </div>

      {/* Stat Cards Row */}
      <div className="dashboard-stats-row">
        {[
          { label: "Projects", value: stats.total_projects || 0, icon: "📁", color: "#3b82f6" },
          { label: "Chat Sessions", value: stats.total_chats || 0, icon: "💬", color: "#06b6d4" },
          { label: "Messages", value: stats.total_messages || 0, icon: "📝", color: "#8b5cf6" },
          { label: "Papers Analyzed", value: stats.total_papers || 0, icon: "📄", color: "#10b981" },
        ].map((s) => (
          <div key={s.label} className="dashboard-stat-card">
            <div className="stat-card-icon" style={{ background: s.color + "20", borderColor: s.color + "40" }}>
              <span>{s.icon}</span>
            </div>
            <div className="stat-card-value" style={{ color: s.color }}>{s.value}</div>
            <div className="stat-card-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="dashboard-charts-row">
        {/* Mode Distribution Donut */}
        <div className="dashboard-chart-card">
          <h3 className="chart-title">Mode Distribution</h3>
          <p className="chart-subtitle">Research pipeline modes used</p>
          <div className="chart-canvas-wrapper">
            <canvas ref={donutRef} width={250} height={250} />
          </div>
          <div className="chart-legend">
            {stats.mode_distribution && Object.entries(stats.mode_distribution).map(([mode, count], i) => (
              <span key={mode} className="legend-item">
                <span className="legend-dot" style={{ background: ["#06b6d4", "#8b5cf6", "#10b981", "#f59e0b"][i] }} />
                {mode}: {count}
              </span>
            ))}
          </div>
        </div>

        {/* Top Topics Bar Chart */}
        <div className="dashboard-chart-card wide">
          <h3 className="chart-title">Top Research Topics</h3>
          <p className="chart-subtitle">Most frequently researched areas</p>
          <div className="chart-canvas-wrapper">
            <canvas ref={barRef} width={500} height={250} />
          </div>
        </div>
      </div>

      {/* Activity Timeline */}
      <div className="dashboard-chart-card full-width">
        <h3 className="chart-title">Research Activity Timeline</h3>
        <p className="chart-subtitle">Messages over the last 30 days</p>
        <div className="chart-canvas-wrapper wide-chart">
          <canvas ref={lineRef} width={900} height={220} />
        </div>
      </div>

      {/* Recent Activity Feed */}
      <div className="dashboard-chart-card full-width">
        <h3 className="chart-title">Recent Activity</h3>
        <p className="chart-subtitle">Latest research interactions</p>
        <div className="recent-activity-list">
          {(stats.recent_activity || []).map((item, i) => (
            <div key={i} className="activity-item">
              <span className="activity-icon">{item.role === "user" ? "👤" : "🤖"}</span>
              <div className="activity-content">
                <span className="activity-text">{(item.content || "").slice(0, 120)}</span>
                <span className="activity-meta">
                  {item.role} • {item.created_at ? new Date(item.created_at * 1000).toLocaleDateString() : ""}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
