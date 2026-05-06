const RichTextRenderer = ({ text }) => {

  if (!text) return null

  const lines = text.split("\n")

  return (

    <div className="space-y-5 fade-in">

      {lines.map((line, idx) => {

        const trimmed = line.trim()

        /* EMPTY */

        if (!trimmed) {

          return (
            <div
              key={idx}
              className="h-2"
            />
          )
        }

        /* -----------------------------------
           MAIN TITLE
        ----------------------------------- */

        if (idx === 0) {

          return (

            <h1
              key={idx}
              className="
                text-4xl
                md:text-5xl
                font-semibold
                tracking-tight
                leading-tight
                text-white
                mb-10
              "
            >
              {trimmed}
            </h1>
          )
        }

        /* -----------------------------------
           ## HEADINGS
        ----------------------------------- */

        if (
          trimmed.startsWith("## ")
        ) {

          const clean = trimmed
            .replace("## ", "")

          return (

            <div
              key={idx}
              className="
                pt-10
                pb-2
              "
            >

              <div
                className="
                  flex
                  items-center
                  gap-3
                  mb-4
                "
              >

                <div
                  className="
                    w-2
                    h-2
                    rounded-full
                    bg-blue-400
                    shadow-[0_0_12px_rgba(96,165,250,0.9)]
                  "
                />

                <h2
                  className="
                    text-2xl
                    md:text-3xl
                    font-semibold
                    tracking-tight
                    text-white
                  "
                >
                  {getSectionIcon(clean)} {clean}
                </h2>

              </div>

              <div
                className="
                  h-px
                  bg-gradient-to-r
                  from-blue-500/30
                  to-transparent
                  w-full
                "
              />

            </div>
          )
        }

        /* -----------------------------------
           BULLETS
        ----------------------------------- */

        if (
          trimmed.startsWith("- ") ||
          trimmed.startsWith("* ")
        ) {

          const bulletText = trimmed
            .replace("- ", "")
            .replace("* ", "")

          const category =
            detectCategory(bulletText)

          return (

            <div
              key={idx}
              className="
                group
                relative
              "
            >

              {/* GLOW */}

              <div
                className="
                  absolute
                  inset-0
                  rounded-2xl
                  opacity-0
                  group-hover:opacity-100
                  transition
                  duration-500
                  blur-xl
                  bg-blue-500/10
                "
              />

              {/* CARD */}

              <div
                className="
                  relative
                  rounded-2xl
                  border
                  border-white/5
                  bg-gradient-to-br
                  from-white/[0.03]
                  to-white/[0.01]
                  px-5
                  py-5
                  hover:border-blue-500/20
                  transition-all
                  duration-300
                "
              >

                {/* CATEGORY */}

                <div
                  className="
                    flex
                    items-center
                    gap-3
                    mb-3
                  "
                >

                  <div
                    className={`
                      w-3
                      h-3
                      rounded-full
                      ${category.color}
                      shadow-lg
                    `}
                  />

                  <div
                    className="
                      text-xs
                      uppercase
                      tracking-widest
                      text-slate-400
                      font-semibold
                    "
                  >
                    {category.label}
                  </div>

                </div>

                {/* CONTENT */}

                <div
                  className="
                    text-zinc-200
                    leading-8
                    text-[15px]
                    md:text-base
                  "
                >
                  {highlightKeywords(bulletText)}
                </div>

              </div>

            </div>
          )
        }

        /* -----------------------------------
           NORMAL TEXT
        ----------------------------------- */

        return (

          <p
            key={idx}
            className="
              text-zinc-300
              leading-8
              text-[15px]
              md:text-base
              tracking-[0.01em]
            "
            style={{
              maxWidth: "78ch"
            }}
          >
            {trimmed.replace(/\*\*/g, "")}
          </p>
        )
      })}

    </div>
  )
}


/* =========================================
   CATEGORY DETECTION
========================================= */

function detectCategory(text) {

  const t = text.toLowerCase()

  if (
    t.includes("performance") ||
    t.includes("benchmark") ||
    t.includes("accuracy")
  ) {

    return {
      label: "Performance",
      color: "bg-green-400"
    }
  }

  if (
    t.includes("deployment") ||
    t.includes("hardware") ||
    t.includes("inference")
  ) {

    return {
      label: "Deployment",
      color: "bg-blue-400"
    }
  }

  if (
    t.includes("bias") ||
    t.includes("limitations") ||
    t.includes("risk")
  ) {

    return {
      label: "Risk",
      color: "bg-red-400"
    }
  }

  if (
    t.includes("tool") ||
    t.includes("agent")
  ) {

    return {
      label: "Agents",
      color: "bg-purple-400"
    }
  }

  if (
    t.includes("efficient") ||
    t.includes("optimization")
  ) {

    return {
      label: "Optimization",
      color: "bg-cyan-400"
    }
  }

  return {
    label: "Research",
    color: "bg-slate-400"
  }
}


/* =========================================
   SECTION ICONS
========================================= */

function getSectionIcon(title) {

  const map = {

    "Key Insights": "💡",

    "Common Themes": "🧩",

    "Emerging Focus Areas": "🚀",

    "Summary": "📄",

    "Key Patterns": "🔍",

    "Emerging Trends": "📈",

    "Research Agreements": "🤝",

    "Research Disagreements": "⚔",

    "Methodological Observations": "🧠",

    "Strategic Insights": "✨",

    "Research Limitations": "⚠",

    "Research Gaps": "🕳",

    "Future Research Directions": "🌐",

    "Methodological Weaknesses": "📉",

    "Deployment Challenges": "🛠",

    "Strategic Opportunities": "🎯",

    "Cluster Relationships": "🔗",

    "Contrasting Research Directions": "⚡",

    "Cross-Domain Insights": "🌍",

    "Strategic Observations": "🧠",

    "Unified Research Understanding": "⊕"
  }

  return map[title] || "◈"
}


/* =========================================
   KEYWORD HIGHLIGHTING
========================================= */

function highlightKeywords(text) {

  const keywords = [
    "LLM",
    "LLMs",
    "deployment",
    "agents",
    "tool use",
    "benchmarking",
    "efficiency",
    "inference",
    "performance",
    "bias",
    "multitask",
    "optimization",
    "reasoning",
    "alignment"
  ]

  let output = text

  keywords.forEach(keyword => {

    const regex = new RegExp(
      `(${keyword})`,
      "gi"
    )

    output = output.replace(
      regex,
      `<span class="text-blue-400 font-semibold">$1</span>`
    )
  })

  return (

    <span
      dangerouslySetInnerHTML={{
        __html: output
      }}
    />
  )
}

export default RichTextRenderer