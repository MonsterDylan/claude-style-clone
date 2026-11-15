# Style Clone

AI can build any motion graphic you ask for. It can't read your mind.

"Make it look premium" tells an editor nothing, which is why AI-edited videos come out as skilled execution of a vague brief. The fix is to stop describing what good looks like and point at it.

This is a Claude skill that does the pointing. Give it a creator whose edits you admire. It pulls their top 10 videos, measures the pacing, looks at every frame, and writes down the rules underneath: layout, type, colour, motion, pacing, and what they never do. You get one file, `STYLE.md`, that your AI editor reads before it touches your footage.

It models the style. It does not copy the videos.

## What comes out

A style file with rules specific enough to act on:

- "Captions are one line, 1 to 4 words, with one word emphasised per phrase" and not "dynamic captions"
- A count after every rule, so you can tell a habit (9/10) from a one-off
- A "Why" line where the reason can be inferred, so the editor can make a judgment call the rules don't cover
- A "Never" list. Half of taste is what you leave out
- Every number marked `measured` or `read from frames`, and a section on what could not be measured

See a full one in [`examples/dylanjwatkins/STYLE.md`](examples/dylanjwatkins/STYLE.md). That is this skill run on my own YouTube Shorts, start to finish, by a fresh Claude session that had nothing but the skill.

## What you need

- **Claude Code**, on a Mac or Linux machine. Tested on macOS only.
- `ffmpeg` and `yt-dlp`: `brew install ffmpeg yt-dlp`
- Python 3.9 or newer. No packages to install.

That is enough to run it on YouTube Shorts from a handle, or on any 10 video links or files.

Two optional keys:

- An **Apify** token, only if you want to type an Instagram or TikTok handle and have it find the top videos for you. A run costs a few cents. Without it, paste 10 links instead.
- A **Groq** API key (free tier works), only if you want words per minute in the numbers. Everything else runs without it.

This will not work as an upload to claude.ai on the web. It needs a real shell to download and process video.

## Install

Paste this into your terminal:

```bash
git clone https://github.com/MonsterDylan/claude-style-clone.git && sh claude-style-clone/install.sh
```

It copies the skill into `~/.claude/skills/`, checks that ffmpeg and yt-dlp are there, and tells you what is missing if they are not.

Or paste this into Claude Code and let it do the same thing:

> Clone https://github.com/MonsterDylan/claude-style-clone and run its install.sh. If ffmpeg or yt-dlp is missing, install them for me.

Optional keys go in `~/.config/style-clone/.env`. The installer creates the file with both lines blank.

## Use it

Open Claude Code in the folder where your video projects live and say one of these:

> Clone the editing style of @somecreator on YouTube.

> Clone the editing style of @somecreator on Instagram.

> Clone the editing style from these 10 reels: (paste the links)

> Clone the editing style from the videos in ~/Downloads/reference-clips

It takes about ten minutes for ten videos. Most of that is Claude looking at the frames, around 120 images.

When it finishes it offers to add one line to your project's `CLAUDE.md`, so every future edit starts by reading the style file. Say yes. An editor only follows a style it reads.

## Which way in

| You have | Key needed | Tested |
|---|---|---|
| A YouTube handle | None | Yes. Takes the channel's Shorts, not long-form |
| 10 links (Instagram, TikTok, YouTube) | None | Yes, on Instagram and YouTube links |
| Video files on your machine | None | Yes |
| An Instagram handle | Apify token | Yes |
| A TikTok handle | Apify token | Yes, on one account |

The handle paths rank the creator's 40 most recent videos by views and keep the top 10. That is the top of their recent work, not of all time. `--pool 80` looks further back.

## How it works

1. **Fetch.** `scripts/fetch.py` finds the top videos and downloads them with yt-dlp.
2. **Measure.** `scripts/analyze.py` compares every frame with the one before and counts hard cuts, jump cuts and punch-ins, moves, and small changes like a caption word. It also measures loudness, estimates whether there is a music bed, and pulls the dominant colours.
3. **Draw.** Per video it makes contact sheets (a frame a second), large frames (so the type is readable) and motion strips (12 frames a second at the biggest moves, so you can see how things arrive).
4. **Look.** Claude opens every image, one video at a time, and takes notes.
5. **Write.** Claude writes `STYLE.md` from the notes and the numbers.

Everything stays on your machine, in `./style-clone/<name>/`.

## What it can't do

I would rather you know this now than find out mid-run.

- **Sound effects are not measured.** At all. The music bed is a guess from audio levels, and room or crowd noise can fool it.
- **The cut counts are approximate.** The counter cannot tell a jump cut from a large graphic landing, and big hand gestures or scrolling inside a card inflate it. On the few test videos I counted by eye it landed within about 50%. The skill tells Claude to check the numbers against the frames and trust the frames.
- **Motion timing is read off 12-frames-a-second stills.** Good to about a tenth of a second. It cannot see easing curves.
- **Fonts are named by look.** You get the closest free equivalent, not the creator's licensed face.
- **Positions are judged by eye** from downscaled frames, so they come as a share of the frame.
- **Instagram blocks downloads sometimes.** When it does, save the videos from the app and hand over the files.
- **Instagram does not give view counts for pasted links.** Only the handle path can rank by views there.
- **Only the first 3 minutes of each video are analysed.** This is built for short-form.
- **Some creators have no single style.** The skill will say so. All three test creators turned out to have a main format plus a second one, so it writes rules for the main format and lists the other as a variant.
- **One creator per style.** Mixing three gets you mush.

## Model, don't copy

The skill writes rules you can apply to your own footage and your own topic. It will not recreate a specific video, and it leaves out the creator's logo, name, face, catchphrases and exact graphics. Pacing, layout and motion grammar are how every editor learns. Someone's identity is not yours to take.

## Credit

The idea that creative work disappoints you because your taste is ahead of your skill is Ira Glass's. His fix was volume. This doesn't replace the reps. It gives them a target.

Built by [Dylan Watkins](https://dylanjwatkins.com). MIT licensed.
