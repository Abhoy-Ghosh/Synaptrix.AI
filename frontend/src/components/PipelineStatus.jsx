const PipelineStatus = ({ currentStep }) => {

  const steps = [
    { label: "Retrieving Papers",    icon: "⬡", color: "blue"   },
    { label: "Running Summarizer",   icon: "⬡", color: "cyan"   },
    { label: "Running Analyzer",     icon: "⬡", color: "violet" },
    { label: "Finding Research Gaps",icon: "⬡", color: "blue"   },
    { label: "Building Synthesis",   icon: "⬡", color: "cyan"   },
    { label: "Finalizing Output",    icon: "⬡", color: "violet" },
  ]

  const colorMap = {
    blue:   { active: '#3b82f6', done: '#22c55e', glow: 'rgba(59,130,246,0.25)'  },
    cyan:   { active: '#06b6d4', done: '#22c55e', glow: 'rgba(6,182,212,0.25)'   },
    violet: { active: '#8b5cf6', done: '#22c55e', glow: 'rgba(139,92,246,0.25)'  },
  }

  const progress = currentStep >= 0 ? ((currentStep + 1) / steps.length) * 100 : 0

  return (
    <div
      className="rounded-[var(--radius-xl)] p-8 mt-10 relative overflow-hidden anim-fade-up"
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
      }}
    >
      {/* Background glow */}
      <div
        className="absolute top-0 left-0 w-full h-full pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at 20% 50%, rgba(59,130,246,0.05) 0%, transparent 60%)',
        }}
      />

      {/* Header */}
      <div className="flex items-center justify-between mb-8 relative z-10">
        <div className="flex items-center gap-4">
          <div
            className="w-10 h-10 rounded-2xl flex items-center justify-center"
            style={{
              background: 'rgba(59,130,246,0.12)',
              border: '1px solid rgba(59,130,246,0.2)',
            }}
          >
            <span style={{ fontSize: '18px' }}>⚙</span>
          </div>
          <div>
            <h2
              className="text-xl font-bold"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              AI Pipeline
            </h2>
            <p className="text-xs" style={{ color: 'var(--text-muted)', letterSpacing: '0.08em' }}>
              NEURAL ORCHESTRATION
            </p>
          </div>
        </div>

        {/* Live indicator */}
        <div
          className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium"
          style={{
            background: 'rgba(59,130,246,0.08)',
            border: '1px solid rgba(59,130,246,0.15)',
            color: '#93c5fd',
          }}
        >
          <div
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: '#3b82f6', animation: 'neural-pulse 1.5s ease infinite' }}
          />
          PROCESSING
        </div>
      </div>

      {/* Progress bar */}
      <div
        className="h-0.5 rounded-full mb-8 relative overflow-hidden"
        style={{ background: 'rgba(255,255,255,0.04)' }}
      >
        <div
          className="h-full rounded-full progress-line"
          style={{
            width: `${progress}%`,
            transition: 'width 0.6s cubic-bezier(0.22,1,0.36,1)',
            boxShadow: '0 0 12px rgba(59,130,246,0.6)',
          }}
        />
      </div>

      {/* Steps */}
      <div className="space-y-3 relative z-10">
        {steps.map((step, idx) => {
          const isDone    = idx < currentStep
          const isActive  = idx === currentStep
          const isPending = idx > currentStep
          const colors    = colorMap[step.color]

          return (
            <div
              key={idx}
              className="pipeline-step flex items-center gap-4 px-5 py-4 rounded-2xl relative overflow-hidden"
              style={{
                background: isDone
                  ? 'rgba(34,197,94,0.06)'
                  : isActive
                  ? `rgba(59,130,246,0.08)`
                  : 'rgba(255,255,255,0.02)',
                border: `1px solid ${
                  isDone
                    ? 'rgba(34,197,94,0.2)'
                    : isActive
                    ? 'rgba(59,130,246,0.25)'
                    : 'rgba(255,255,255,0.04)'
                }`,
                ...(isActive ? { boxShadow: '0 0 30px rgba(59,130,246,0.1)' } : {}),
              }}
            >
              {/* Scan line for active step */}
              {isActive && (
                <div
                  className="absolute inset-0 pointer-events-none"
                  style={{
                    background: 'linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.04) 50%, transparent 100%)',
                    animation: 'shimmer-sweep 2s ease-in-out infinite',
                  }}
                />
              )}

              {/* Step indicator */}
              <div
                className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 relative"
                style={{
                  background: isDone
                    ? 'rgba(34,197,94,0.15)'
                    : isActive
                    ? `rgba(59,130,246,0.15)`
                    : 'rgba(255,255,255,0.04)',
                  border: `1px solid ${
                    isDone
                      ? 'rgba(34,197,94,0.3)'
                      : isActive
                      ? 'rgba(59,130,246,0.4)'
                      : 'rgba(255,255,255,0.06)'
                  }`,
                  transition: 'all 0.4s ease',
                  ...(isActive ? {
                    boxShadow: '0 0 16px rgba(59,130,246,0.4)',
                    animation: 'neural-pulse 1.5s ease infinite',
                  } : {}),
                }}
              >
                {isDone ? (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2.5 7L5.5 10L11.5 4" stroke="#22c55e" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                ) : (
                  <span
                    className="text-xs font-bold"
                    style={{
                      color: isActive ? '#60a5fa' : 'rgba(255,255,255,0.2)',
                      fontFamily: 'var(--font-display)',
                    }}
                  >
                    {String(idx + 1).padStart(2, '0')}
                  </span>
                )}
              </div>

              {/* Label */}
              <span
                className="text-sm font-medium flex-1"
                style={{
                  color: isDone
                    ? '#86efac'
                    : isActive
                    ? '#e2e8f0'
                    : 'rgba(255,255,255,0.3)',
                  fontFamily: 'var(--font-body)',
                  transition: 'color 0.3s ease',
                }}
              >
                {step.label}
              </span>

              {/* Status tag */}
              {isDone && (
                <span
                  className="text-xs px-2.5 py-1 rounded-full font-medium"
                  style={{
                    background: 'rgba(34,197,94,0.1)',
                    color: '#86efac',
                    border: '1px solid rgba(34,197,94,0.15)',
                  }}
                >
                  Done
                </span>
              )}
              {isActive && (
                <div className="flex items-center gap-1.5">
                  {[0, 1, 2].map(d => (
                    <div
                      key={d}
                      className="w-1 h-1 rounded-full"
                      style={{
                        background: '#60a5fa',
                        animation: `neural-pulse 1s ease infinite`,
                        animationDelay: `${d * 0.2}s`,
                      }}
                    />
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default PipelineStatus