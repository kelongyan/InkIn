# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

**InkIn（入画）** is a local web app that converts photos into comic/art style images via OpenAI-compatible vision APIs. Users configure any compatible provider (OpenAI, Doubao, Tongyi, Zhipu, etc.) and the app sends the image to the model with a style prompt.

## Commands

### Frontend (Vue 3 + Vite)
```bash
cd frontend
pnpm install          # install dependencies
pnpm dev              # dev server on port 3000
pnpm build            # production build to dist/
```

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py         # starts on port 5000
```

### Health check
```bash
curl http://localhost:5000/api/health
```

## Architecture

```
Browser → Vite dev server (port 3000) → proxy /api → Flask (port 5000) → external LLM API
```

- **Vite proxies** all `/api/*` requests to Flask (`localhost:5000`) — configured in `frontend/vite.config.js`
- **Flask** serves REST endpoints; CORS is also enabled for direct access
- **No database** — config persisted to `backend/config.json` (gitignored), uploads stored in `backend/uploads/`

### Backend modules

| File | Role |
|------|------|
| `app.py` | Flask app, route definitions, error handlers |
| `config_manager.py` | Read/write `config.json` (api_key, base_url, model) |
| `api_handler.py` | Encodes image to base64, calls LLM via OpenAI Chat Completions format, parses response (URL, base64, or markdown image link) |

### Frontend structure

| Path | Role |
|------|------|
| `src/App.vue` | Root component — orchestrates upload → generate → display flow |
| `src/components/ImageUploader.vue` | Drag-and-drop upload with validation (JPG/PNG/GIF/WebP, 10MB max) |
| `src/components/ApiSettings.vue` | Config form (API Key, Base URL, Model ID) loaded/saved via backend |
| `src/components/ResultViewer.vue` | Side-by-side original vs comic display + download button |
| `src/utils/api.js` | Axios instance (baseURL `/api`, 120s timeout) wrapping all API calls |

### Data flow

1. User uploads image → `POST /api/upload` → saved to `backend/uploads/`, returns filename
2. User clicks "生成漫画" → `POST /api/generate` with filename
3. Backend reads image from disk, base64-encodes, calls configured LLM API
4. LLM returns image (URL or base64) → frontend displays result

## Tech Stack & Conventions

- **Frontend**: Vue 3 Composition API (`<script setup>`), Element Plus, Axios — **use pnpm only** (not npm/yarn)
- **Backend**: Flask 3, Flask-CORS, Requests — Python 3.9+
- **Naming**: camelCase in JS, snake_case in Python
- **Commit format**: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:` prefixes
- **No test framework** is set up — validation is manual (start both servers, test the flow)

## Key Details

- API config fields: `api_key`, `base_url`, `model` — stored in `backend/config.json`
- Default prompt in `api_handler.py` is hardcoded (line 60): "请将这张照片转换为卡通漫画风格…"
- The LLM response parser handles three formats: raw URL, data URI, markdown `![]()` syntax
- Upload filename is a UUID hex to avoid collisions
- Frontend timeout matches backend: 120 seconds for generation requests
