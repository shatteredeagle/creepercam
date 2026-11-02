#!/usr/bin/env python3
"""Cut a highlight reel of the day's best motion events from Frigate.

Stdlib + ffmpeg only. Lists Frigate recording segments (10 s each, with a
motion score), groups neighbouring active segments into events, ranks them,
downloads the best ones and joins them into one mp4.

Scoring is pluggable: --scorer motion (default) needs no AI.
"""
import argparse, json, os, subprocess, sys, tempfile, time, urllib.request
from datetime import datetime

FRIGATE = os.environ.get("FRIGATE_URL", "http://frigate:5000")


def get(path):
    with urllib.request.urlopen(FRIGATE + path, timeout=30) as r:
        return json.load(r)


def segments(cam, after, before):
    return get(f"/api/{cam}/recordings?after={int(after)}&before={int(before)}")


def group_events(segs, min_motion, gap):
    """Merge segments whose motion >= min_motion; a gap <= `gap` s stays one event."""
    events, cur = [], None
    for s in sorted(segs, key=lambda x: x["start_time"]):
        if s["motion"] < min_motion:
            continue
        if cur and s["start_time"] - cur["end"] <= gap:
            cur["end"] = s["end_time"]
            cur["motion"] += s["motion"]
            cur["peak"] = max(cur["peak"], s["motion"])
            cur["n"] += 1
        else:
            if cur:
                events.append(cur)
            cur = {"start": s["start_time"], "end": s["end_time"],
                   "motion": s["motion"], "peak": s["motion"], "n": 1}
    if cur:
        events.append(cur)
    return events


def pick(events, top, max_len, min_len):
    """Rank by motion, trim long events around their busiest part, cap total count."""
    ev = [e for e in events if e["end"] - e["start"] >= min_len]
    ev.sort(key=lambda e: e["motion"], reverse=True)
    ev = ev[:top]
    for e in ev:
        if e["end"] - e["start"] > max_len:
            e["end"] = e["start"] + max_len
    ev.sort(key=lambda e: e["start"])  # play in time order
    return ev


FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf",
         "/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/noto/NotoSans-Regular.ttf"]


def stamp_filter(epoch):
    """ffmpeg drawtext filter with the real clock time, or None when no font is installed."""
    font = next((f for f in FONTS if os.path.exists(f)), None)
    if not font:
        return None
    t = datetime.fromtimestamp(epoch)
    text = t.strftime("%a %b %-d  %-I:%M %p").replace(":", "\\:")
    return (f"drawtext=fontfile={font}:text='{text}':x=24:y=h-th-24:fontsize=30:"
            "fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10")


def clip(cam, e, dest):
    url = f"{FRIGATE}/api/{cam}/start/{int(e['start'])}/end/{int(e['end'])}/clip.mp4"
    with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)


def sample_frames(path, step, outdir):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                    "-vf", f"fps=1/{step},scale=1280:-1", "-q:v", "3",
                    os.path.join(outdir, "f_%04d.jpg")], check=True)
    return sorted(os.path.join(outdir, f) for f in os.listdir(outdir) if f.endswith(".jpg"))


def spider_span(scores, step, thresh, pad, length):
    """First/last second with a spider frame, padded. None when no frame passes."""
    hit = [i for i, v in enumerate(scores) if v >= thresh]
    if not hit:
        return None
    return max(0, hit[0] * step - pad), min(length, hit[-1] * step + step + pad), len(hit) / len(scores)


