# Example: my own YouTube Shorts

This is the skill run on my own channel, [@DylanJWatkins](https://www.youtube.com/@DylanJWatkins/shorts), by a fresh Claude Code session that had nothing but the skill.

The request was one line:

> Clone the editing style of @DylanJWatkins on YouTube Shorts.

It ranked my 40 most recent Shorts by views, took the top 10, opened all 127 images, and wrote [`STYLE.md`](STYLE.md). No keys, no transcript, about 11 minutes.

Things worth noticing in the result:

- It found that 8 of the 10 share one format and 2 are a different lo-fi format, wrote rules for the 8, and listed the other as a variant.
- It caught the measured cut count being wrong for this style (instant layout swaps read as cuts) and replaced it with its own count from the frames, labelled as such.
- The "Never" list is 11 lines long, and it marks which of them the lo-fi variant breaks.

The evidence images are not in this repo. They are frames of the videos, and yours will be generated on your machine when you run it.
