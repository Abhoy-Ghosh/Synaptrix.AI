const PipelineStatus = ({ currentStep }) => {

  const steps = [
    "Retrieving Papers",
    "Running Summarizer",
    "Running Analyzer",
    "Finding Research Gaps",
    "Building Synthesis",
    "Finalizing Output"
  ]

  return (

    <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8 mt-10">

      <h2 className="text-3xl font-bold mb-8">
        AI Pipeline
      </h2>

      <div className="space-y-5">

        {steps.map((step, idx) => (

          <div
            key={idx}
            className={`
              flex items-center gap-4 p-4 rounded-2xl border
              transition-all duration-300

              ${idx < currentStep
                ? "bg-green-500/10 border-green-500"
                : idx === currentStep
                ? "bg-blue-500/10 border-blue-500 animate-pulse"
                : "bg-[#1f2937] border-zinc-700"
              }
            `}
          >

            <div
              className={`
                w-4 h-4 rounded-full

                ${idx < currentStep
                  ? "bg-green-500"
                  : idx === currentStep
                  ? "bg-blue-500"
                  : "bg-zinc-600"
                }
              `}
            />

            <span className="text-lg text-zinc-200">
              {step}
            </span>

          </div>

        ))}

      </div>

    </div>

  )
}

export default PipelineStatus