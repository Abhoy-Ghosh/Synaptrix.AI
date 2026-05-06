import axios from "axios"

const API = axios.create({
  baseURL: "http://127.0.0.1:8001"
})

/* -----------------------------
   GENERATE RESEARCH
----------------------------- */

export const generateResearch = async (
  topic,
  mode
) => {

  const response = await API.post("/generate", {
    topic,
    mode
  })

  return response.data
}

/* -----------------------------
   GLOBAL FEEDBACK
----------------------------- */

export const submitGlobalFeedback = async (
  topic,
  feedback
) => {

  const response = await API.post("/feedback", {
    topic,
    feedback
  })

  return response.data
}

/* -----------------------------
   PAPER FEEDBACK
----------------------------- */

export const submitPaperFeedback = async (
  paperTitle,
  feedback
) => {

  const score =
    feedback === "useful"
      ? 1
      : -1

  const response = await API.post("/paper-feedback", {
    title: paperTitle,
    score: score
  })

  return response.data
}