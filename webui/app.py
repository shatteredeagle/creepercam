#!/usr/bin/env python3
"""Petcam web UI: live view, camera controls, snapshot and Pi status.

Talks to mediamtx (control API on 127.0.0.1:9997) to change camera settings,
and grabs snapshots from its local RTSP stream. LAN only, no auth.
"""
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request

from flask import Flask, Response, jsonify, request, send_from_directory

API = "http://127.0.0.1:9997/v3/config/paths"
PATH = os.environ.get("PETCAM_PATH", "cam")
RTSP = f"rtsp://127.0.0.1:8554/{PATH}"
# BCM pin that switches the IR board on, or empty if there is none yet
IR_PIN = os.environ.get("PETCAM_IR_PIN", "")

# Settings the UI may change: name -> (type, min, max) or list of choices
SETTINGS = {
    "rpiCameraAfMode": ["auto", "manual", "continuous"],
    "rpiCameraLensPosition": ("float", 0.0, 10.0),
    "rpiCameraBrightness": ("float", -1.0, 1.0),
    "rpiCameraContrast": ("float", 0.0, 4.0),
    "rpiCameraSaturation": ("float", 0.0, 4.0),
    "rpiCameraSharpness": ("float", 0.0, 4.0),
    "rpiCameraEV": ("float", -4.0, 4.0),
    "rpiCameraExposure": ["normal", "short", "long"],
    "rpiCameraHDR": ("bool",),
    "rpiCameraHFlip": ("bool",),
    "rpiCameraVFlip": ("bool",),
    "rpiCameraFPS": ("float", 1.0, 30.0),
    "rpiCameraWidth": ("int", 320, 4608),
    "rpiCameraHeight": ("int", 240, 2592),
}

app = Flask(__name__, static_folder="static")


def mtx(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def clean(name, value):
    spec = SETTINGS[name]
    if isinstance(spec, list):
        if value not in spec:
            raise ValueError(f"{name}: expected one of {spec}")
        return value
    kind = spec[0]
    if kind == "bool":
        return bool(value)
    num = int(value) if kind == "int" else float(value)
    if not spec[1] <= num <= spec[2]:
        raise ValueError(f"{name}: {num} outside {spec[1]}..{spec[2]}")
    return num


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/settings")
def get_settings():
    try:
        cfg = mtx("GET", f"{API}/get/{PATH}")
    except (urllib.error.URLError, OSError) as e:
        return jsonify(error=f"mediamtx unreachable: {e}"), 503
    return jsonify({k: cfg.get(k) for k in SETTINGS})


@app.post("/api/settings")
def set_settings():
    body = request.get_json(force=True) or {}
    try:
        patch = {k: clean(k, v) for k, v in body.items() if k in SETTINGS}
    except (ValueError, TypeError) as e:
        return jsonify(error=str(e)), 400
    if not patch:
        return jsonify(error="no valid settings"), 400
    try:
        mtx("PATCH", f"{API}/patch/{PATH}", patch)
    except (urllib.error.URLError, OSError) as e:
        return jsonify(error=f"mediamtx unreachable: {e}"), 503
    return jsonify(patch)


@app.get("/api/snapshot")
def snapshot():
    if not shutil.which("ffmpeg"):
        return jsonify(error="ffmpeg missing"), 500
    cmd = ["ffmpeg", "-loglevel", "error", "-rtsp_transport", "tcp", "-i", RTSP,
           "-frames:v", "1", "-f", "image2", "-c:v", "mjpeg", "pipe:1"]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=15, check=True).stdout
    except (subprocess.SubprocessError, OSError) as e:
        return jsonify(error=f"snapshot failed: {e}"), 503
    return Response(out, mimetype="image/jpeg",
                    headers={"Content-Disposition": "inline; filename=petcam.jpg"})


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return None


def vcgen(arg):
    try:
        return subprocess.run(["vcgencmd", arg], capture_output=True, text=True,
                              timeout=2).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


@app.get("/api/status")
def status():
    temp = read("/sys/class/thermal/thermal_zone0/temp")
    up = read("/proc/uptime")
    load = read("/proc/loadavg")
    throttled = vcgen("get_throttled")
    cams = None
    if shutil.which("rpicam-hello"):
        # only meaningful while mediamtx is not holding the camera
        cams = "see stream"
    return jsonify(
        host=os.uname().nodename,
        cpu_temp_c=round(int(temp) / 1000, 1) if temp else None,
        uptime_s=int(float(up.split()[0])) if up else None,
        load=load.split()[:3] if load else None,
        throttled=throttled.split("=")[-1] if throttled else None,
        ir_pin=IR_PIN or None,
        camera=cams,
    )


@app.post("/api/ir")
def ir():
    if not IR_PIN:
        return jsonify(error="no IR pin configured (set PETCAM_IR_PIN)"), 400
    on = bool((request.get_json(force=True) or {}).get("on"))
    cmd = ["pinctrl", "set", IR_PIN, "op", "dh" if on else "dl"]
    try:
        subprocess.run(cmd, check=True, timeout=3)
    except (subprocess.SubprocessError, OSError) as e:
        return jsonify(error=f"gpio failed: {e}"), 500
    return jsonify(on=on)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
