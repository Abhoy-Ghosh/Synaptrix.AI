import {
  BrainCircuit,
  Database,
  FileText,
  GitBranch,
  Layers3,
  Sparkles,
  Workflow,
  Zap,
} from "lucide-react"

export default function Guide() {

  const flow = [
    "Query Input",
    "Retriever Agent",
    "Insight Extraction",
    "Cross-Paper Analysis",
    "Gap Detection",
    "Final Synthesis",
    "PDF Generation",
  ]

  const modes = [
    {
      title: "Fast Mode",
      icon: <Zap size={18} />,
      credits: "1 Credit",
      description:
        "Rapid synthesis pipeline optimized for quick intelligence generation and lightweight semantic retrieval.",
    },

    {
      title: "Parallel Mode",
      icon: <Workflow size={18} />,
      credits: "3 Credits",
      description:
        "Runs multiple research agents concurrently for broader reasoning coverage and faster comparative analysis.",
    },

    {
      title: "Research Mode",
      icon: <BrainCircuit size={18} />,
      credits: "6 Credits",
      description:
        "Deep sequential reasoning pipeline with layered synthesis, gap analysis, and higher-quality research intelligence.",
    },
  ]

  const outputs = [
    {
      title: "Summary",
      description:
        "Condensed overview of the most important findings across retrieved research papers.",
    },

    {
      title: "Analysis",
      description:
        "Cross-paper reasoning, trends, agreements, contradictions, and technical observations.",
    },

    {
      title: "Research Gaps",
      description:
        "Areas lacking exploration, unresolved limitations, and opportunities for future work.",
    },

    {
      title: "Final Synthesis",
      description:
        "Unified intelligence layer generated from multiple reasoning agents and semantic synthesis.",
    },
  ]

  return (

    <div className="min-h-screen bg-[#050816] text-white overflow-hidden">

      {/* ambient glow */}

      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(circle at top right, rgba(59,130,246,0.12), transparent 40%)',
        }}
      />

      <div className="relative z-10 max-w-7xl mx-auto px-6 md:px-10 py-24">

        {/* HERO */}

        <div className="mb-24">

          <div
            className="inline-flex items-center gap-3 px-5 py-2 rounded-full mb-8"
            style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.06)',
            }}
          >

            <Sparkles size={14} className="text-cyan-400" />

            <span
              className="text-xs uppercase tracking-[0.18em] text-cyan-300"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              System Guide
            </span>

          </div>

          <h1
            className="text-5xl md:text-7xl font-black leading-[0.95] mb-8"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Understanding
            <br />
            <span className="text-cyan-300">
              Synaptrix AI
            </span>
          </h1>

          <p className="text-zinc-400 text-lg leading-8 max-w-3xl">
            Synaptrix AI is a multi-agent neural research engine designed for
            semantic retrieval, cross-paper reasoning, intelligent synthesis,
            and explainable research generation.
          </p>

        </div>

        {/* SYSTEM FLOW */}

        <section className="mb-28">

          <div className="flex items-center gap-3 mb-10">
            <GitBranch size={18} className="text-cyan-400" />

            <h2
              className="text-2xl font-bold tracking-wide"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Neural Research Pipeline
            </h2>
          </div>

          <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-5">

            {flow.map((step, idx) => (

              <div
                key={step}
                className="rounded-[28px] p-6"
                style={{
                  background: 'rgba(255,255,255,0.025)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  backdropFilter: 'blur(20px)',
                }}
              >

                <div className="text-cyan-400 text-xs tracking-[0.16em] uppercase mb-4">
                  Step {idx + 1}
                </div>

                <div className="text-xl font-semibold text-zinc-100 leading-snug">
                  {step}
                </div>

              </div>
            ))}

          </div>

        </section>

        {/* RESEARCH MODES */}

        <section className="mb-28">

          <div className="flex items-center gap-3 mb-10">
            <Layers3 size={18} className="text-cyan-400" />

            <h2
              className="text-2xl font-bold tracking-wide"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Research Modes
            </h2>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">

            {modes.map((mode) => (

              <div
                key={mode.title}
                className="rounded-[32px] p-8"
                style={{
                  background: 'rgba(255,255,255,0.025)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  backdropFilter: 'blur(20px)',
                }}
              >

                <div className="flex items-center justify-between mb-6">

                  <div className="flex items-center gap-3">
                    <div className="text-cyan-400">
                      {mode.icon}
                    </div>

                    <h3 className="text-xl font-semibold">
                      {mode.title}
                    </h3>
                  </div>

                  <div
                    className="px-3 py-1 rounded-full text-xs text-cyan-300"
                    style={{
                      background: 'rgba(59,130,246,0.08)',
                      border: '1px solid rgba(59,130,246,0.16)',
                    }}
                  >
                    {mode.credits}
                  </div>

                </div>

                <p className="text-zinc-400 leading-7">
                  {mode.description}
                </p>

              </div>
            ))}

          </div>

        </section>

        {/* ARCHITECTURE */}

        <section className="mb-28">

          <div className="flex items-center gap-3 mb-10">
            <Database size={18} className="text-cyan-400" />

            <h2
              className="text-2xl font-bold tracking-wide"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Live Architecture
            </h2>
          </div>

          <div
            className="overflow-hidden rounded-[36px]"
            style={{
              border: '1px solid rgba(255,255,255,0.06)',
              background: 'rgba(255,255,255,0.02)',
            }}
          >

            <iframe
              src="/codegraph.html"
              title="Architecture Graph"
              className="w-full h-[500px] md:h-[700px] border-0"
            />

          </div>

        </section>

        {/* OUTPUTS */}

        <section className="mb-28">

          <div className="flex items-center gap-3 mb-10">
            <FileText size={18} className="text-cyan-400" />

            <h2
              className="text-2xl font-bold tracking-wide"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Output Intelligence Layers
            </h2>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">

            {outputs.map((item) => (

              <div
                key={item.title}
                className="rounded-[28px] p-7"
                style={{
                  background: 'rgba(255,255,255,0.025)',
                  border: '1px solid rgba(255,255,255,0.06)',
                }}
              >

                <h3 className="text-xl font-semibold mb-4 text-cyan-300">
                  {item.title}
                </h3>

                <p className="text-zinc-400 leading-7">
                  {item.description}
                </p>

              </div>
            ))}

          </div>

        </section>

        {/* QUERY EXAMPLES */}

        <section className="mb-20">

          <div className="flex items-center gap-3 mb-10">
            <Sparkles size={18} className="text-cyan-400" />

            <h2
              className="text-2xl font-bold tracking-wide"
              style={{ fontFamily: 'var(--font-display)' }}
            >
              Recommended Research Queries
            </h2>
          </div>

          <div className="space-y-5">

            {[
              "Recent advances in long-context transformer architectures",
              "Applications of multimodal AI in healthcare diagnostics",
              "Cross-paper analysis of autonomous robotics in warfare",
              "Neural retrieval systems for scientific literature synthesis",
            ].map((query) => (

              <div
                key={query}
                className="rounded-[24px] px-6 py-5 text-zinc-300"
                style={{
                  background: 'rgba(255,255,255,0.025)',
                  border: '1px solid rgba(255,255,255,0.06)',
                }}
              >
                {query}
              </div>
            ))}

          </div>

        </section>

      </div>

    </div>
  )
}