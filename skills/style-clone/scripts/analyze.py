#!/usr/bin/env python3
"""style-clone analyzer: turn a folder of videos into evidence an agent can read.

Numbers say how fast. Pictures say how it looks. This script produces both, per video:
  metrics.json          size, length, hard cuts, jumps, moves, small changes, speech pace, loudness, music bed, palette
  sheet-<a>-<b>.jpg     one frame a second, 6 per row, 18 per page (row 1 = the first 6 seconds of the page)
  big-<a>-<b>.jpg       whole frames twice a second, large enough to read the type: the first 12s, then up to 3 later looks
  motion-<t>.jpg        12 frames a second for 2 seconds at the opening and at the biggest moves and landings
  transcript.txt        what is said (only when a transcriber is available, see --transcribe)
and one summary.md for the whole set, listing every image the agent must look at.

Needs ffmpeg and ffprobe on PATH. No Python packages. Transcription is optional:
faster-whisper if it is installed, else a GROQ_API_KEY or OPENAI_API_KEY, else skipped.

Usage: python3 analyze.py <out_dir> [<video> ...]      (no videos given: uses <out_dir>/videos/*)
"""
import argparse
import glob
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import urllib.request
import uuid

GW, GH, GFPS = 32, 56, 30   # the tiny grey stream every frame is compared on
CELL = 9            # a cell "changed" when it moves more than this many grey levels between frames
HARD = 0.45         # share of cells changing in one frame: a hard cut (new shot or new layout)
BIG = 0.20          # ... a jump cut, a punch-in, or a large graphic landing (the counter cannot tell which)
SMALL = 0.012       # ... a caption word, a small graphic, a highlight
MERGE = 0.20        # events closer than this count once
MAX_S = 180         # analyse at most the first 3 minutes
PAGE = 18           # frames per contact-sheet page (6 x 3)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"{tool} not found. Install it first (macOS: brew install ffmpeg yt-dlp).")


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
             "-of", "json", path])
    j = json.loads(r.stdout or "{}")
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v:
        return None
    num, den = (v.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    return dict(width=v["width"], height=v["height"], fps=round(float(num) / max(float(den), 1), 2),
                duration=round(float(j["format"]["duration"]), 2),
                has_audio=any(s.get("codec_type") == "audio" for s in j.get("streams", [])))


def merge(times, gap=MERGE):
    out = []
    for t in sorted(times):
        if not out or t - out[-1] >= gap:
            out.append(t)
    return out


def picture_events(path, dur):
    """Compare every frame with the one before on a 32x56 grey grid and sort what changed by how much of the
    picture moved and for how long. Returns (events, baseline) where each event is (time, kind, share):
      cut    one frame, most of the picture: a new shot or a whole new layout
      jump   one or two frames, a fifth to half of the picture: a jump cut, a punch-in, or a big graphic landing
      move   three or more frames in a row: a zoom, a push, a slide, a wipe, a transition
      small  a brief small change: a caption word, a small graphic, a highlight"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", str(dur), "-i", path, "-vf",
                          f"fps={GFPS},scale={GW}:{GH}:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = GW * GH
    frames = [raw[k:k + n] for k in range(0, len(raw) - n + 1, n)]
    series = []                                            # (time, share of cells changed), repeated frames dropped
    for k in range(1, len(frames)):
        a, b = frames[k - 1], frames[k]
        if a == b:
            continue
        share = sum(1 for x, y in zip(a, b) if x - y > CELL or y - x > CELL) / n
        series.append((k / GFPS, share))
    end = len(frames) / GFPS
    series = [(t, v) for t, v in series if t < end - 0.5]      # a file's last frame often differs (a fade, an end slate): not an edit
    if not series:
        return [], 0.0
    base = statistics.median(v for _, v in series)
    vals = sorted(v for _, v in series)
    p90 = vals[int(len(vals) * 0.9)]
    big = max(BIG, 4 * base, 1.2 * p90)          # a speaker who gestures a lot raises the bar, so waving is not counted as cutting
    ev, k = [], 0
    while k < len(series):
        t, v = series[k]
        if v >= big:                                       # a burst of big change: how long does it last?
            j, peak = k, v
            while j + 1 < len(series) and series[j + 1][1] >= big * 0.8 and series[j + 1][0] - series[j][0] < 0.12:
                j += 1
                peak = max(peak, series[j][1])
            run_len = j - k + 1
            kind = "move" if run_len >= 3 else ("cut" if peak >= max(HARD, 2 * big) or peak >= 0.6 else "jump")
            ev.append((round(t, 2), kind, round(peak, 3)))
            k = j + 1
            continue
        near = [x for _, x in series[max(0, k - 4):k] + series[k + 1:k + 5]]
        if v >= SMALL and v >= 3 * (statistics.median(near) if near else 0) + 0.008:
            ev.append((round(t, 2), "small", round(v, 3)))
        k += 1
    return ev, round(base, 3)


def audio_stats(path, dur):
    out = dict(lufs=None, longest_pause=None, pauses_per_min=None, speech_share=None, bed_gap_db=None, music_bed=None)
    r = run(["ffmpeg", "-hide_banner", "-t", str(dur), "-i", path, "-af", "ebur128=framelog=quiet", "-vn", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    if m:
        out["lufs"] = float(m[-1])
    r = run(["ffmpeg", "-hide_banner", "-t", str(dur), "-i", path, "-af", "silencedetect=noise=-35dB:d=0.25", "-vn", "-f", "null", "-"])
    sil = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r.stderr)]
    out["longest_pause"] = round(max(sil), 2) if sil else None      # None: never quiet enough to tell (usually a music bed)
    out["pauses_per_min"] = round(len(sil) / dur * 60, 1) if sil else None
    out["speech_share"] = round(1 - sum(sil) / dur, 2)
    # music bed: how far the quiet moments sit under the loud ones. A dry voice drops 35 dB or more between words.
    r = run(["ffmpeg", "-hide_banner", "-t", str(dur), "-i", path, "-af",
             "aresample=16000,asetnsamples=3200,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
             "-vn", "-f", "null", "-"])
    lv = sorted(float(x) for x in re.findall(r"RMS_level=(-?[\d.]+)", r.stderr) if x not in ("-inf",))
    lv = [x for x in lv if x > -90]
    if len(lv) >= 20:
        floor = statistics.mean(lv[: max(1, len(lv) // 20)])          # quietest 5%
        voice = statistics.median(lv[len(lv) // 2:])                   # upper half
        out["bed_gap_db"] = round(voice - floor, 1)
        out["music_bed"] = "likely" if voice - floor < 22 else ("unclear" if voice - floor < 30 else "no")
    return out


def palette(path, dur):
    """dominant colours from one small frame a second"""
    r = subprocess.run(["ffmpeg", "-v", "error", "-t", str(dur), "-i", path, "-vf", "fps=1,scale=24:42", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True)
    b, counts, sat = r.stdout, {}, {}
    for i in range(0, len(b) - 2, 3):
        R, G, B = b[i], b[i + 1], b[i + 2]
        k = (R >> 5, G >> 5, B >> 5)
        c = counts.setdefault(k, [0, 0, 0, 0])
        c[0] += 1; c[1] += R; c[2] += G; c[3] += B
    total = sum(c[0] for c in counts.values()) or 1
    def hexof(c): return "#%02X%02X%02X" % (c[1] // c[0], c[2] // c[0], c[3] // c[0])
    main = sorted(counts.values(), key=lambda c: -c[0])[:6]
    for c in counts.values():
        r_, g_, b_ = c[1] / c[0], c[2] / c[0], c[3] / c[0]
        mx, mn = max(r_, g_, b_), min(r_, g_, b_)
        if mx > 90 and (mx - mn) / mx > 0.55:
            sat[hexof(c)] = c[0] / total
    acc = sorted(sat.items(), key=lambda x: -x[1])[:4]
    dark = sum(c[0] for c in counts.values() if (c[1] + c[2] + c[3]) / c[0] < 150) / total
    return dict(main=[(hexof(c), round(c[0] / total * 100)) for c in main],
                accents=[(h, round(s * 100, 1)) for h, s in acc], dark_share=round(dark, 2))


def tile(path, out, start, length, fps, cols, rows, width, crop=None):
    vf = f"fps={fps},"
    if crop:
        vf += crop + ","
    vf += f"scale={width}:-2,tile={cols}x{rows}:padding=4:color=0x202020"
    r = run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", path, "-vf", vf,
             "-frames:v", "1", "-q:v", "3", out])
    return r.returncode == 0 and os.path.exists(out)


def mmss(t):
    return f"{int(t) // 60}:{int(t) % 60:02d}"


def sheets(path, d, dur):
    made = {"sheet": [], "type": []}
    t = 0
    while t < dur - 0.2:
        n = min(PAGE, math.ceil(dur - t))
        name = f"sheet-{int(t):03d}-{int(t) + n:03d}.jpg"
        if tile(path, os.path.join(d, name), t, n, 1, 6, 3, 270):
            made["sheet"].append((name, t, t + n))
        t += PAGE
    later = list(range(24, int(dur), 20))
    starts = [0, 4, 8] + later[:: max(1, math.ceil(len(later) / 3))][:3]   # the first 12 seconds in full, then up to 3 later looks
    for t in starts:
        if t >= dur - 0.5:
            break
        n = min(4, dur - t)
        name = f"big-{int(t):03d}-{int(t + n):03d}.jpg"
        if tile(path, os.path.join(d, name), t, n, 2, 4, 2, 400):
            made["type"].append((name, t, t + n))
    return made


def motion_strips(path, d, dur, ev, n=5):
    """12 fps for 2s at the opening and at the biggest moves and landings, spread across the video"""
    picks = [0.0]
    rank = {"move": 3, "jump": 2, "small": 1, "cut": 0}
    for t, kind, share in sorted(ev, key=lambda e: (-rank[e[1]], -e[2])):
        s0 = max(0.0, t - 0.5)
        if kind != "cut" and all(abs(s0 - p) > 4 for p in picks) and s0 + 2 <= dur:
            picks.append(s0)
        if len(picks) >= n:
            break
    out = []
    for s0 in sorted(picks):
        name = f"motion-{s0:06.2f}.jpg"
        if tile(path, os.path.join(d, name), s0, 2, 12, 8, 3, 250):
            out.append((name, round(s0, 2)))
    return out


def transcribe(path, d, dur, mode):
    """returns (text, words_per_minute or None, how)"""
    if mode == "off":
        return None, None, "off"
    wav = os.path.join(d, "audio.mp3")
    run(["ffmpeg", "-v", "error", "-y", "-t", str(dur), "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", wav])
    if not os.path.exists(wav):
        return None, None, "no audio"
    text, how = None, None
    try:
        from faster_whisper import WhisperModel  # optional
        model = WhisperModel("small", compute_type="int8")
        segs, _ = model.transcribe(wav)
        text, how = " ".join(s.text.strip() for s in segs), "faster-whisper small"
    except Exception:
        for key, url, model in (("GROQ_API_KEY", "https://api.groq.com/openai/v1/audio/transcriptions", "whisper-large-v3-turbo"),
                                ("OPENAI_API_KEY", "https://api.openai.com/v1/audio/transcriptions", "whisper-1")):
            k = os.environ.get(key)
            if not k:
                continue
            try:
                bnd = uuid.uuid4().hex
                body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{model}\r\n"
                        f"--{bnd}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\n"
                        f"Content-Type: audio/mpeg\r\n\r\n").encode() + open(wav, "rb").read() + f"\r\n--{bnd}--\r\n".encode()
                req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {k}",
                                             "Content-Type": f"multipart/form-data; boundary={bnd}", "User-Agent": "style-clone"})
                text, how = json.loads(urllib.request.urlopen(req, timeout=120).read())["text"], key.split("_")[0].lower()
                break
            except Exception as e:
                how = f"{key} failed: {e}"
    try:
        os.remove(wav)
    except OSError:
        pass
    if not text:
        return None, None, how or "no transcriber (install faster-whisper, or set GROQ_API_KEY)"
    open(os.path.join(d, "transcript.txt"), "w").write(text.strip() + "\n")
    return text.strip(), len(text.split()), how


def analyse(path, d, mode):
    os.makedirs(d, exist_ok=True)
    p = probe(path)
    if not p:
        return None
    dur = min(p["duration"], MAX_S)
    ev, base = picture_events(path, dur)
    def times(*kinds): return merge([t for t, k, _ in ev if k in kinds])
    cuts, jumps, moves, small = times("cut"), times("jump"), times("move"), times("small")
    reframes, everything = times("cut", "jump", "move"), times("cut", "jump", "move", "small")
    def gaps(ts): return [b - a for a, b in zip([0] + ts, ts + [dur])]
    def block(ts): return dict(count=len(ts), per_min=round(len(ts) / dur * 60, 1), median_gap_s=round(statistics.median(gaps(ts)), 2),
                               longest_gap_s=round(max(gaps(ts)), 2))
    m = dict(file=os.path.basename(path), **p, analysed_s=dur,
             hard_cuts=dict(**block(cuts), times=[round(t, 2) for t in cuts]),
             jumps_or_landings=block(jumps), moves=block(moves), small_changes=block(small),
             framing_changes=block(reframes), any_change=block(everything), restlessness=base)
    m["audio"] = audio_stats(path, dur) if p["has_audio"] else None
    m["palette"] = palette(path, dur)
    text, words, how = transcribe(path, d, dur, mode) if p["has_audio"] else (None, None, "no audio")
    talk = dur * (m["audio"]["speech_share"] if m["audio"] and m["audio"]["speech_share"] else 1)
    m["speech"] = dict(transcriber=how, words=words, wpm=round(words / dur * 60) if words else None,
                       wpm_while_talking=round(words / max(talk, 1) * 60) if words else None,
                       first_line=(re.split(r"(?<=[.?!])\s", text)[0][:160] if text else None))
    m["images"] = sheets(path, d, dur)
    m["images"]["motion"] = motion_strips(path, d, dur, ev)
    json.dump(m, open(os.path.join(d, "metrics.json"), "w"), indent=1)
    return m


LOOK = """## How to read this (do not skip)

Numbers tell you how fast. Only the images tell you how it looks. Before writing a single rule, open every image
listed below, one video at a time, and write that video's notes BEFORE opening the next video: earlier images drop
out of your context as you go, so the notes are what you will write the style file from.

1. `sheet-*.jpg`: one frame a second, 6 per row. Page `sheet-018-036` row 1 is 0:18 to 0:23. Shows the whole edit:
   formats, layouts, when the framing changes, what the ending looks like.
2. `big-*.jpg`: whole frames, 2 a second, 4 per row, large enough to read type. They cover the first 12 seconds
   and up to three later 4-second looks, not the whole video. Read the font, case, weight, colour, box or no box,
   how many words at a time, where it sits.
3. `motion-*.jpg`: 24 frames = 2 seconds at 12 a second, 8 per row. The only place you can see HOW things arrive:
   fade, blur, slide (from where), scale, pop, type-on, wipe, or a plain cut. Count frames to time it: 2 frames
   is about 0.17s, 4 is about 0.33s. Easing curves cannot be read off these; do not claim them.
4. One moment at full size: `ffmpeg -ss <seconds> -i <video> -frames:v 1 frame.png`.

Limits to state in the style file: sound effects are not measured at all; the music bed is judged by level, so
crowd or room noise can read as a bed; motion timing is read off 12 fps stills; positions are judged by eye from
downscaled frames, so give them as a share of the frame.
"""


def summary(out, ms, meta):
    L = ["# Style evidence", "", f"{len(ms)} videos analysed. Every number is in `<video>/metrics.json`.", "",
         "| # | video | views | length | hard cuts/min | jumps or landings/min | moves/min | framing changes/min | small changes/min | any change every | wpm | LUFS | music bed |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (name, m) in enumerate(ms, 1):
        a, s, mt = m.get("audio") or {}, m["speech"], meta.get(m["file"], {})
        v = mt.get("views")
        L.append(f"| {i} | {name} | {f'{v:,}' if isinstance(v, int) else '?'} | {m['analysed_s']:.0f}s | {m['hard_cuts']['per_min']} | "
                 f"{m['jumps_or_landings']['per_min']} | {m['moves']['per_min']} | {m['framing_changes']['per_min']} | "
                 f"{m['small_changes']['per_min']} | {m['any_change']['median_gap_s']}s | {s['wpm'] or '?'} | {a.get('lufs', '?')} | "
                 f"{a.get('music_bed', '?')} ({a.get('bed_gap_db', '?')} dB) |")
    def med(f):
        xs = [f(m) for _, m in ms if f(m) is not None]
        return round(statistics.median(xs), 2) if xs else "?"
    L += ["", f"**Medians:** hard cuts/min {med(lambda m: m['hard_cuts']['per_min'])}, framing changes/min "
          f"{med(lambda m: m['framing_changes']['per_min'])}, any change every {med(lambda m: m['any_change']['median_gap_s'])}s, "
          f"wpm {med(lambda m: m['speech']['wpm'])}, length {med(lambda m: m['analysed_s'])}s.", "",
          "What the columns mean. Each frame is compared with the one before on a small grey grid:",
          "- **hard cut**: most of the picture changes in one frame. A new shot or a whole new layout.",
          "- **jump or landing**: a fifth to half of the picture changes in one or two frames. A jump cut, a punch-in, "
          "or a large graphic landing. The counter CANNOT tell these apart: look at the sheets and say which it is.",
          "- **move**: a big change that lasts three frames or more. A zoom, push, slide, wipe or transition.",
          "- **framing changes** = the three above together. **small changes**: a caption word, a small graphic.",
          "- **any change every**: the median gap between changes of any size. How long the picture ever sits still.",
          "A style can cut rarely and still change constantly. Scrolling inside a card, shaky handheld footage and big "
          "gestures inflate these counts. Check at least two videos' numbers against their sheets before quoting them, "
          "and where they disagree, trust the sheets and say so.", ""]
    lu = [m["audio"]["lufs"] for _, m in ms if m.get("audio") and m["audio"].get("lufs") is not None]
    if lu and max(lu) - min(lu) > 6:
        L += [f"Loudness varies a lot between these videos ({min(lu)} to {max(lu)} LUFS). Do not report one target loudness "
              "unless most of them agree.", ""]
    L += [LOOK]
    for name, m in ms:
        s, pal, mt = m["speech"], m["palette"], meta.get(m["file"], {})
        L += [f"## {name}", f"- source: {mt.get('url', m['file'])}  ({m['width']}x{m['height']}, {m['fps']} fps)",
              f"- first line: {s['first_line'] or '(no transcript: ' + str(s['transcriber']) + ')'}",
              f"- palette (whole-frame average, so small accents will not show): " + ", ".join(f"{h} {p}%" for h, p in pal["main"]) +
              f"; saturated: " + (", ".join(f"{h} {p}%" for h, p in pal["accents"]) or "none") + f"; dark share {pal['dark_share']}",
              f"- longest stretch with no hard cut {m['hard_cuts']['longest_gap_s']}s; with nothing changing at all {m['any_change']['longest_gap_s']}s",
              "- sheets: " + ", ".join(f"`{name}/{n}` ({mmss(a)}-{mmss(b)})" for n, a, b in m["images"]["sheet"]),
              "- big: " + ", ".join(f"`{name}/{n}`" for n, _, _ in m["images"]["type"]),
              "- motion: " + ", ".join(f"`{name}/{n}` (from {t}s)" for n, t in m["images"]["motion"]), ""]
    open(os.path.join(out, "summary.md"), "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out_dir")
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--transcribe", choices=["auto", "off"], default="auto")
    a = ap.parse_args()
    need("ffmpeg"); need("ffprobe")
    out = os.path.abspath(a.out_dir)
    vids = a.videos or sorted(f for f in glob.glob(os.path.join(out, "videos", "*")) if f.lower().endswith((".mp4", ".mov", ".webm", ".mkv", ".m4v")))
    if not vids:
        sys.exit(f"no videos given and none in {out}/videos/")
    meta = {}
    mp = os.path.join(out, "videos.json")
    if os.path.exists(mp):
        for v in json.load(open(mp)):
            if v.get("file"):
                meta[os.path.basename(v["file"])] = v
    vids.sort(key=lambda f: -(meta.get(os.path.basename(f), {}).get("views") or 0))
    ms = []
    for i, v in enumerate(vids, 1):
        name = f"v{i:02d}"
        print(f"[{i}/{len(vids)}] {os.path.basename(v)} -> {name}/", flush=True)
        m = analyse(v, os.path.join(out, "evidence", name), a.transcribe)
        if m:
            ms.append((name, m))
        else:
            print("   skipped: not a readable video")
    if not ms:
        sys.exit("nothing analysed")
    summary(os.path.join(out, "evidence"), ms, meta)
    imgs = sum(len(m["images"]["sheet"]) + len(m["images"]["type"]) + len(m["images"]["motion"]) for _, m in ms)
    print(f"DONE {len(ms)} videos, {imgs} images. Read {os.path.join(out, 'evidence', 'summary.md')} first.")


if __name__ == "__main__":
    main()
