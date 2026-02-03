#!/usr/bin/env bash
set -euo pipefail

if command -v ipconfig >/dev/null 2>&1; then
  ipconfig getifaddr en0
elif command -v hostname >/dev/null 2>&1; then
  hostname -I | awk '{print $1}'
else
  python - <<'PY'
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
finally:
    s.close()
PY
fi
