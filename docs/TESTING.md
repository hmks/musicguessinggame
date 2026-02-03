# Testing

## API (macOS/Linux)
```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## API (Windows PowerShell)
```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

## Mobile (macOS/Linux)
```bash
cd mobile
npm install
npm run lint --if-present
npm test --if-present
npx expo start
```

## Mobile (Windows PowerShell)
```powershell
cd mobile
npm install
npm run lint --if-present
npm test --if-present
npx expo start
```

## Windows Emulator Notes
- Android emulator should use `http://10.0.2.2:8001` for API access.
- For a physical device, set `EXPO_PUBLIC_API_BASE_URL` to your machine IP on the same Wi-Fi.
