### QuantumCanvasAI (QCA)

FastAPI backend for QCA models with OAuth, Stripe billing, streaming chat API, programming engine, simple voice synthesis, and Render deployment. This bundle is ready to zip and deploy.

#### Features
- 10 model versions: `qca-4.9` → `qca-6.8-supereme`
- Chat API with streaming and sliding memory window to forget early turns
- Programming-focused engine emphasizing non-destructive code edits
- OAuth login (Google/GitHub) via Authlib
- Stripe billing with Free/Pro/Enterprise plan gating (Saudi National Day promo supported via code)
- Voice synthesis placeholder endpoint (WAV)
- Render deployment files included

#### Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn qca.app:app --host 0.0.0.0 --port 8000 --reload
```

#### Environment
See `.env.example`. Set the same variables in Render.

#### Endpoints
- `GET /health`
- `GET /v1/models`
- `GET /v1/access?model_id=qca-6.8-supereme&plan=pro` – plan gating check
- `POST /v1/chat/completions` (supports `stream=true` and `plan`)
- `GET /v1/voice/synthesize?text=hello` – simple WAV output
- `GET /auth/login/google`, `GET /auth/login/github`
- `GET /auth/callback/google`, `GET /auth/callback/github`
- `POST /billing/create-checkout-session`
- `POST /billing/webhook`

#### Packaging (ZIP)
```bash
bash scripts/create_zip.sh
```

