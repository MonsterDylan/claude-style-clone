---
name: style-clone
description: Learn a creator's editing style from their top videos and write it down as rules an AI video editor can follow. Takes a handle (or 10 links, or video files), pulls the most viewed videos, measures the pacing, looks at every frame sheet, and writes a STYLE.md with the layout, type, colour, motion, pacing and sound rules, the reasoning behind them, and what the creator never does. Use when someone says "clone this creator's style", "edit like @handle", "learn this creator's editing style", "build me a style guide from these videos", "make my videos look like theirs", types /style-clone, or pastes a creator's profile and asks how their edits work. Models the style, never copies a specific video.
---

# style-clone

Taste does not fit in a prompt. "Make it look premium" tells an editor nothing. This skill replaces the description
with evidence: it studies the videos someone already admires and writes down the rules underneath them, so an AI
editor works from a specific, proven style and not from adjectives.

The output is one file, `STYLE.md`: rules specific enough to act on, why each rule exists, which rules hold across
most videos and which are one-offs, and what this creator never does.

**Model the style, never copy the video.** Rules must be things someone could apply to their own footage and their
own topic. Never reproduce a creator's logo, name, handle, face, catchphrases, exact titles, exact diagrams or
product. If the person asks for a recreation of one specific video, say this skill doesn't do that and offer the
style instead.

## Paths

- `SKILL` = the folder this file is in. Scripts: `SKILL/scripts/fetch.py`, `SKILL/scripts/analyze.py`.
- `OUT` = `./style-clone/<name>/` in the current working directory, where `<name>` is the handle without the @
  (or a short name the person gives for a set of links). Everything this run makes goes there.
- Run scripts with `python3`. They use only the standard library plus `ffmpeg`, `ffprobe` and `yt-dlp`.

## 0. Check the machine (once per session, quietly)

Run `ffmpeg -version`, `yt-dlp --version` and `python3 --version`. If one is missing, say which and give the fix:
macOS `brew install ffmpeg yt-dlp`, Windows `winget install ffmpeg yt-dlp`, Linux the package manager plus
`pip install yt-dlp`. Offer to run it. Do not continue without ffmpeg.

## 1. Get the videos

Ask for one thing only if it was not given: whose style. Accept any of these, and do not ask for more:

