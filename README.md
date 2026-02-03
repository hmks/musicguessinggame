# MusiGuess (Stage-2)

Monorepo scaffold for MusiGuess with a FastAPI + MongoDB API and an Expo React Native client.

## Contents
- `api/`: FastAPI app with JWT auth, seed songs, and a minimal game flow
- `mobile/`: Expo React Native app with login + game demo UI
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

## Stage-2 Notes
- API health returns `ok` if MongoDB is reachable, otherwise `degraded`.
- Auth uses MongoDB if available, otherwise falls back to in-memory storage for Stage-2.
- Mobile keeps the JWT in memory (no AsyncStorage dependency). This means you must log in again after app restart.
- Android emulator reaches the API via `http://10.0.2.2:8001`.

## API Endpoints (Stage-2)
- `POST /auth/register` (email or username + password)
- `POST /auth/login` (email or username + password)
- `GET /songs` (optional query `q`)
- `POST /games/start`
- `POST /games/{game_id}/guess`
- `POST /games/{game_id}/finish`
