#!/usr/bin/env python3
"""style-clone fetcher: get a creator's top videos onto disk.

Three ways in, easiest first:
  1. Links or files you already have (no key, any platform yt-dlp can read):
       python3 fetch.py <out_dir> https://www.instagram.com/reel/abc/ https://... ~/Downloads/clip.mp4
  2. A YouTube handle (no key): lists the channel's Shorts (not long-form) with view counts and takes the top ones.
     YouTube rounds the counts it lists, so near ties are ranked approximately.
       python3 fetch.py <out_dir> --handle @name --platform youtube
  3. An Instagram or TikTok handle (needs an Apify token in APIFY_TOKEN, costs a few cents a run):
       python3 fetch.py <out_dir> --handle @name --platform instagram

Writes <out_dir>/videos/*.mp4 and <out_dir>/videos.json (url, views, likes, date, file), most viewed first.
Keys are read from the environment or from ~/.config/style-clone/.env (KEY=value lines).
Needs yt-dlp and ffmpeg on PATH. No Python packages.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ENV = os.path.expanduser("~/.config/style-clone/.env")
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4v")


def load_env():
    if os.path.exists(ENV):
        for line in open(ENV):
            m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$", line)
            if m and m.group(2) and not os.environ.get(m.group(1)):
                os.environ[m.group(1)] = m.group(2).strip("'\"")


def apify(actor, payload):
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        return None
    req = urllib.request.Request(f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=240",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit("Apify rejected the token (HTTP %d). Check APIFY_TOKEN in ~/.config/style-clone/.env: copy a fresh one "
                     "from apify.com > Settings > API & Integrations. Or skip the key and pass 10 links instead." % e.code)
        sys.exit(f"Apify run failed (HTTP {e.code}): {e.read()[:300].decode(errors='replace')}")


def list_youtube(handle, pool):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(pool), "--print",
                        "%(view_count)s\t%(id)s\t%(title)s", f"https://www.youtube.com/@{handle}/shorts"],
                       capture_output=True, text=True)
    out = []
    for line in r.stdout.splitlines():
        p = line.split("\t")
        if len(p) >= 2 and p[0].isdigit():
            out.append(dict(url=f"https://www.youtube.com/shorts/{p[1]}", views=int(p[0]), title=p[2] if len(p) > 2 else ""))
    if not out:
        sys.exit(f"Could not list Shorts for @{handle}. yt-dlp said: {r.stderr.strip()[-300:] or 'nothing'}")
    return out


def list_instagram(handle, pool):
    items = apify("apify~instagram-reel-scraper", {"username": [handle], "resultsLimit": pool})
    if items is None:
        sys.exit(NO_KEY.format(platform="Instagram"))
    out = []
    for it in items:
        url = it.get("url") or (f"https://www.instagram.com/reel/{it['shortCode']}/" if it.get("shortCode") else None)
        if url:
            out.append(dict(url=url, views=it.get("videoPlayCount") or it.get("videoViewCount") or 0,
                            likes=it.get("likesCount"), comments=it.get("commentsCount"), date=(it.get("timestamp") or "")[:10],
                            title=(it.get("caption") or "")[:80], direct=it.get("videoUrl")))
    return out


def list_tiktok(handle, pool):
    items = apify("clockworks~tiktok-scraper", {"profiles": [handle], "resultsPerPage": pool, "profileSorting": "popular",
                                                "shouldDownloadVideos": False})
    if items is None:
        sys.exit(NO_KEY.format(platform="TikTok"))
    return [dict(url=it["webVideoUrl"], views=it.get("playCount") or 0, likes=it.get("diggCount"),
                 comments=it.get("commentCount"), date=(it.get("createTimeISO") or "")[:10], title=(it.get("text") or "")[:80])
            for it in items if it.get("webVideoUrl")]


NO_KEY = """No APIFY_TOKEN found, so I can't list a creator's {platform} videos from the handle alone.
Two ways forward:
  a) Open their profile, sort by most viewed (or just pick the ones you love), copy 10 links and run:
       python3 fetch.py <out_dir> <link> <link> ...
  b) Get an Apify token (apify.com, Settings > API & Integrations) and put it in ~/.config/style-clone/.env as
       APIFY_TOKEN=...
     then run the same command again."""


def download(url, vdir, i, direct=None, info=None):
    base = os.path.join(vdir, f"{i:02d}")
    for f in os.listdir(vdir):
        if f.startswith(f"{i:02d}."):
            return os.path.join(vdir, f)
    r = subprocess.run(["yt-dlp", "-q", "--no-warnings", "--no-playlist", "-S", "vcodec:h264,res:1080", "--merge-output-format", "mp4",
                        "--no-simulate", "--print", "after_move:META\t%(view_count)s\t%(like_count)s\t%(upload_date)s\t%(title).80s",
                        "-o", base + ".%(ext)s", url], capture_output=True, text=True)
    for line in r.stdout.splitlines():                     # what the platform says about the video, when it says anything
        p = line.split("\t")
        if p[0] == "META" and len(p) >= 5 and info is not None:
            if p[1].isdigit(): info.setdefault("views", int(p[1]))
            if p[2].isdigit(): info.setdefault("likes", int(p[2]))
            if p[3].isdigit(): info.setdefault("date", f"{p[3][:4]}-{p[3][4:6]}-{p[3][6:8]}")
            if p[4] and p[4] != "NA": info.setdefault("title", p[4])
    hit = [f for f in os.listdir(vdir) if f.startswith(f"{i:02d}.")]
    if not hit and direct:                                 # the scraper's own file link, when yt-dlp is blocked
        try:
            req = urllib.request.Request(direct, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp, open(base + ".mp4", "wb") as fh:
                shutil.copyfileobj(resp, fh)
            hit = [os.path.basename(base + ".mp4")]
        except Exception:
            pass
    if not hit:
        print(f"   could not download {url}: {r.stderr.strip()[-200:] or 'blocked'}")
        return None
    return os.path.join(vdir, hit[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out_dir")
    ap.add_argument("inputs", nargs="*", help="video links or local files")
    ap.add_argument("--handle")
    ap.add_argument("--platform", choices=["instagram", "tiktok", "youtube"], default="instagram")
    ap.add_argument("--top", type=int, default=10, help="how many to keep (default 10)")
    ap.add_argument("--pool", type=int, default=40, help="how many recent videos to rank from (default 40)")
    a = ap.parse_args()
    for t in ("yt-dlp", "ffmpeg"):
        if not shutil.which(t):
            sys.exit(f"{t} not found. Install it first (macOS: brew install ffmpeg yt-dlp).")
    load_env()
    out = os.path.abspath(a.out_dir)
    vdir = os.path.join(out, "videos")
    os.makedirs(vdir, exist_ok=True)

    if a.handle:
        h = a.handle.strip().lstrip("@").rstrip("/").split("/")[-1].lstrip("@")
        listed = {"youtube": list_youtube, "instagram": list_instagram, "tiktok": list_tiktok}[a.platform](h, a.pool)
        listed.sort(key=lambda v: -(v.get("views") or 0))
        print(f"@{h} on {a.platform}: ranked {len(listed)} recent videos by views, keeping the top {min(a.top, len(listed))}")
        picks, pool_n = listed[: a.top], len(listed)
    else:
        if not a.inputs:
            sys.exit("Give me a --handle, or some links or files.")
        picks, pool_n = [dict(url=x) for x in a.inputs], None

    done = []
    for i, v in enumerate(picks, 1):
        src = v["url"]
        if os.path.exists(os.path.expanduser(src)):
            src = os.path.expanduser(src)
            if not src.lower().endswith(VIDEO_EXT):
                print(f"   skipping {src}: not a video file"); continue
            dest = os.path.join(vdir, f"{i:02d}{os.path.splitext(src)[1].lower()}")
            if not os.path.exists(dest):
                shutil.copy(src, dest)
            v["file"] = dest
        else:
            print(f"[{i}/{len(picks)}] {src}" + (f"  ({v['views']:,} views)" if v.get("views") else ""), flush=True)
            v["file"] = download(src, vdir, i, v.pop("direct", None), v)
        v.pop("direct", None)
        if v.get("file"):
            done.append(v)
    json.dump(done, open(os.path.join(out, "videos.json"), "w"), indent=1)
    meta = dict(handle=a.handle, platform=a.platform if a.handle else None, ranked_from=pool_n, kept=len(done), asked=len(picks))
    json.dump(meta, open(os.path.join(out, "fetch.json"), "w"), indent=1)
    if not done:
        sys.exit("Nothing downloaded. Instagram and TikTok often block downloads: save the videos from the app and pass the files.")
    print(f"DONE {len(done)} of {len(picks)} videos in {vdir}" + ("" if len(done) == len(picks) else
          "  (some were blocked: save those from the app and pass the files, or carry on with what you have)"))


if __name__ == "__main__":
    main()
