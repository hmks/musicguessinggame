# MusiGuess (Stage-1)

Monorepo scaffold for MusiGuess with a FastAPI + MongoDB API and an Expo React Native client.

## Contents
- `api/`: FastAPI app with JWT auth and health check
- `mobile/`: Expo React Native app
- `scripts/`: dev helpers
- `docs/`: testing docs

## Quick Start

### Prereqs
- Docker (for MongoDB)
- Python 3.11+
- Node.js 18+

### Environment
Copy `.env.example` to `.env` and adjust values if needed.

### Start (macOS/Linux)
```bash
./scripts/dev.sh
```

### Start (Windows)
```powershell
./scripts/dev.ps1
```

### API Health
```bash
curl http://localhost:8001/health
```

### Mobile (manual)
```bash
cd mobile
npm install
npx expo start
```

## Notes
- API health returns `ok` if MongoDB is reachable, otherwise `degraded`.
- Auth uses MongoDB if available, otherwise falls back to in-memory storage for Stage-1.
