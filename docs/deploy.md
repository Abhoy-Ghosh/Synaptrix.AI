# 🚀 Synaptrix.AI — Cloud Deployment Guide

Deploy Synaptrix.AI with **Vercel** (frontend) + **Render** (backend).

---

## Prerequisites

- GitHub account with the repo pushed
- [Vercel](https://vercel.com) account (free)
- [Render](https://render.com) account (free)
- Your API keys: `GEMINI_API_KEY`, `GROQ_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`, etc.

---

## Step 1: Push to GitHub

```bash
cd d:/research-synthesizer
git add -A
git commit -m "feat: cloud deployment ready"
git push origin main
```

---

## Step 2: Deploy Backend to Render

### Option A: One-Click (using render.yaml)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Blueprint**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and creates the service
5. Set environment variables in the Render dashboard:
   - `GEMINI_API_KEY` = your key
   - `GROQ_API_KEY` = your key
   - `SEMANTIC_SCHOLAR_API_KEY` = your key
   - `SPRINGER_META_API_KEY` = your key
   - `IEEE_API_KEY` = your key
   - `ALLOWED_ORIGINS` = `https://your-frontend.vercel.app`

### Option B: Manual Setup
1. Go to Render → **New** → **Web Service**
2. Connect GitHub repo
3. Settings:
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Plan**: Free (or Starter for always-on)
4. Add a **Disk**:
   - Mount path: `/opt/render/project/data`
   - Size: 1 GB
5. Set all environment variables listed above
6. Add: `DATA_DIR` = `/opt/render/project/data`
7. Deploy!

### After Deploy
Note your backend URL (e.g., `https://synaptrix-api.onrender.com`).
Test it: `curl https://synaptrix-api.onrender.com/` → should return `{"status": "running"}`

---

## Step 3: Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Import your GitHub repo
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL` = `https://synaptrix-api.onrender.com` (your Render backend URL)
6. Deploy!

---

## Step 4: Update CORS

After both are deployed, go back to Render and update:
- `ALLOWED_ORIGINS` = `https://your-project.vercel.app`

---

## Architecture

```
┌─────────────────────┐         HTTPS          ┌──────────────────────┐
│      Vercel          │ ─────────────────────► │       Render          │
│   (Static React)     │    VITE_API_URL        │  (Docker + FastAPI)   │
│                      │                        │                       │
│  • Vite build        │                        │  • SQLite (disk)      │
│  • SPA routing       │                        │  • MiniLM embedding   │
│  • CDN cached        │                        │  • Gemini/Groq LLM    │
└─────────────────────┘                        └──────────────────────┘
```

---

## Environment Variables Reference

### Backend (Render)
| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `GROQ_API_KEY` | ✅ | Groq API key (fallback LLM) |
| `SEMANTIC_SCHOLAR_API_KEY` | ✅ | Semantic Scholar API key |
| `SPRINGER_META_API_KEY` | ⚡ | Springer Nature API key |
| `IEEE_API_KEY` | ⚡ | IEEE Xplore API key |
| `ALLOWED_ORIGINS` | ✅ | Your Vercel frontend URL |
| `DATA_DIR` | ✅ | `/opt/render/project/data` |

### Frontend (Vercel)
| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | ✅ | Your Render backend URL |

---

## Troubleshooting

### Backend takes long to start
Free tier Render services sleep after 15 min. First request after sleep loads the embedding model (~30s). Upgrade to Starter ($7/mo) for always-on.

### CORS errors in browser
Make sure `ALLOWED_ORIGINS` on Render matches your exact Vercel URL (including `https://`).

### SQLite "database is locked"
The backend runs with 1 worker (`--workers 1`) to avoid SQLite concurrency issues. This is fine for personal/team use.

### Model download fails during Docker build
The Dockerfile pre-downloads the model. If Render build times out, increase build timeout in Render settings or use a pre-built Docker image.

---

## Local Development (unchanged)

```bash
# Terminal 1 — Backend
cd backend
python -m uvicorn app.main:app --reload --port 8001

# Terminal 2 — Frontend
cd frontend
npm run dev
```

No env vars needed locally — defaults to `http://127.0.0.1:8001`.
