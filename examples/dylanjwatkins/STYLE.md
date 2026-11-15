# Dark card explainer style

One continuous talking-head take, re-laid-out every few seconds on a near-black navy ground. The frame keeps
switching between a stacked split (proof on top, face below), the full face, and a full-screen graphic card, and it
gets there with a short fade through the dark ground, not with a cut to another shot. The one idea that holds it
together: the camera never cuts away, but the picture never sits still for more than a few seconds.

Source: YouTube Shorts @DylanJWatkins, 10 videos, top 10 by views of the most recent 40 (recent work, not all
time), analysed 2026-11-14. Counts below are out of the 8 videos in the main format, written `(n/8 main)`. The
other 2 are a lo-fi format described under Variants. This file models the style. It does not license copying any
video, logo, name, face or product.

## The numbers
All for the 8 main-format videos.
- Hard cuts between camera shots: 0 in 7 videos, 1 in the eighth (counted from sheets). The measured figure is a
  median of 0.4 a minute with one video at 7.6, but that video's "cuts" are instant layout swaps inside one take
  and two others are just the last frame of the file
- Framing changes a minute (layout swaps, card landings, moves): median 19.9, range 10.0 to 27.7 (measured,
  approximate). That is a new framing about every 3 seconds
- Something changes on screen every 1.27s, range 0.78s to 2.13s (measured: median gap between changes of any size)
- Longest stretch with nothing changing at all: median 5.3s, never more than 7.6s (measured)
- Length: 31s to 78s, median 58s (measured)
- Music bed: unclear. By level only it reads likely in 2, unclear in 4, no in 2 (measured by level, not by ear)
- Loudness: 5 of the 8 sit at -14.2 to -14.4 LUFS. The other 3 sit at -23.0 to -24.9 LUFS (measured)

## Layout (1080 x 1920)
All positions are read from frames.
- Three layouts built from one take and rotated through the whole video: stacked split, full face, full-screen
  graphic card (8/8 main use split and full face, 7/8 main also use the full-screen card)
- Stacked split: a proof card on top from about 7% to 45% down (y 135 to 865), about 96% of the frame wide. The
  speaker in a second card from about 46% to 90% down (y 885 to 1730), inset about 4% each side (x 43 to 1037).
  Both cards have rounded corners of about 2% of frame width (about 22px) and a visible strip of ground between
  them (7/8 main)
  Why: the viewer sees the evidence and the person reacting to it at once, so neither needs a cut.
- In the split the speaker is cropped tight: eyes about one third down the speaker card, head nearly filling its
  width (8/8 main)
- Full face: the same take scaled to fill the frame, head and upper chest, with a dark gradient over the bottom
  30% (below about y 1345) so captions stay readable (8/8 main)
- Full-screen graphic card: no speaker. The graphic lives between about 15% and 60% down (y 290 to 1150). The
  lower third is left empty except for captions (7/8 main)
- The top card can be shorter than its zone, about 7% to 22% down (y 135 to 420), with bare ground under it. Do
  not stretch content to fill the zone (5/8 main)
- Small labels and pills sit in a band at about 4% to 13% down (y 75 to 250): above the head on the full face,
  above the top card in the split (7/8 main)
- Captions sit at about 82% to 88% down (y 1575 to 1690) in every layout, centred. In the split they overlap the
  bottom edge of the speaker card (8/8 main)
  Why: the caption line never moves, so the eye has one fixed place to read while everything else rearranges.

## Type
- Face 1: a heavy geometric sans, weight about 800 to 900, all caps, slightly loose word spacing. Used for
  captions, titles, section names, pills and big numbers. Closest free equivalent: Montserrat ExtraBold or Black
  (8/8 main, identified by look)
- The same family at about weight 600, all caps, tracked very wide (roughly 0.25em), for tiny kickers above a
  title or a graphic (8/8 main)
- Face 2: a small monospace for the address line of window-style cards and for code-like tags. Closest free
  equivalent: JetBrains Mono (6/8 main)
- Sizes, as cap height against frame width (read from frames): captions about 3.2% (about 34px on a 1080-wide
  frame); kickers about 1.7% (18px); pill text about 2.1% (23px); titles about 6% (65px); hero numbers and the
  call-to-action word about 10% to 20% (110 to 215px)

## Colour
- Ground: near-black navy, about #050A12. It is the single largest colour in every main-format video, 32% to 49%
  of the frame, and dark pixels overall are 45% to 67% (measured). A faint violet or deep blue radial glow sits
  behind graphic cards (read from frames)
