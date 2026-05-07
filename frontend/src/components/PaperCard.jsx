import { useState } from "react"
import { submitPaperFeedback } from "../services/api"

const PaperCard = ({ paper, index = 0 }) => {

  const [feedbackStatus, setFeedbackStatus] = useState("")
  const [isExpanded, setIsExpanded] = useState(false)

  const handleFeedback = async (type) => {
    try {
      await submitPaperFeedback(paper.title, type)
      setFeedbackStatus(type)
    } catch (err) {
      console.log(err)
    }
  }

  const score = paper.feedback_score || 0
  const scoreColor = score > 0 ? '#86efac' : score < 0 ? '#fca5a5' : '#94a3b8'

  return (
    <div
      className="rounded-[var(--radius-xl)] relative overflow-hidden anim-fade-up card-hover gradient-border"
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
        animationDelay: `${index * 0.1}s`,
      }}
    >
      {/* Background gradient tint */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: index % 2 === 0
            ? 'radial-gradient(ellipse at 0% 0%, rgba(59,130,246,0.04) 0%, transparent 60%)'
            : 'radial-gradient(ellipse at 100% 0%, rgba(139,92,246,0.04) 0%, transparent 60%)',
        }}
      />

      <div className="p-8 relative z-10">

        {/* HEADER */}
        <div className="flex items-start justify-between gap-4 mb-5">
          <h2
            className="text-2xl font-bold leading-snug flex-1"
            style={{
              fontFamily: 'var(--font-display)',
              color: 'var(--text-primary)',
              lineHeight: '1.3',
            }}
          >
            {paper.title}
          </h2>
        </div>

        {/* SOURCE + SCORE */}
        <div className="flex items-center gap-3 mb-7 flex-wrap">
          <span
            className="text-xs font-semibold px-4 py-1.5 rounded-full"
            style={{
              background: 'linear-gradient(135deg, rgba(37,99,235,0.2), rgba(8,145,178,0.2))',
              border: '1px solid rgba(59,130,246,0.25)',
              color: '#93c5fd',
              fontFamily: 'var(--font-display)',
              letterSpacing: '0.05em',
            }}
          >
            {paper.source}
          </span>

          <div
            className="score-badge flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium"
          >
            <span style={{ color: '#fbbf24', fontSize: '12px' }}>★</span>
            <span style={{ color: scoreColor, fontFamily: 'var(--font-display)' }}>
              {score > 0 ? `+${score}` : score}
            </span>
          </div>
        </div>

        {/* ABSTRACT */}
        <div className="mb-7">
          <div className="flex items-center gap-2 mb-3">
            <div
              className="h-px flex-1"
              style={{ background: 'linear-gradient(90deg, rgba(59,130,246,0.3), transparent)' }}
            />
            <span className="section-label">Abstract</span>
            <div
              className="h-px flex-1"
              style={{ background: 'linear-gradient(90deg, transparent, rgba(59,130,246,0.1))' }}
            />
          </div>

          <p className="result-prose text-sm" style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
            {isExpanded
              ? paper.abstract
              : `${paper.abstract?.slice(0, 300)}...`}
          </p>

          {paper.abstract?.length > 300 && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="mt-2 text-xs font-medium transition-colors"
              style={{ color: '#60a5fa' }}
            >
              {isExpanded ? 'Show less ↑' : 'Read more ↓'}
            </button>
          )}
        </div>

        {/* KEY INSIGHTS */}
        {paper.insights?.points?.length > 0 && (
          <div className="mb-7">
            <div className="flex items-center gap-2 mb-4">
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, rgba(6,182,212,0.3), transparent)' }}
              />
              <span className="section-label">Key Insights</span>
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, transparent, rgba(6,182,212,0.1))' }}
              />
            </div>

            <ul className="space-y-2.5">
              {paper.insights.points.map((point, idx) => (
                <li
                  key={idx}
                  className="flex gap-3 text-sm"
                  style={{
                    color: '#cbd5e1',
                    lineHeight: '1.7',
                    animation: `slide-right 0.4s ease both`,
                    animationDelay: `${idx * 0.08}s`,
                  }}
                >
                  <span
                    className="flex-shrink-0 w-5 h-5 rounded-md flex items-center justify-center mt-0.5"
                    style={{
                      background: 'rgba(6,182,212,0.1)',
                      border: '1px solid rgba(6,182,212,0.2)',
                      fontSize: '10px',
                      color: '#22d3ee',
                      fontFamily: 'var(--font-display)',
                    }}
                  >
                    {idx + 1}
                  </span>
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* KEYWORDS */}
        {paper.insights?.keywords?.length > 0 && (
          <div className="mb-7">
            <div className="flex items-center gap-2 mb-4">
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, rgba(139,92,246,0.3), transparent)' }}
              />
              <span className="section-label">Keywords</span>
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, transparent, rgba(139,92,246,0.1))' }}
              />
            </div>

            <div className="flex flex-wrap gap-2">
              {paper.insights.keywords.map((keyword, idx) => (
                <span
                  key={idx}
                  className="keyword-pill text-xs px-3 py-1.5 rounded-full cursor-default"
                  style={{
                    background: 'rgba(139,92,246,0.07)',
                    border: '1px solid rgba(139,92,246,0.15)',
                    color: '#c4b5fd',
                    fontFamily: 'var(--font-body)',
                    animationDelay: `${idx * 0.05}s`,
                  }}
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* WHY IMPORTANT */}
        {paper.insights?.why && (
          <div className="mb-7">
            <div className="flex items-center gap-2 mb-3">
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, rgba(59,130,246,0.3), transparent)' }}
              />
              <span className="section-label">Why Important</span>
              <div
                className="h-px flex-1"
                style={{ background: 'linear-gradient(90deg, transparent, rgba(59,130,246,0.1))' }}
              />
            </div>

            <p
              className="text-sm leading-relaxed"
              style={{
                color: '#94a3b8',
                fontStyle: 'italic',
                borderLeft: '2px solid rgba(59,130,246,0.3)',
                paddingLeft: '12px',
              }}
            >
              {paper.insights.why}
            </p>
          </div>
        )}

        {/* FEEDBACK */}
        <div
          className="pt-6 mt-2"
          style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}
        >
          <p
            className="text-xs mb-4 font-medium"
            style={{
              color: 'var(--text-muted)',
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              fontFamily: 'var(--font-display)',
            }}
          >
            Was this paper useful?
          </p>

          <div className="flex gap-3 flex-wrap">
            <button
              onClick={() => handleFeedback("useful")}
              className="feedback-btn text-sm font-semibold px-5 py-2.5 rounded-xl flex items-center gap-2"
              style={{
                background: feedbackStatus === "useful"
                  ? 'rgba(34,197,94,0.2)'
                  : 'rgba(34,197,94,0.08)',
                border: `1px solid ${feedbackStatus === "useful" ? 'rgba(34,197,94,0.4)' : 'rgba(34,197,94,0.15)'}`,
                color: '#86efac',
                fontFamily: 'var(--font-body)',
              }}
            >
              <span>👍</span>
              <span>Useful</span>
            </button>

            <button
              onClick={() => handleFeedback("not_useful")}
              className="feedback-btn text-sm font-semibold px-5 py-2.5 rounded-xl flex items-center gap-2"
              style={{
                background: feedbackStatus === "not_useful"
                  ? 'rgba(239,68,68,0.2)'
                  : 'rgba(239,68,68,0.08)',
                border: `1px solid ${feedbackStatus === "not_useful" ? 'rgba(239,68,68,0.4)' : 'rgba(239,68,68,0.15)'}`,
                color: '#fca5a5',
                fontFamily: 'var(--font-body)',
              }}
            >
              <span>👎</span>
              <span>Not Useful</span>
            </button>
          </div>

          {feedbackStatus && (
            <p
              className="mt-3 text-xs flex items-center gap-2"
              style={{ color: 'var(--text-muted)' }}
            >
              <span
                className="w-1.5 h-1.5 rounded-full inline-block"
                style={{ background: feedbackStatus === 'useful' ? '#22c55e' : '#ef4444' }}
              />
              Feedback submitted — thank you
            </p>
          )}
        </div>

      </div>
    </div>
  )
}

export default PaperCard