def clip_reel(a, events):
    from scorer import ClipScorer  # lazy: needs torch
    cand = pick(events, a.candidates, a.max_len * 2, a.min_len)
    sc = ClipScorer()
    found = []
    with tempfile.TemporaryDirectory() as d:
        for i, e in enumerate(cand):
            src = os.path.join(d, f"src{i:02d}.mp4")
            clip(a.camera, e, src)
            fd = os.path.join(d, f"fr{i:02d}")
            os.mkdir(fd)
            frames = sample_frames(src, a.step, fd)
            scores = sc.score(frames)
            zoomed = False
            if a.zoom and max(scores) < a.thresh:  # nothing in the wide pass: look closer for a small spider
                z = sc.score(frames, zoom=True)
                zoomed = max(z) >= a.thresh
                scores = [max(x, y) for x, y in zip(scores, z)]
            length = e["end"] - e["start"]
            span = spider_span(scores, a.step, a.thresh, a.pad, length)
            t = datetime.fromtimestamp(e["start"]).strftime("%a %H:%M:%S")
            if span:
                lo, hi, frac = span
                found.append({"src": src, "lo": lo, "hi": min(hi, lo + a.max_len), "frac": frac,
                              "peak": max(scores), "t": e["start"], "motion": e["motion"]})
                print(f"  {t}  keep {int(found[-1]['hi'] - lo):3d}s  spider in {frac:.0%} of frames, peak {max(scores):.2f}{' (found by zoom)' if zoomed else ''}")
            else:
                print(f"  {t}  skip  no spider (peak {max(scores):.2f})")
        found.sort(key=lambda f: f["frac"] * f["motion"], reverse=True)  # moving spider beats a parked one
        found = sorted(found[:a.top], key=lambda f: f["t"])
        print(f"{len(cand)} candidates, {len(found)} in the reel, about {sum(int(f['hi'] - f['lo']) for f in found)}s", file=sys.stderr)
        if a.dry_run or not found:
            return
        lst = os.path.join(d, "list.txt")
        with open(lst, "w") as f:
            for i, x in enumerate(found):
                cut = os.path.join(d, f"cut{i:02d}.mp4")
                vf = stamp_filter(x["t"] + x["lo"])
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(x["lo"]), "-t", str(x["hi"] - x["lo"]),
                                "-i", x["src"], *(["-vf", vf] if vf else []),
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-r", "15", "-an", cut], check=True)
                f.write(f"file '{cut}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", "-movflags", "+faststart", a.out], check=True)
    print("wrote", a.out, file=sys.stderr)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--camera", default=os.environ.get("CAMERA", "camera"), help="Frigate camera name (env CAMERA)")
    p.add_argument("--hours", type=float, default=24, help="look back this many hours")
    p.add_argument("--min-motion", type=int, default=40, help="segment motion score to count as active")
    p.add_argument("--gap", type=int, default=30, help="seconds of quiet that still keep one event")
    p.add_argument("--min-len", type=int, default=10)
    p.add_argument("--max-len", type=int, default=60, help="seconds per event in the reel")
    p.add_argument("--top", type=int, default=8, help="events in the reel")
    p.add_argument("--out", default="reel.mp4")
    p.add_argument("--scorer", choices=["motion", "clip"], default="motion",
                   help="clip: keep only moments where a tarantula is visible (needs torch)")
    p.add_argument("--candidates", type=int, default=24, help="clip scorer: top motion events to examine")
    p.add_argument("--thresh", type=float, default=0.7, help="clip scorer: frame score that counts as spider")
    p.add_argument("--step", type=int, default=2, help="clip scorer: seconds between sampled frames")
    p.add_argument("--zoom", action="store_true",
                   help="clip scorer: also score zoomed crops of empty-looking events (EXPERIMENTAL: bedding texture scores as spider)")
    p.add_argument("--pad", type=int, default=4, help="clip scorer: seconds kept around the spider")
    p.add_argument("--dry-run", action="store_true", help="list the picks, download nothing")
    a = p.parse_args()

    now = time.time()
    segs = segments(a.camera, now - a.hours * 3600, now)
    events = group_events(segs, a.min_motion, a.gap)
    if a.scorer == "clip":
        return clip_reel(a, events)
    chosen = pick(events, a.top, a.max_len, a.min_len)
    print(f"{len(segs)} segments, {len(events)} events, {len(chosen)} picked", file=sys.stderr)
    for e in chosen:
        t = datetime.fromtimestamp(e["start"]).strftime("%a %H:%M:%S")
        print(f"  {t}  {int(e['end'] - e['start']):3d}s  motion {e['motion']} (peak {e['peak']})")
    if a.dry_run or not chosen:
        return

    with tempfile.TemporaryDirectory() as d:
        lst = os.path.join(d, "list.txt")
        with open(lst, "w") as f:
            for i, e in enumerate(chosen):
                path = os.path.join(d, f"{i:02d}.mp4")
                clip(a.camera, e, path)
                f.write(f"file '{path}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", "-movflags", "+faststart", a.out], check=True)
    print("wrote", a.out, file=sys.stderr)


if __name__ == "__main__":
    main()