- Accent: cyan, about #35E0E6 (read from frames). Used for: the word being spoken, the key number, the fix or the
  win, ticks, the call-to-action word. Never for body text or for the border of the speaker card (8/8 main)
- Second colour: violet, about #7C4DFF (read from frames). Used for card borders (a thin line with a soft outer
  glow), numerals in section tags, the glow behind white titles, and filled sticker labels (8/8 main)
- A cyan to violet or cyan to blue gradient is reserved for hero numbers, the call-to-action word and one result
  pill per video (6/8 main)
- Red, about #FF2D55 (read from frames): only for the thing being dismissed or the bad reading. Strike-throughs,
  a tilted stamp word, an outline around a wrong word, an alert card (7/8 main)
  Why: cyan means "this is the answer" and red means "this is the problem". Each colour has one job, so a viewer
  with the sound off still follows the argument.
- Built graphic panels are a dark violet-grey, about #2A2740. Pills are dark navy, about #0E1524 (7/8 main, read
  from frames)
- White for all other type. Grey at about 55% white for kickers and sub-labels (8/8 main)
- Tiny cyan and violet dots drift slowly over the ground and over the face (5/8 main, read from frames, faint)

## Captions
- All caps, heavy sans, white, no box, soft dark shadow only. 3 to 6 words on screen, on 1 or 2 centred lines.
  Punctuation kept (7/8 main). The eighth sets them in sentence case with the same rules otherwise
- The word being spoken turns cyan, one word at a time. The rest of the line stays white (8/8 main)
- A new line fades up in 1 to 2 frames at 12 fps (about 0.1 to 0.15s), and the old line is gone before the new
  one arrives. No slide, no bounce, no scale (8/8 main, read from frames)
- Captions run through every layout, including full-screen graphic cards and the call to action. They never stop
  (8/8 main)

## Motion
All timings are read from 12 fps stills.
- Layout changes go through the dark ground: the old layout dims for 1 frame and is gone by the next, then the
  new one fades up over about 2 frames. 3 to 4 frames in total, about 0.3s (8/8 main)
- Split to full face and back is a morph when the speaker is in both: the speaker card grows or shrinks to its
  new size in about 3 frames, about 0.25s, while the top card fades (6/8 main)
- Titles fade up in 2 to 3 frames with the kicker a frame ahead of the main line. No slide (7/8 main)
- Lists build one item per spoken item: pills, rows, chips or tiles fade up in about 2 frames each, some with a
  slight scale-up, and stack downward. They leave together in one fade (8/8 main)
- Numbers count up to their final value in about 0.7 to 1s (5/8 main)
- Real web pages or app recordings inside the top card scroll slowly and continuously for as long as they are on
  screen (6/8 main)
  Why: the slow scroll keeps the picture alive between layout changes without adding a cut.
- Built graphics animate their own content: lines type on, bars fill left to right, strike-throughs draw left to
  right (7/8 main)
- Short emphasis labels are tilted about 3 to 5 degrees (a stamp word, a sticker pill) and pop on in 1 to 2
  frames (5/8 main)
- What never moves: the caption position, the speaker card position within a layout, the ground. There are no
  zoom punches on the face (8/8 main)
  Why: with the frame this busy, a steady face and a steady caption line stop it feeling frantic.

## Pacing
- Never cut to another shot, change the framing about every 3 seconds, and land something small about every
  1.3 seconds: a caption line, a pill, a card swap (measured: about 20 framing changes a minute, any change every
  1.27s)
- The trigger for a layout change is the script: a new claim goes to the full face, proof goes to the split, a
  number or a list goes to a full-screen card (8/8 main, read from frames)
- Never leave the frame completely unchanged for more than about 7 seconds (measured: longest still stretch 3.0s
  to 7.6s)
- First second: the frame is never plain. Either the split is already up with a title fading in by frame 2, or
  the full face is up with the first caption and a label landing within about 0.3s (7/8 main, read from frames)

## Structure
1. 0 to 3s, the hook. At frame 0 the proof is already visible and moving. A two-line title (small tracked kicker
   then one heavy line, or a white line then an accent line) sits over the proof card or the face and is gone by
   about 3 to 4s (6/8 main)
2. Each point runs the same loop: claim on the full face, proof in the split or on a full-screen card, payoff
   line back on the full face (8/8 main)
3. The end is a one-word call to action held for the last 3 to 8 seconds: a small tracked instruction line, one
   giant word in the accent colour or gradient, and a one-line promise under it. Captions keep running (6/8 main)
4. The video stops on the last spoken word. No outro card, no logo, no fade to black (8/8 main)

