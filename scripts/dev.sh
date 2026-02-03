#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

if command -v docker >/dev/null 2>&1; then
  docker compose up -d mongo
else
  echo "Docker not found; skipping MongoDB startup."
fi

if [ -d "api" ]; then
  echo "Starting API (FastAPI) on http://localhost:8001"
  (cd api && python -m venv .venv >/dev/null 2>&1 || true)
  (cd api && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8001) &
fi

if [ -d "mobile" ]; then
  echo "Starting Expo"
  (cd mobile && npm install && npx expo start)
fi
