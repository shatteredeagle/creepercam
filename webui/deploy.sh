#!/usr/bin/env bash
# Deploy the web UI to the Pi: bash webui/deploy.sh [user@host]   (default pi@petcam.local)
set -euo pipefail
HOST=${1:-pi@petcam.local}
cd "$(dirname "$0")"
ssh "$HOST" 'sudo apt-get -y install python3-flask >/dev/null && sudo install -d -o pi /opt/petcam-ui'
scp -q -r app.py static "$HOST":/opt/petcam-ui/
scp -q petcam-ui.service "$HOST":/tmp/petcam-ui.service
ssh "$HOST" 'sudo install -m 644 /tmp/petcam-ui.service /etc/systemd/system/petcam-ui.service && sudo systemctl daemon-reload && sudo systemctl enable --now petcam-ui && sudo systemctl restart petcam-ui'
echo "UI: http://${HOST#*@}:8080"
