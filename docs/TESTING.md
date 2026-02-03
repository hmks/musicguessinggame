# Testing

## API
```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Mobile
```bash
cd mobile
npm install
npm run lint --if-present
npm test --if-present
```
