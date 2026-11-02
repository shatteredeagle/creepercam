#!/usr/bin/env bash
# Run on the Pi 4B after first boot: bash pi-setup.sh
# Prepares libcamera tools and a mediamtx stream for the IMX708. The camera can be plugged in later.
set -euo pipefail

sudo apt-get update
sudo apt-get -y full-upgrade
sudo apt-get -y install rpicam-apps python3-picamera2 ffmpeg curl python3-flask

# Camera overlay. camera_auto_detect=1 (the Pi OS default) finds the IMX708 on its own;
# this line only makes it explicit. Add ",cam0" if the 4B does not detect it.
CFG=/boot/firmware/config.txt
grep -q '^dtoverlay=imx708' "$CFG" || echo 'dtoverlay=imx708' | sudo tee -a "$CFG" >/dev/null

# mediamtx (arm64 build has the built-in rpiCamera source)
if ! command -v mediamtx >/dev/null; then
  url=$(curl -fsSL https://api.github.com/repos/bluenviron/mediamtx/releases/latest \
    | grep -o 'https://[^"]*linux_arm64\.tar\.gz' | head -1)
  tmp=$(mktemp -d)
  curl -fsSL "$url" | tar -xz -C "$tmp"
  sudo install -m 755 "$tmp/mediamtx" /usr/local/bin/mediamtx
  sudo install -d /etc/mediamtx
  sudo install -m 644 "$tmp/mediamtx.yml" /etc/mediamtx/mediamtx.yml
fi

# Stream config: 1080p, autofocus continuous, rtsp://<host>:8554/cam
sudo tee /etc/mediamtx/mediamtx.yml >/dev/null <<'EOF'
api: yes
apiAddress: 127.0.0.1:9997
paths:
  cam:
    source: rpiCamera
    rpiCameraWidth: 1920
    rpiCameraHeight: 1080
    rpiCameraFPS: 15
    rpiCameraAfMode: continuous
EOF

sudo tee /etc/systemd/system/mediamtx.service >/dev/null <<'EOF'
[Unit]
Description=mediamtx camera stream
After=network-online.target

[Service]
ExecStart=/usr/local/bin/mediamtx /etc/mediamtx/mediamtx.yml
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
# Left disabled until the camera is attached (it would restart-loop with no sensor).
echo "Done. Reboot, plug in the camera, then:"
echo "  rpicam-hello --list-cameras"
echo "  sudo systemctl enable --now mediamtx"
echo "  stream: rtsp://$(hostname).local:8554/cam"
