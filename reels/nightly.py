#!/usr/bin/env python3
"""Run digest.py every night, keep the last N reels, ping Home Assistant.

Env: CAMERA (Frigate camera name), REEL_PREFIX (file name prefix), RUN_AT (HH:MM local, default 04:00), HOURS (look-back, default 24),
OUT_DIR (default /reels), KEEP_DAYS (default 14), HA_WEBHOOK_URL (optional),
REEL_URL_BASE (where Frigate serves OUT_DIR, sent to HA as the reel url),
RUN_NOW=1 (run once at start, then follow the schedule).
"""
import datetime as dt, functools, glob, http.server, json, os, re, subprocess, sys, threading, time, urllib.request

RUN_AT = os.environ.get("RUN_AT", "04:00")
HOURS = os.environ.get("HOURS", "24")
OUT = os.environ.get("OUT_DIR", "/reels")
KEEP = int(os.environ.get("KEEP_DAYS", "14"))
HOOK = os.environ.get("HA_WEBHOOK_URL", "")
PREFIX = os.environ.get("REEL_PREFIX", "reel")  # file names: <PREFIX>-YYYY-MM-DD.mp4
HERE = os.path.dirname(os.path.abspath(__file__))


URL_BASE = os.environ.get("REEL_URL_BASE", "")


def notify(title, message, **extra):
    print(f"notify: {title} - {message}", flush=True)
    if not HOOK:
        return
    req = urllib.request.Request(HOOK, json.dumps({"title": title, "message": message, **extra}).encode(),
                                 {"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=15).read()
    except Exception as e:  # HA down must not kill the loop
        print("notify failed:", e, flush=True)


class Download(http.server.SimpleHTTPRequestHandler):
    """Tiny download server: /<PREFIX>-DATE[-share].mp4 comes back as an attachment."""
    NAME = re.compile(rf"^/{re.escape(PREFIX)}-\d{{4}}-\d{{2}}-\d{{2}}(-share)?\.mp4$")

    def do_GET(self):
        if not self.NAME.match(self.path):
            self.send_error(404)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Content-Disposition", f'attachment; filename="{self.path.lstrip("/")}"')
        super().end_headers()

    do_HEAD = do_GET

    def log_message(self, *a):
        pass


def serve_downloads():
    port = int(os.environ.get("DOWNLOAD_PORT", "8088"))
    srv = http.server.ThreadingHTTPServer(("", port), functools.partial(Download, directory=OUT))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("downloads on port", port, flush=True)


def make_share(path):
    """720p copy small enough for chat apps."""
    share = path.replace(".mp4", "-share.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vf", "scale=-2:720",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-r", "15", "-an",
                    "-movflags", "+faststart", share], check=True)
    return share


def run_once():
    day = dt.date.today().isoformat()
    path = f"{OUT}/{PREFIX}-{day}.mp4"
    tmp = path + ".part.mp4"
    p = subprocess.run([sys.executable, f"{HERE}/digest.py", "--scorer", "clip", "--hours", HOURS, "--out", tmp],
                       capture_output=True, text=True)
    print(p.stdout, p.stderr, flush=True)
    if p.returncode != 0:
        notify("Highlight reel failed", (p.stderr.strip().splitlines() or ["see container log"])[-1])
        return
    m = re.search(r"(\d+) candidates, (\d+) in the reel, about (\d+)s", p.stderr)
    if os.path.exists(tmp):
        os.replace(tmp, path)
        try:
            make_share(path)
        except subprocess.CalledProcessError as e:
            print('share copy failed:', e, flush=True)
        notify("Highlight reel ready", f"{m.group(2)} clips, about {m.group(3)} s" if m else os.path.basename(path),
               date=day, url=f"{URL_BASE}/{os.path.basename(path)}" if URL_BASE else "")
    else:
        notify("No tarantula moments today", f"{m.group(1)} motion events checked, none showed the spider." if m else "no moments found", date="", url="")
    cutoff = time.time() - KEEP * 86400
    for f in glob.glob(f"{OUT}/{PREFIX}-*.mp4"):
        if os.path.getmtime(f) < cutoff:
            os.remove(f)


def next_run():
    h, m = map(int, RUN_AT.split(":"))
    t = dt.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
    return t if t > dt.datetime.now() else t + dt.timedelta(days=1)


os.makedirs(OUT, exist_ok=True)
serve_downloads()
if os.environ.get("RUN_NOW") == "1":
    run_once()
while True:
    t = next_run()
    print("next run", t, flush=True)
    time.sleep(max(1, (t - dt.datetime.now()).total_seconds()))
    run_once()