| They gave | Run |
|---|---|
| A YouTube handle or channel link | `python3 SKILL/scripts/fetch.py OUT --handle <handle> --platform youtube` (no key needed; takes the channel's Shorts, not long-form) |
| An Instagram or TikTok handle | `python3 SKILL/scripts/fetch.py OUT --handle <handle> --platform instagram` (or `tiktok`). Needs `APIFY_TOKEN`. |
| Links to specific videos | `python3 SKILL/scripts/fetch.py OUT <link> <link> ...` (no key) |
| Video files or a folder | `python3 SKILL/scripts/fetch.py OUT <file> <file> ...` (no key) |

- The handle works with or without the @.
- The handle path ranks the creator's most recent 40 videos by views and keeps the top 10. That is "top 10 of
  their recent work", not of all time. Say so in the style file. `--pool 80` looks further back, `--top N` changes
  how many.
- No Apify token and an Instagram or TikTok handle: the script prints the two ways forward. Relay them plainly.
  The no-key way is: open the profile, pick the 10 videos they like most (or the most viewed), paste the links.
- Downloads get blocked sometimes, Instagram most of all. If some fail, carry on when at least 5 came down, and
  say how many you have. Under 5: ask them to save the videos from the app and give you the files.
- One creator per style. If they name several, ask which one first: mixing three styles produces mush. A second
  creator is a second run and a second file.
- Fewer than 5 videos means patterns can't be told from one-offs. Do the run if they want it, and label the
  result "thin evidence" at the top of the style file.

## 2. Measure

`python3 SKILL/scripts/analyze.py OUT`

About 5 to 10 seconds a video. It writes `OUT/evidence/summary.md` plus, per video, `metrics.json`, contact sheets
(`sheet-*.jpg`, a frame a second, the whole video), large frames (`big-*.jpg`, two a second with readable type, for
the first 12 seconds and up to three later looks) and motion strips (`motion-*.jpg`, 12 frames a second for 2
seconds at the opening and at the biggest moves). Expect about 12 images a video, 120 or so for ten.

Transcripts are optional. Without `faster-whisper` installed or a `GROQ_API_KEY`, words-per-minute is skipped and
everything else still works. Mention that once, do not block on it.

## 3. Look (the step that makes or breaks the result)

Read `OUT/evidence/summary.md`, then open **every image it lists, for every video**. Not a sample. Numbers say how
fast; only the pictures say how it looks, and a style file written from numbers alone is the vague brief this
skill exists to replace.

Work one video at a time. Open that video's images, then write its notes into `OUT/notes.md` BEFORE opening the
next video. This is not optional housekeeping: with this many images the early ones drop out of your context, and
the notes are what the style file gets written from. If you could not open every image, say exactly how many of
how many you opened, in the style file.

The summary's counts are approximate. For at least two videos, check the hard-cut and framing-change numbers
against what the sheets show. Where they disagree, trust the sheets, use your own count, and say so.

Do not record private details you happen to see on screen (names, account names, health or money details, a
third party's branding). Describe the editing, not the content.

For each video note:

- **Format**: talking head, split screen, screen recording, B-roll with voiceover, podcast clip, something else.
- **Layout**: where the speaker sits, where graphics sit, where type sits. Give positions as a share of the frame
  ("captions centred at about 67% down"). The frames you see are downscaled, so never read off pixels directly.
- **Type**: how many faces, what kind (tight grotesque, serif italic, mono, handwritten), case, weight, colour,
  box or no box, how many words on screen at once, whether a word is ever emphasised and how.
- **Colour**: the ground or grounds, the one colour that means "look here", how many accent colours, any glow or
  outline. The palette in the summary is a whole-frame average: good for grounds, useless for a small accent.
  Read accent colours off the big frames and label them "read from frames".
- **Motion**: from the motion strips, how each kind of thing arrives and leaves (fade, blur to sharp, slide from
  where, scale, pop, type-on, wipe, hard cut) and how long it takes. Count frames: 2 frames is about 0.17s.
  What stays perfectly still.
- **Pacing**: the cut rate against the change rate. A style can cut every 5 seconds and still land something new
  every second. What the first second looks like.
- **Structure**: what happens in the first 3 seconds, how sections are announced, how it ends.
- **Absences**: what you would expect in this kind of video that never shows up (emoji, caps, zooms, stock
  footage, transitions, a second accent colour).

If the videos fall into clearly different formats, group them. Write the rules for the largest group (the main
format) and describe the others in a short "Variants" section. Say how many videos are in each.

## 4. Write the style file

Write `OUT/STYLE.md` from the template in `SKILL/references/style-template.md`. The bar:

- **Specific enough to act on.** "Type enters on the stressed word, lower third, holds 0.8s" beats "dynamic
  captions". Every rule should let an editor make a decision without asking a follow-up question. Use numbers:
  seconds, frames, pixels on a 1080x1920 frame or shares of the frame, hex colours, words per caption.
- **Counted.** After each rule say how many videos show it. With one format, count out of all of them: `(9/10)`.
  With a main format and variants, count out of the main format and say so once at the top: `(7/7 main)`. A rule
  needs more than half of its group. Anything seen in fewer than that goes in "One-offs" with its count, and is
  not a rule.
- **Reasoned.** Where you can infer why a rule works, add one line starting "Why:". It lets an editor make a
  judgment call on a case the rules don't cover. If you can't infer a reason, leave it out rather than invent one.
- **Measured or seen, and labelled.** Mark each number `measured` (from metrics.json) or `read from frames` (your
  estimate from stills). Never present an estimate as a measurement. If a measurement is plainly wrong against the
  sheets, give your own count and label it `counted from sheets`. Drop any template line you have no data for
  (no transcript means no words-a-minute line).
- **Positions and sizes.** Give positions as a share of the frame first, then the pixel value that share works out
  to on 1080x1920 ("captions at 67% down, about y 1290"). Type sizes are cap height as a share of frame width.
  Estimate the share by eye from the big frames (a caption whose capitals are about a thirtieth of the frame
  width is 3.3%), then multiply out. These are all read from frames.
- **Generic about props.** When a rule depends on a branded prop or recurring object, describe what it does
  ("a small 3D object that illustrates the noun"), not what it is.
- **A "Never" list.** What this creator does not do. Half of taste is restraint. Only list absences that held
  across every video in the main format. If a variant breaks one, note that next to it.
- **No false averages.** When the videos split into two clear clusters on a number (loudness, length, cut rate),
  report both clusters and how many videos are in each. Do not average them into a figure no video has.
- **Honest about limits.** A short "What this is based on" section: how many videos, how they were chosen, what
  could not be measured (sound effects never are; motion timing is read off 12 fps stills; fonts are identified by
  look, so name the closest free equivalent and say it is an equivalent).
- **Portable.** No reference to this skill, to the creator's identity beyond the source line, or to any one
  editing tool. Any AI editor should be able to follow it.

Plain language. No hype words. No em dashes.

## 5. Hand it over

Tell them, in a few lines: where the file is, the three or four rules that most define the style, anything
surprising (a rule they would not have thought to put in a prompt), and what the evidence could not tell you.

Then offer the one step that makes it stick. An editor only follows a style it reads, so ask:

> Want me to add a line to this project's CLAUDE.md so your editor reads this style before it touches footage?

On yes, append to `CLAUDE.md` in the working directory (create it if missing):

```
## Video style
Before editing or building any video, motion graphic or caption, read `style-clone/<name>/STYLE.md` and follow it.
Where it is silent, use its "Why" lines to decide. Its "Never" list is not optional.
```

If they use a specific editor with its own style file (a Remotion theme, a HyperFrames project, a brand kit),
offer to translate the rules into that format as well. Do not do it unasked.

## Things that go wrong

- **Instagram links fail to download.** Common. Ask for the saved files, or try again later. Do not loop.
- **Apify says the token is not valid.** The script says so. Point them to apify.com, Settings, API & Integrations.
- **Every video looks different.** Some creators have no consistent style. Say that plainly and offer to model the
  3 or 4 videos that share a look, chosen by them.
- **Long videos.** Only the first 3 minutes of each are analysed. This skill is built for short-form.
- **They ask you to copy a video shot for shot, or to use the creator's name, face or logo.** Decline that part,
  explain that the skill models style, and carry on with the style.
