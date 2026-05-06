import { useState } from "react"
import { submitPaperFeedback } from "../services/api"

const PaperCard = ({ paper }) => {

  const [feedbackStatus, setFeedbackStatus] = useState("")

  const handleFeedback = async (type) => {

    try {

      await submitPaperFeedback(
        paper.title,
        type
      )

      setFeedbackStatus(type)

    } catch (err) {

      console.log(err)

    }
  }

  return (

    <div className="bg-[#111827] border border-zinc-800 rounded-3xl p-8 hover:border-blue-500 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/10">

      {/* TITLE */}

      <h2 className="text-3xl font-bold leading-tight mb-5">
        {paper.title}
      </h2>

      {/* SOURCE */}

      <div className="mb-5">

        <span className="bg-blue-600 text-sm px-4 py-1 rounded-full font-medium">
          {paper.source}
        </span>

      <span className="bg-[#1f2937] border border-zinc-700 text-sm px-4 py-1 rounded-full">
         ⭐ Score: {paper.feedback_score || 0}
      </span>

</div>

      {/* ABSTRACT */}

      <div className="mb-8">

        <h3 className="text-xl font-semibold mb-4">
          Abstract
        </h3>

        <p className="text-zinc-300 text-lg leading-8">
          {paper.abstract?.slice(0, 300)}...
        </p>

      </div>

      {/* KEY INSIGHTS */}

      <div className="mb-8">

        <h3 className="text-xl font-semibold mb-4">
          Key Insights
        </h3>

        <ul className="space-y-3">

          {paper.insights?.points?.map((point, idx) => (

            <li
              key={idx}
              className="text-zinc-300 flex gap-3 text-lg leading-7"
            >

              <span className="text-blue-400 mt-1">
                •
              </span>

              <span>
                {point}
              </span>

            </li>

          ))}

        </ul>

      </div>

      {/* KEYWORDS */}

      <div className="mb-8">

        <h3 className="text-xl font-semibold mb-4">
          Keywords
        </h3>

        <div className="flex flex-wrap gap-3">

          {paper.insights?.keywords?.map((keyword, idx) => (

            <span
              key={idx}
              className="bg-[#1f2937] border border-zinc-700 px-4 py-2 rounded-full text-sm text-zinc-300 hover:border-blue-500 transition-all"
            >
              {keyword}
            </span>

          ))}

        </div>

      </div>

      {/* WHY IMPORTANT */}

      <div className="mb-8">

        <h3 className="text-xl font-semibold mb-4">
          Why Important
        </h3>

        <p className="text-zinc-300 text-lg leading-8">
          {paper.insights?.why}
        </p>

      </div>

      {/* FEEDBACK */}

      <div className="border-t border-zinc-800 pt-6">

        <h3 className="text-lg font-semibold mb-4">
          Was this paper useful?
        </h3>

        <div className="flex gap-4 flex-wrap">

          <button
            onClick={() => handleFeedback("useful")}
            className={`
              px-5 py-3 rounded-xl transition-all font-medium

              ${feedbackStatus === "useful"
                ? "bg-green-700"
                : "bg-green-600 hover:bg-green-700"
              }
            `}
          >
            👍 Useful
          </button>

          <button
            onClick={() => handleFeedback("not_useful")}
            className={`
              px-5 py-3 rounded-xl transition-all font-medium

              ${feedbackStatus === "not_useful"
                ? "bg-red-700"
                : "bg-red-600 hover:bg-red-700"
              }
            `}
          >
            👎 Not Useful
          </button>

        </div>

        {feedbackStatus && (

          <p className="text-zinc-400 mt-4 text-sm">
            Feedback submitted: {feedbackStatus}
          </p>

        )}

      </div>

    </div>

  )
}

export default PaperCard