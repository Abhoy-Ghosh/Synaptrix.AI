import { useState, useEffect, useRef, useCallback } from "react"
import { fetchKnowledgeGraph } from "../services/api"

/* ═══════════════════════════════════════════
   FORCE-DIRECTED KNOWLEDGE GRAPH (Canvas API)
═══════════════════════════════════════════ */

const KnowledgeGraph = ({ isVisible }) => {
  const canvasRef = useRef(null)
  const nodesRef = useRef([])
  const edgesRef = useRef([])
  const animRef = useRef(null)
  const dragRef = useRef(null)
  const hoverRef = useRef(null)
  const offsetRef = useRef({ x: 0, y: 0 })
  const scaleRef = useRef(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [stats, setStats] = useState({ nodes: 0, edges: 0 })

  /* Color palette for groups */
  const GROUP_COLORS = [
    "#06b6d4", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444",
    "#ec4899", "#6366f1", "#14b8a6", "#f97316", "#84cc16"
  ]

  const getGroupColor = (group, groups) => {
    const idx = groups.indexOf(group)
    return GROUP_COLORS[idx % GROUP_COLORS.length]
  }

  /* Fetch graph data */
  useEffect(() => {
    if (!isVisible) return

    const fetchData = async () => {
      setLoading(true)
      try {
        const data = await fetchKnowledgeGraph()

        if (!data.nodes?.length) {
          setError("No research data yet. Run some queries first!")
          setLoading(false)
          return
        }

        const groups = [...new Set(data.nodes.map(n => n.group))]

        /* Position nodes randomly */
        const canvas = canvasRef.current
        const w = canvas?.width || 800
        const h = canvas?.height || 600

        const nodes = data.nodes.map((n, i) => ({
          ...n,
          x: w / 2 + (Math.random() - 0.5) * w * 0.6,
          y: h / 2 + (Math.random() - 0.5) * h * 0.6,
          vx: 0,
          vy: 0,
          radius: n.type === "topic" ? 22 : Math.max(8, Math.min(18, Math.sqrt(n.citations || 1) * 2)),
          color: getGroupColor(n.group, groups),
        }))

        const nodeMap = {}
        nodes.forEach(n => nodeMap[n.id] = n)

        const edges = (data.edges || [])
          .filter(e => nodeMap[e.source] && nodeMap[e.target])
          .map(e => ({
            ...e,
            sourceNode: nodeMap[e.source],
            targetNode: nodeMap[e.target],
          }))

        nodesRef.current = nodes
        edgesRef.current = edges
        setStats({ nodes: nodes.length, edges: edges.length })
        setLoading(false)
      } catch (err) {
        console.error("Knowledge graph fetch error:", err)
        setError("Failed to load knowledge graph data")
        setLoading(false)
      }
    }

    fetchData()
  }, [isVisible])

  /* Force simulation tick */
  const simulate = useCallback(() => {
    const nodes = nodesRef.current
    const edges = edgesRef.current
    if (!nodes.length) return

    const canvas = canvasRef.current
    if (!canvas) return

    const w = canvas.width
    const h = canvas.height
    const centerX = w / 2
    const centerY = h / 2

    /* Forces */
    // Repulsion between all nodes
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[j].x - nodes[i].x
        const dy = nodes[j].y - nodes[i].y
        const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 1)
        const force = 800 / (dist * dist)
        const fx = (dx / dist) * force
        const fy = (dy / dist) * force
        nodes[i].vx -= fx
        nodes[i].vy -= fy
        nodes[j].vx += fx
        nodes[j].vy += fy
      }
    }

    // Attraction along edges
    edges.forEach(e => {
      const dx = e.targetNode.x - e.sourceNode.x
      const dy = e.targetNode.y - e.sourceNode.y
      const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 1)
      const force = (dist - 120) * 0.01 * (e.weight || 0.5)
      const fx = (dx / dist) * force
      const fy = (dy / dist) * force
      e.sourceNode.vx += fx
      e.sourceNode.vy += fy
      e.targetNode.vx -= fx
      e.targetNode.vy -= fy
    })

    // Center gravity
    nodes.forEach(n => {
      n.vx += (centerX - n.x) * 0.001
      n.vy += (centerY - n.y) * 0.001
    })

    // Apply velocity with damping
    nodes.forEach(n => {
      if (dragRef.current && dragRef.current.id === n.id) return
      n.vx *= 0.85
      n.vy *= 0.85
      n.x += n.vx
      n.y += n.vy
      // Keep in bounds
      n.x = Math.max(n.radius, Math.min(w - n.radius, n.x))
      n.y = Math.max(n.radius, Math.min(h - n.radius, n.y))
    })
  }, [])

  /* Render loop */
  useEffect(() => {
    if (!isVisible || loading) return

    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")

    const render = () => {
      simulate()

      const w = canvas.width
      const h = canvas.height
      const nodes = nodesRef.current
      const edges = edgesRef.current

      ctx.clearRect(0, 0, w, h)

      /* Draw edges */
      edges.forEach(e => {
        const alpha = Math.min(0.6, (e.weight || 0.3) * 0.8)
        ctx.beginPath()
        ctx.moveTo(e.sourceNode.x, e.sourceNode.y)
        ctx.lineTo(e.targetNode.x, e.targetNode.y)
        ctx.strokeStyle = `rgba(148, 163, 184, ${alpha})`
        ctx.lineWidth = Math.max(0.5, (e.weight || 0.3) * 2.5)
        ctx.stroke()
      })

      /* Draw nodes */
      nodes.forEach(n => {
        const isHovered = hoverRef.current?.id === n.id

        // Glow
        if (isHovered || n.type === "topic") {
          ctx.beginPath()
          ctx.arc(n.x, n.y, n.radius + 8, 0, Math.PI * 2)
          const glow = ctx.createRadialGradient(n.x, n.y, n.radius, n.x, n.y, n.radius + 8)
          glow.addColorStop(0, n.color + "40")
          glow.addColorStop(1, "transparent")
          ctx.fillStyle = glow
          ctx.fill()
        }

        // Node body
        ctx.beginPath()
        if (n.type === "topic") {
          // Hexagon
          for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 6
            const px = n.x + n.radius * Math.cos(angle)
            const py = n.y + n.radius * Math.sin(angle)
            if (i === 0) ctx.moveTo(px, py)
            else ctx.lineTo(px, py)
          }
          ctx.closePath()
        } else {
          ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2)
        }

        ctx.fillStyle = isHovered ? n.color : n.color + "cc"
        ctx.fill()
        ctx.strokeStyle = n.color
        ctx.lineWidth = isHovered ? 2 : 1
        ctx.stroke()

        // Label for topics and hovered nodes
        if (n.type === "topic" || isHovered) {
          ctx.fillStyle = "#f8fafc"
          ctx.font = `${isHovered ? "bold " : ""}${n.type === "topic" ? 11 : 10}px Inter, system-ui`
          ctx.textAlign = "center"
          ctx.textBaseline = "top"
          const label = n.label.length > 25 ? n.label.slice(0, 22) + "..." : n.label
          ctx.fillText(label, n.x, n.y + n.radius + 6)
        }
      })

      /* Tooltip for hovered node */
      if (hoverRef.current) {
        const n = hoverRef.current
        const tooltipW = 220
        const tooltipH = n.type === "topic" ? 40 : 60
        let tx = n.x + n.radius + 12
        let ty = n.y - tooltipH / 2

        if (tx + tooltipW > w) tx = n.x - n.radius - tooltipW - 12
        if (ty < 0) ty = 4
        if (ty + tooltipH > h) ty = h - tooltipH - 4

        ctx.fillStyle = "rgba(15, 23, 42, 0.92)"
        ctx.strokeStyle = "rgba(148, 163, 184, 0.2)"
        ctx.lineWidth = 1

        const r = 8
        ctx.beginPath()
        ctx.moveTo(tx + r, ty)
        ctx.lineTo(tx + tooltipW - r, ty)
        ctx.quadraticCurveTo(tx + tooltipW, ty, tx + tooltipW, ty + r)
        ctx.lineTo(tx + tooltipW, ty + tooltipH - r)
        ctx.quadraticCurveTo(tx + tooltipW, ty + tooltipH, tx + tooltipW - r, ty + tooltipH)
        ctx.lineTo(tx + r, ty + tooltipH)
        ctx.quadraticCurveTo(tx, ty + tooltipH, tx, ty + tooltipH - r)
        ctx.lineTo(tx, ty + r)
        ctx.quadraticCurveTo(tx, ty, tx + r, ty)
        ctx.closePath()
        ctx.fill()
        ctx.stroke()

        ctx.fillStyle = "#e2e8f0"
        ctx.font = "bold 11px Inter, system-ui"
        ctx.textAlign = "left"
        ctx.textBaseline = "top"
        const title = n.label.length > 28 ? n.label.slice(0, 25) + "..." : n.label
        ctx.fillText(title, tx + 10, ty + 10)

        if (n.type !== "topic") {
          ctx.fillStyle = "#94a3b8"
          ctx.font = "10px Inter, system-ui"
          ctx.fillText(`${n.citations || 0} citations • ${n.group || ""}`, tx + 10, ty + 28)
        }
      }

      animRef.current = requestAnimationFrame(render)
    }

    animRef.current = requestAnimationFrame(render)
    return () => cancelAnimationFrame(animRef.current)
  }, [isVisible, loading, simulate])

  /* Resize canvas */
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const resize = () => {
      const parent = canvas.parentElement
      if (parent) {
        canvas.width = parent.clientWidth
        canvas.height = parent.clientHeight
      }
    }

    resize()
    window.addEventListener("resize", resize)
    return () => window.removeEventListener("resize", resize)
  }, [isVisible])

  /* Mouse interactions */
  const getNodeAt = (x, y) => {
    return nodesRef.current.find(n => {
      const dx = n.x - x
      const dy = n.y - y
      return Math.sqrt(dx * dx + dy * dy) <= n.radius + 4
    })
  }

  const handleMouseMove = (e) => {
    const rect = canvasRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    if (dragRef.current) {
      dragRef.current.x = x - offsetRef.current.x
      dragRef.current.y = y - offsetRef.current.y
      dragRef.current.vx = 0
      dragRef.current.vy = 0
    } else {
      const node = getNodeAt(x, y)
      hoverRef.current = node || null
      canvasRef.current.style.cursor = node ? "pointer" : "default"
    }
  }

  const handleMouseDown = (e) => {
    const rect = canvasRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const node = getNodeAt(x, y)
    if (node) {
      dragRef.current = node
      offsetRef.current = { x: x - node.x, y: y - node.y }
    }
  }

  const handleMouseUp = () => {
    dragRef.current = null
  }

  if (!isVisible) return null

  return (
    <div className="knowledge-graph-container">
      {/* Header */}
      <div className="kg-header">
        <div className="kg-header-left">
          <span className="kg-icon">🧠</span>
          <div>
            <h3 className="kg-title">Knowledge Graph</h3>
            <p className="kg-subtitle">{stats.nodes} nodes • {stats.edges} connections</p>
          </div>
        </div>
        <div className="kg-legend">
          <span className="kg-legend-item"><span style={{ background: "#06b6d4" }} className="kg-dot" /> Papers</span>
          <span className="kg-legend-item"><span style={{ background: "#8b5cf6" }} className="kg-dot hex" /> Topics</span>
        </div>
      </div>

      {/* Canvas */}
      <div className="kg-canvas-wrapper">
        {loading && (
          <div className="kg-loading">
            <span className="animate-spin text-2xl">⚡</span>
            <span>Loading research graph...</span>
          </div>
        )}

        {error && (
          <div className="kg-error">
            <span>⊘</span>
            <span>{error}</span>
          </div>
        )}

        <canvas
          ref={canvasRef}
          onMouseMove={handleMouseMove}
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          className="kg-canvas"
        />
      </div>
    </div>
  )
}

export default KnowledgeGraph
