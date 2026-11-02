---
title: Software
---

# Software on the Pi

How to get the camera stream running on the Pi, tune autofocus, and use the small web UI.

The Pi runs Pi OS Lite 64-bit with [mediamtx](https://github.com/bluenviron/mediamtx) reading the camera directly
(its built-in `rpiCamera` source) and serving it as RTSP and WebRTC. There is no ffmpeg pipeline.

## Setup

[`pi-setup.sh`]({{ site.github.repository_url }}/blob/main/pi-setup.sh) installs `rpicam-apps`, `python3-picamera2`,
Flask and mediamtx, and creates a systemd unit. Run it after first boot:

```
bash pi-setup.sh
rpicam-hello --list-cameras      # the IMX708 should be listed
sudo systemctl enable --now mediamtx
```

The script leaves mediamtx disabled until the camera is attached, because it restart-loops with no sensor.
The stream is at `rtsp://<pi-host>:8554/cam`. Use a hostname rather than a fixed IP.

## Stream config

A working `/etc/mediamtx/mediamtx.yml`:

```yaml
api: yes
apiAddress: 127.0.0.1:9997
paths:
  cam:
    source: rpiCamera
    rpiCameraWidth: 1920
    rpiCameraHeight: 1080
    rpiCameraFPS: 15
    rpiCameraHFlip: true            # the camera is mounted upside-down
    rpiCameraVFlip: true
    rpiCameraAfMode: continuous
    rpiCameraAfRange: macro         # near focus only (about 5-50 cm)
    rpiCameraAfSpeed: normal
    rpiCameraTuningFile: /usr/share/libcamera/ipa/rpi/vc4/imx708_wide_noir.json
```

> **Tip:** keep the NoIR tuning file. The standard IMX708 file assumes an IR-cut filter and gives odd colours without one.

## Autofocus

The Camera Module 3 has continuous autofocus, but in a terrarium it can hunt: the scene is mostly
static and dark, and IR light has poor contrast. Options, in order of preference:

1. **Continuous with a limited range** (the config above): `AfMode continuous`, `AfRange macro`, `AfSpeed normal`.
   Works well when the animal moves around the enclosure.
2. **Manual lock** if it still hunts: `rpiCameraAfMode: manual` and `rpiCameraLensPosition` set to
   1 divided by the distance in metres. A subject 25 cm away is 4.0; a compromise of about 3.0 (33 cm)
   gives a wide sharp range in a small enclosure.

Hunting is more than cosmetic. Refocus pulses change the image and can register as motion in Frigate.

## Web UI

[`webui/`]({{ site.github.repository_url }}/tree/main/webui) is a small Flask app on port 8080 (LAN only, no auth).
It embeds the WebRTC live view and exposes camera controls: AF mode, lens position, brightness, contrast, saturation,
sharpness, EV, exposure, HDR, flips, FPS and resolution, plus a snapshot button and a Pi status panel. It talks to
mediamtx's control API. Deploy with `bash webui/deploy.sh user@pi-host`.

> **Warning:** settings changed in the UI live in memory only. A mediamtx restart or a Pi reboot reverts them.
> Write anything you want to keep (the flips, the autofocus range) into `mediamtx.yml`. Persisting UI
> settings automatically is not implemented.

## Useful commands

| Command | What it tells you |
|---|---|
| `vcgencmd get_throttled` | `0x0` is healthy. `0x50005` was under-voltage; `0x80008` is a soft temperature limit. |
| `journalctl -u mediamtx -f` | Stream and encoder logs. |
| `rpicam-hello --list-cameras` | Is the sensor detected? |
| `curl http://<pi-host>:8080/api/snapshot > shot.jpg` | Grab a still. |

Next: [Home Assistant and Frigate](home-assistant-frigate)
