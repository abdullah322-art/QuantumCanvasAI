### QCA API (QuantumCanvasAI)

- FastAPI backend with 10 model versions from QCA-4.9 to QCA-6.8-SUPREME.
- OAuth and Stripe are stubbed; provide your own frontend.

Run locally:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Deploy to Render: create a Web Service with start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables follow `.env.example`.
