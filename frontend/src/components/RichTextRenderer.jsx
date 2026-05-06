const RichTextRenderer = ({
  text,
  type = "default"
}) => {

  if (!text) return null

  const lines = text.split("\n")

  /* =========================================
     AGENT THEMES
  ========================================= */

  const THEMES = {

    summary: {
      border: "border-cyan-500/20",
      glow: "bg-cyan-500/10",
      accent: "text-cyan-300",
      icon: "◈"
    },

    analysis: {
      border: "border-violet-500/20",
      glow: "bg-violet-500/10",
      accent: "text-violet-300",
      icon: "⬡"
    },

    gaps: {
      border: "border-red-500/20",
      glow: "bg-red-500/10",
      accent: "text-red-300",
      icon: "◇"
    },

    synthesis: {
      border: "border-emerald-500/20",
      glow: "bg-emerald-500/10",
      accent: "text-emerald-300",
      icon: "⊕"
    },

    default: {
      border: "border-white/10",
      glow: "bg-white/5",
      accent: "text-white",
      icon: "•"
    }
  }

  const theme =
    THEMES[type] || THEMES.default


  return (

    <div
      className="
        relative
        space-y-3
        fade-in
      "
    >

      {/* =====================================
          AGENT HEADER
      ===================================== */}

      <div
        className="
          flex
          items-center
          gap-4
          mb-10
        "
      >

        <div
          className={`
            flex
            items-center
            justify-center

            w-12
            h-12

            rounded-2xl

            border
            ${theme.border}

            bg-white/[0.03]

            backdrop-blur-xl

            shadow-[0_10px_40px_rgba(0,0,0,0.35)]

            text-xl
            ${theme.accent}
          `}
        >
          {theme.icon}
        </div>

        <div>

          <div
            className="
              uppercase
              tracking-[0.28em]
              text-[10px]
              text-zinc-500
              mb-1
            "
          >
            {type} intelligence
          </div>

          <div
            className={`
              text-sm
              ${theme.accent}
            `}
          >
            Multi-agent semantic reasoning layer
          </div>

        </div>

      </div>


      {/* =====================================
          CONTENT
      ===================================== */}

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

        /* =====================================
           MAIN TITLE
        ===================================== */

        if (idx === 0) {

          return (

            <div
              key={idx}
              className="
                mb-14
              "
            >

              <h1
                className="
                  text-[42px]
                  md:text-[64px]

                  max-w-5xl

                  font-semibold
                  tracking-tight
                  leading-[1.05]

                  text-white
                "
              >
                {trimmed.replace("# ", "")}
              </h1>

            </div>
          )
        }

        /* =====================================
           ## HEADINGS
        ===================================== */

        if (
          trimmed.startsWith("## ")
        ) {

          const clean =
            trimmed.replace("## ", "")

          return (

            <div
              key={idx}
              className="
                pt-14
                pb-2
              "
            >

              <div
                className="
                  flex
                  items-center
                  gap-4
                  mb-5
                "
              >

                <div
                  className={`
                    w-2.5
                    h-2.5
                    rounded-full
                    ${theme.glow}

                    shadow-[0_0_24px_rgba(255,255,255,0.25)]
                  `}
                />

                <h2
                  className={`
                    text-[28px]
                    md:text-[34px]

                    font-semibold
                    tracking-tight

                    ${theme.accent}
                  `}
                >
                  {getSectionIcon(clean)} {clean}
                </h2>

              </div>

              <div
                className="
                  h-px
                  w-full

                  bg-gradient-to-r
                  from-white/10
                  via-white/5
                  to-transparent
                "
              />

            </div>
          )
        }

        /* =====================================
           BULLET CARDS
        ===================================== */

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

              {/* AMBIENT GLOW */}

              <div
                className={`
                  absolute
                  inset-0

                  rounded-[32px]

                  opacity-0
                  group-hover:opacity-100

                  transition
                  duration-700

                  blur-2xl

                  ${theme.glow}
                `}
              />

              {/* CARD */}

              <div
                className={`
                  relative

                  overflow-hidden

                  rounded-[30px]

                  border
                  ${theme.border}

                  bg-[linear-gradient(180deg,rgba(255,255,255,0.045),rgba(255,255,255,0.015))]

                  backdrop-blur-2xl

                  px-8
                  py-7

                  shadow-[0_0_0_1px_rgba(255,255,255,0.02),0_20px_80px_rgba(0,0,0,0.35)]

                  hover:translate-y-[-3px]

                  hover:shadow-[0_0_0_1px_rgba(255,255,255,0.04),0_40px_120px_rgba(0,0,0,0.45)]

                  transition-all
                  duration-500
                `}
              >

                {/* TOP LIGHT */}

                <div
                  className={`
                    absolute
                    top-0
                    left-0

                    w-full
                    h-px

                    ${theme.glow}

                    opacity-40
                  `}
                />

                {/* GRID TEXTURE */}

                <div
                  className="
                    absolute
                    inset-0

                    opacity-[0.03]

                    pointer-events-none
                  "
                  style={{
                    backgroundImage:
                      "radial-gradient(circle at 1px 1px, white 1px, transparent 0)",

                    backgroundSize:
                      "24px 24px"
                  }}
                />

                {/* CATEGORY */}

                <div
                  className="
                    relative

                    flex
                    items-center
                    gap-3

                    mb-5
                  "
                >

                  <div
                    className={`
                      w-3
                      h-3

                      rounded-full

                      ${category.color}

                      shadow-[0_0_20px_rgba(255,255,255,0.4)]
                    `}
                  />

                  <div
                    className="
                      text-[10px]

                      uppercase

                      tracking-[0.28em]

                      text-zinc-500

                      font-semibold
                    "
                  >
                    {category.label}
                  </div>

                </div>

                {/* TEXT */}

                <div
                  className="
                    relative

                    text-zinc-100

                    leading-[2]

                    text-[16px]

                    font-[425]
                  "
                >
                  {highlightKeywords(bulletText)}
                </div>

              </div>

            </div>
          )
        }

        /* =====================================
           PARAGRAPHS
        ===================================== */

        return (

          <p
            key={idx}
            className="
              text-zinc-300

              leading-[2]

              text-[16px]

              tracking-[0.01em]
            "
            style={{
              maxWidth: "92ch"
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
      color: "bg-emerald-400"
    }
  }

  if (
    t.includes("deployment") ||
    t.includes("hardware") ||
    t.includes("inference")
  ) {

    return {
      label: "Infrastructure",
      color: "bg-cyan-400"
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
      color: "bg-violet-400"
    }
  }

  if (
    t.includes("efficient") ||
    t.includes("optimization")
  ) {

    return {
      label: "Optimization",
      color: "bg-sky-400"
    }
  }

  return {
    label: "Research",
    color: "bg-zinc-400"
  }
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
    "alignment",
    "warfare",
    "autonomous",
    "military",
    "safety",
    "human oversight"
  ]

  let output = text

  keywords.forEach(keyword => {

    const regex = new RegExp(
      `(${keyword})`,
      "gi"
    )

    output = output.replace(
      regex,
      `<span class="text-cyan-300 font-semibold">$1</span>`
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