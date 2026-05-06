import { useState } from "react"

import { generateResearch } from "../services/api"
import PaperCard from "../components/PaperCard"
import PipelineStatus from "../components/PipelineStatus"
import LoadingSkeleton from "../components/LoadingSkeleton"

const Home = () => {

  const [topic, setTopic] = useState("")
  const [mode, setMode] = useState("fast")

  const [loading, setLoading] = useState(false)

  const [result, setResult] = useState(null)

  const [activeTab, setActiveTab] = useState("summary")

  const [currentStep, setCurrentStep] = useState(-1)

  const handleGenerate = async () => {

    if (!topic) return

    try {

      setLoading(true)

      for(let i = 0; i < 6; i++){

  setCurrentStep(i)

  await new Promise(resolve =>
    setTimeout(resolve, 700)
  )
}

      const data = await generateResearch(topic, mode)

      console.log(data)

      setResult(data)

      setCurrentStep(-1)

    } catch (err) {

      console.log(err)

    } finally {

      setLoading(false)

    }
  }

  return (

    <div className="min-h-screen bg-[#0b0f19] text-white">

      <div className="max-w-7xl mx-auto px-6 py-20">

        {/* HERO */}

        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Research Synthesizer AI
        </h1>

        <p className="text-zinc-400 text-lg mb-10">
          Adaptive Multi-Agent Research Intelligence System
        </p>

        {/* INPUT */}

        <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-6">

          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter research topic..."
            className="w-full bg-[#1f2937] border border-zinc-700 rounded-2xl p-5 outline-none resize-none min-h-[140px]"
          />

          <div className="flex justify-between items-center mt-6 flex-wrap gap-4">

            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="bg-[#1f2937] border border-zinc-700 rounded-xl px-4 py-3"
            >
              <option value="fast">⚡ Fast</option>
              <option value="parallel">🔄 Parallel</option>
              <option value="research">🧠 Research</option>
            </select>

            <button
              onClick={handleGenerate}
              className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-xl font-semibold transition-all"
            >
              {loading ? "Generating..." : "Generate Research"}
            </button>

          </div>

        </div>

        {/* PIPELINE */}

        {loading && (
            <PipelineStatus currentStep={currentStep} />
        )}

        {/* LOADING SKELETON */}

        {loading && (
            <LoadingSkeleton />
        )}

        
        {/* RESULTS */}

        {result && (

          <div className="mt-16">

            {/* TABS */}

            <div className="flex flex-wrap gap-4 mb-10">

              {[
                "summary",
                "analysis",
                "gaps",
                "synthesis",
                "papers"
              ].map((tab) => (

                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`
                    px-6 py-3 rounded-2xl capitalize font-medium transition-all
                    ${activeTab === tab
                      ? "bg-blue-600 text-white"
                      : "bg-[#111827] border border-zinc-800 text-zinc-400 hover:text-white"
                    }
                  `}
                >
                  {tab}
                </button>

              ))}

            </div>

            {/* SUMMARY */}

            {activeTab === "summary" && (

              <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8">

                <h2 className="text-5xl font-bold mb-8">
                  Research Summary
                </h2>

                <div className="text-zinc-300 whitespace-pre-wrap leading-8 text-lg">
                  {result.summary}
                </div>

              </div>

            )}

            {/* ANALYSIS */}

            {activeTab === "analysis" && (

              <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8">

                <h2 className="text-5xl font-bold mb-8">
                  Research Analysis
                </h2>

                <div className="text-zinc-300 whitespace-pre-wrap leading-8 text-lg">
                  {result.analysis}
                </div>

              </div>

            )}

            {/* GAPS */}

            {activeTab === "gaps" && (

              <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8">

                <h2 className="text-5xl font-bold mb-8">
                  Research Gaps
                </h2>

                <div className="text-zinc-300 whitespace-pre-wrap leading-8 text-lg">
                  {result.gaps}
                </div>

              </div>

            )}

            {/* SYNTHESIS */}

            {activeTab === "synthesis" && (

              <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8">

                <h2 className="text-5xl font-bold mb-8">
                  Cross-Paper Synthesis
                </h2>

                <div className="text-zinc-300 whitespace-pre-wrap leading-8 text-lg">
                  {result.synthesis}
                </div>

              </div>

            )}

            {/* PAPERS */}

            {activeTab === "papers" && (

              <div>

                <h2 className="text-5xl font-bold mb-10">
                  Top Research Papers
                </h2>

                <div className="grid xl:grid-cols-2 gap-10">

                  {result.top_papers?.map((paper, idx) => (

                    <PaperCard
                      key={idx}
                      paper={paper}
                    />

                  ))}

                </div>

              </div>

            )}

          </div>

        )}

      </div>

    </div>

  )
}

export default Home