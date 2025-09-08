### QCA Platform (FastAPI) — Multi‑Version AI Service Skeleton

This repository scaffolds a deployable FastAPI service for QCA — a family of AI models with 10 tiered versions from `QCA 4.9` up to `QCA 6.8 SUPREME`. It includes a model registry, chat API with controllable memory (forgets earliest context), OAuth stubs for Google/GitHub, Stripe billing skeleton with discount hooks, a simple TTS stub, Dockerfile, and Render config.

Important: This is a production‑ready skeleton with clean interfaces for plugging real models and providers. It ships with a lightweight mock engine so it can run anywhere without GPUs.

#### Features
- 10 model versions registered via `app/models/registry.py`
- Chat endpoint with memory window control and content trimming
- Programmer‑focused response mode in the mock engine
- OAuth2 login stubs (Google/GitHub) using Authlib
- Stripe billing skeleton with National Day discount hook
- TTS/audio stub endpoint
- Dockerfile + `render.yaml` for Render deployment

#### Quick start (local)
1) Create and fill `.env` from `.env.example`.
2) Install:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
3) Open API docs at `http://localhost:8000/docs`.

#### Deployment on Render
- Create a new Web Service, connect this repo or upload the ZIP.
- Runtime: Docker; Auto deploy off (optional).
- Set environment variables from `.env.example` in Render Dashboard (never commit real secrets).
- Expose port `10000` (Render default; the container listens on `0.0.0.0:10000`).

#### Environment variables
See `.env.example` for the full list. Provide OAuth and Stripe credentials via env vars only. Do not hardcode secrets.

#### Endpoints (summary)
- `GET /` — health/version
- `GET /v1/models` — list models
- `POST /v1/chat` — chat completion with memory controls
- `GET /auth/login/google` and `/auth/callback/google` — Google OAuth stub
- `GET /auth/login/github` and `/auth/callback/github` — GitHub OAuth stub
- `GET /billing/prices` — current prices with discount
- `POST /billing/create-checkout-session` — Stripe checkout (mock if keys missing)
- `POST /v1/tts` — text‑to‑speech stub

#### Model integration
Replace the mock engine in `app/models/engines/mock.py` with your implementation, or add new engines and map them in `app/models/registry.py`.

#### Branding
Assets under `assets/` include a simple `logo.svg` for QCA.

#### License
For demonstration only. You are responsible for compliance when integrating third‑party APIs and deploying.
