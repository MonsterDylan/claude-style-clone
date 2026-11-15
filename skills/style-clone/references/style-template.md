# Style file template

Copy this shape into `STYLE.md`. Delete any section or line the evidence can't support rather than filling it with
guesses, and add a section when the style has something this shape has no place for (a recurring panel treatment,
for example).
Every rule ends with a count like `(8/10)`. Every number is marked `measured` or `read from frames`.

```markdown
# <Short name for the style> style

<Two or three sentences: what this style feels like, what kind of video it is for, and the one idea that holds it
together. Example: "Everything arrives by coming into focus. Nothing slides in.">

Source: <platform> @<handle> (or "<N> links chosen by the user" when there is no handle), <N> videos, <how chosen:
"top 10 by views of the most recent 40" or "picked by the user">, analysed <date>. Counts below are out of <N, or
the M videos in the main format>. This file models the style. It does not license copying any video, logo, name,
face or product.

## The numbers
- Words a minute: <n> (measured, <k> videos with a transcript)
- Hard cuts a minute: <n> (measured, or counted from sheets if the measurement was off)
- Framing changes a minute (cuts, jump cuts, punch-ins, moves): <n> (measured, approximate)
- Something changes on screen every <n>s (measured: median gap between changes of any size)
- Length: <range>
- Music bed: <likely / no / unclear> (measured by level only) at about <n> dB under the voice
- Loudness: <n> LUFS (measured)

## Layout (1080 x 1920)
- <Where the speaker sits, with coordinates or shares of the frame> (n/10)
- <Where graphics sit>
- <Where captions sit>
- <What the second framing is, if there is one, and how often it appears>
  Why: <one line, if you can infer it>

## Type
- <Face 1: what kind, weight, case, tracking, what it is used for. Closest free equivalent: <name>> (n/10)
- <Face 2 ...>
- <Sizes: cap height as a share of frame width, and the px that is on a 1080-wide frame (read from frames)>

## Colour
- Ground: <hex>, about <n>% of the frame (measured). <If the style alternates grounds, list each and when it is used.>
- Accent: <hex> (read from frames). Used for: <the specific things>. Never for: <...> (n/10)
- <Glow, outline, gradient rules, if any>
- <What colours mean: gain, loss, emphasis>

## Captions
- <Words at a time, case, punctuation kept or dropped, box or none, colour, position, how each one arrives> (n/10)

## Motion
- <How titles arrive: the move, the duration, the stagger> (n/10, read from frames)
- <How lists / diagrams / screenshots arrive>
- <How things leave>
- <What a picture cut looks like: hard cut, or a transition, and which>
- <Easing: snappy, linear, overshoot or none>
- <What never moves>
  Why: <...>

## Pacing
- <Cut rate against change rate, in words an editor can act on>
- <The first second: what is on screen at frame 0>
- <How often the framing changes and what triggers it>

## Structure
1. <0 to Ns: what the hook looks like, and what is on screen at frame 0>
2. <How sections are announced>
3. <How it ends: the last shot, and what the call to action looks like if there is one>

## Sound
- <Only what the evidence supports. Music bed yes or no. Sound effects are not measured: say so, and either leave
  this out or mark it "by ear, not measured" if you were told.>

## Variants
- <A second format that some videos use, how many, and how it differs>

## One-offs (seen in fewer than half, not rules)
- <...>

## Never
- <Things absent from every video looked at. Half of taste is restraint.>

## What this is based on
- <N> videos, <how chosen>. Images opened: <a> of <b>.
- Not measured: sound effects; exact easing curves; anything after the first 3 minutes of a video.
- Motion timings are read from 12-frames-a-second stills, so they are good to about a tenth of a second.
- Fonts are identified by look. The names given are free equivalents, not the creator's licensed faces.
```
