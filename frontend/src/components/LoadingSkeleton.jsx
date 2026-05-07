const LoadingSkeleton = () => {
  return (
    <div className="mt-12 space-y-8 anim-fade-in">

      {/* SUMMARY SKELETON */}
      <div
        className="rounded-[var(--radius-xl)] p-8 relative overflow-hidden"
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
        }}
      >
        <div className="absolute inset-0 rounded-[var(--radius-xl)] overflow-hidden pointer-events-none">
          <div
            className="absolute inset-0 opacity-30"
            style={{
              background: 'linear-gradient(135deg, rgba(59,130,246,0.04) 0%, transparent 60%)',
            }}
          />
        </div>

        <div
          className="skeleton-wave rounded-lg mb-8"
          style={{ height: '28px', width: '220px', background: 'rgba(255,255,255,0.04)' }}
        />

        <div className="space-y-3">
          {[100, 100, 88, 72].map((w, i) => (
            <div
              key={i}
              className="skeleton-wave rounded-md"
              style={{
                height: '14px',
                width: `${w}%`,
                background: 'rgba(255,255,255,0.04)',
                animationDelay: `${i * 0.12}s`,
              }}
            />
          ))}
        </div>
      </div>

      {/* PAPER CARDS SKELETON */}
      <div className="grid xl:grid-cols-2 gap-8">
        {[0, 1, 2, 3].map((item) => (
          <div
            key={item}
            className="rounded-[var(--radius-xl)] p-8 relative overflow-hidden"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
              animationDelay: `${item * 0.1}s`,
            }}
          >
            {/* Shimmer overlay */}
            <div
              className="absolute inset-0 opacity-20"
              style={{
                background: `linear-gradient(135deg, ${
                  item % 2 === 0
                    ? 'rgba(59,130,246,0.06)'
                    : 'rgba(139,92,246,0.06)'
                } 0%, transparent 70%)`,
              }}
            />

            {/* Title */}
            <div
              className="skeleton-wave rounded-lg mb-3"
              style={{
                height: '22px',
                width: '80%',
                background: 'rgba(255,255,255,0.05)',
                animationDelay: `${item * 0.08}s`,
              }}
            />
            <div
              className="skeleton-wave rounded-lg mb-6"
              style={{
                height: '22px',
                width: '55%',
                background: 'rgba(255,255,255,0.05)',
                animationDelay: `${item * 0.08 + 0.05}s`,
              }}
            />

            {/* Source badge */}
            <div
              className="skeleton-wave rounded-full mb-8"
              style={{
                height: '26px',
                width: '100px',
                background: 'rgba(59,130,246,0.08)',
                animationDelay: `${item * 0.08 + 0.1}s`,
              }}
            />

            {/* Abstract lines */}
            <div
              className="skeleton-wave rounded-md mb-2"
              style={{
                height: '12px',
                width: '100%',
                background: 'rgba(255,255,255,0.04)',
                animationDelay: `${item * 0.08 + 0.15}s`,
              }}
            />
            <div
              className="skeleton-wave rounded-md mb-2"
              style={{
                height: '12px',
                width: '100%',
                background: 'rgba(255,255,255,0.04)',
                animationDelay: `${item * 0.08 + 0.2}s`,
              }}
            />
            <div
              className="skeleton-wave rounded-md"
              style={{
                height: '12px',
                width: '70%',
                background: 'rgba(255,255,255,0.04)',
                animationDelay: `${item * 0.08 + 0.25}s`,
              }}
            />

            {/* Keyword pills */}
            <div className="flex gap-2 mt-8">
              {[60, 80, 70].map((w, k) => (
                <div
                  key={k}
                  className="skeleton-wave rounded-full"
                  style={{
                    height: '28px',
                    width: `${w}px`,
                    background: 'rgba(255,255,255,0.04)',
                    animationDelay: `${item * 0.08 + k * 0.06}s`,
                  }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default LoadingSkeleton