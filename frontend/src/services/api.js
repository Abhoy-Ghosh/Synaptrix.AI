import axios from "axios"

const API = axios.create({
  baseURL: "http://127.0.0.1:8001"
})

export const generateResearch = async(topic, mode)=>{

  const response = await API.post("/generate", {
    topic,
    mode
  })

  return response.data
}