## Sound
- Sound effects were not measured. Nothing here is a rule about them.
- A music bed could not be confirmed either way. Where the level suggests one, the smallest gap under the voice
  was about 14 dB (measured by level only)
- Speech is nearly wall to wall: the longest pause is 0.25s to 0.63s in the 7 videos where pauses could be
  measured (measured)
- 5 of the 8 are mastered to about -14 LUFS (measured). The other 3 are 9 to 11 dB quieter, so do not treat the
  quiet ones as a target

## Variants
- Lo-fi handheld, 2 of the 10. Phone footage only: a selfie at arm's length and the phone pointed at a laptop
  screen with a finger pointing. No dark ground, no cards, no graphics. Real hard cuts, 6.6 and 7.7 a minute
  (measured). A sentence-case label in a white rounded box with black regular type is pinned near the top for
  the first 3 to 5 seconds. Captions are heavy caps, white with a black outline, 2 to 4 words on two lines at
  about 72% to 76% down (y 1380 to 1460), popping on with no fade. The active-word colour rotates between
  red-pink, cyan and magenta from line to line, and a small emoji sits beside the caption on roughly half the
  lines. No call-to-action card
- Edge-to-edge split, 1 of the 8 main. The speaker is a full-width band across the bottom 43% (below about
  y 1095) in a wider framing with no rounded cards, and the graphic zone takes the top 57%. Captions in sentence
  case. Graphics are all rebuilt mock-ups, none are real screens. Leans more on violet and magenta
- Borrowed-clip cold open, 1 of the 8 main. The first 33 seconds are an interview clip from another show, full
  frame, with its own caption set (condensed italic caps in yellow-green, phrase by phrase, about 74% down,
  y 1420), then one hard cut into the main format

## One-offs (seen once to three times, not rules)
- Numbered section tags on the full face in the top band: a violet numeral with a 1 to 4 word name under it,
  holding 1.5 to 2s. Only in videos built as a numbered list (3)
- Card headlines in sentence case in the same heavy face (3)
- A full-frame phone screen recording with captions laid straight over it, a red rounded outline drawn around
  the exact word being discussed, and a 1 to 2 frame dissolve back to the face with no dip through dark (1)
- A ring diagram that strokes on clockwise with labels popping at each stop (1)
- A hero number so large it runs off both edges of the frame at the end of its count-up (1)
- A single giant gradient word over the face for under a second (2)
- An agenda of three numbered pills stacking up right after the hook (1)
- A save-this sticker with a bookmark glyph in place of the one-word call to action (1)
- Magenta as the opposite of cyan in a two-sided comparison (2)

## Never
These held across all 8 main-format videos.
- No transitions other than the fade through dark and the card morph. No wipes, slides, spins, glitches or whip
  pans
- No zoom punches or shake on the face
- No cutaway to a second camera angle (the lo-fi variant cuts freely)
- No stock footage and no B-roll. Proof is always a real screen or a graphic built for that line
- No boxes or coloured bars behind captions, and no outline stroke on caption text (the lo-fi variant outlines
  its captions)
- No more than one highlighted word in a caption line at a time
- No emoji as decoration next to captions (the lo-fi variant uses them)
- No lower-third name strap, no persistent logo bug of the creator's own, no progress bar
- No light or white ground. The only bright surface is a real web page inside a card (the lo-fi variant has no
  designed ground at all)
- No serif, script or handwritten type
- No outro card, end screen or fade to black

## What this is based on
- 10 videos, the top 10 by views of the most recent 40 Shorts. 8 share the main format, 2 are the lo-fi variant.
- Images opened: 127 of 127 in the first pass. The measurements were then re-run and produced a fresh set of 127
  images; 3 of those were re-opened to settle numbers that disagreed with the notes, and the other 124 were not.
  Every visual rule here comes from the first pass
- Not measured: words a minute (no transcript), sound effects, whether music is present (level only), exact
  easing curves
- The cut counter flags any frame where most of the picture changes. In this style that includes instant layout
  swaps and the final frame of a file, so cuts between camera shots were counted from the sheets instead
- Framing-change and any-change counts are inflated by scrolling inside a card and by big hand gestures. Treat
  them as approximate
- Motion timings are read from 12-frames-a-second stills, so they are good to about a tenth of a second
- Positions, sizes and accent hex colours are estimates read by eye from downscaled frames. The pixel values are
  those shares worked out on 1080 x 1920, not measurements
- Fonts are identified by look. The names given are free equivalents, not the creator's licensed faces
