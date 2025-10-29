# AI Fest Management Monorepo

Monorepo containing:
- apps/web: Next.js (TypeScript) with Zustand
- apps/api: Django REST API with LangChain + LangGraph
- Single deploy via Render blueprint (render.yaml) and Docker

## Quickstart

Prereqs: Node 18+, Python 3.11+, Docker

- Install Node deps: `npm install`
- Setup Python venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install API deps: `pip install -r apps/api/requirements.txt`
- Dev (two terminals):
  - Web: `npm run dev -w apps/web`
  - API: `cd apps/api && ./manage.py runserver 0.0.0.0:8000`

## Single Deploy

- Render one-click using `render.yaml` in repo root
- Or `docker compose up --build`

## Environment

- Web: `.env.local`
- API: `.env` in `apps/api`
