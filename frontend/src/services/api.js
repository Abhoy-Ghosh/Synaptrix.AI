import axios from "axios"

/* =========================================
   API BASE URL (env-configurable for cloud)
========================================= */

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001"

const API = axios.create({
  baseURL: API_BASE
})

/* =========================================
   GENERATE RESEARCH
========================================= */

export const generateResearch = async (
  topic,
  mode
) => {

  const response =
    await API.post("/generate", {

      topic,
      mode
    })

  return response.data
}

/* =========================================
   GLOBAL FEEDBACK
========================================= */

export const submitGlobalFeedback = async (

  topic,
  feedback

) => {

  const response =
    await API.post("/feedback", {

      topic,
      feedback
    })

  return response.data
}

/* =========================================
   PAPER FEEDBACK
========================================= */

export const submitPaperFeedback = async (

  paperTitle,
  feedback

) => {

  const score =
    feedback === "useful"
      ? 1
      : -1

  const response =
    await API.post("/paper-feedback", {

      title: paperTitle,
      score: score
    })

  return response.data
}

/* =========================================
   PDF DOWNLOAD
========================================= */

export async function downloadResearchPDF(data) {

  try {

    const response = await fetch(

`${API_BASE}/generate-pdf`,      {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify(data)
      }
    )

    if (!response.ok) {

      throw new Error(
        "PDF generation failed"
      )
    }

    const blob =
      await response.blob()

    const url =
      window.URL.createObjectURL(blob)

    const a =
      document.createElement("a")

    a.href = url

    a.download =
      "synaptrix_research_report.pdf"

    document.body.appendChild(a)

    a.click()

    a.remove()

    window.URL.revokeObjectURL(url)

  } catch (err) {

    console.error(
      "PDF download failed:",
      err
    )
  }
}

/* =========================================
   PROJECTS API
========================================= */

export const fetchProjects = async () => {
  const response = await API.get("/api/projects")
  return response.data
}

export const createProject = async (name, topic, description = "") => {
  const response = await API.post("/api/projects", { name, topic, description })
  return response.data
}

export const deleteProject = async (projectId) => {
  const response = await API.delete(`/api/projects/${projectId}`)
  return response.data
}

export const fetchProjectChats = async (projectId) => {
  const response = await API.get(`/api/projects/${projectId}/chats`)
  return response.data
}

/* =========================================
   CHATS API
========================================= */

export const createChat = async (projectId, title, mode = "fast") => {
  const response = await API.post(`/api/projects/${projectId}/chats`, { title, mode })
  return response.data
}

export const fetchChatDetail = async (chatId) => {
  const response = await API.get(`/api/chats/${chatId}`)
  return response.data
}

export const deleteChat = async (chatId) => {
  const response = await API.delete(`/api/chats/${chatId}`)
  return response.data
}

export const sendChatMessage = async (chatId, content, mode = null) => {
  const response = await API.post(`/api/chats/${chatId}/messages`, { content, mode })
  return response.data
}

/* =========================================
   GLOBAL SEARCH
========================================= */

export const searchGlobal = async (query) => {
  const response = await API.get(`/api/search?q=${encodeURIComponent(query)}`)
  return response.data
}

/* =========================================
   DASHBOARD STATS
========================================= */

export const fetchDashboardStats = async () => {
  const response = await API.get("/api/dashboard/stats")
  return response.data
}

/* =========================================
   KNOWLEDGE GRAPH
========================================= */

export const fetchKnowledgeGraph = async () => {
  const response = await API.get("/api/knowledge-graph")
  return response.data
}

/* =========================================
   SSE STREAMING
========================================= */

export const streamChatMessage = async (chatId, content, mode, onEvent) => {
  const response = await fetch(`${API_BASE}/api/chats/${chatId}/messages/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content, mode })
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split("\n")
    buffer = lines.pop()

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6))
          if (onEvent) onEvent(data)
        } catch (e) {
          // Skip malformed events
        }
      }
    }
  }
}