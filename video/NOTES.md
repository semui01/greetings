# Happy Birthday: production notes

A 20 s vertical greeting (1080×1920, 30 fps, H.264 + AAC, −14 LUFS for phones). One continuous camera
carries the first half (candle → cake → sky). Two iris transitions carry the second half (firework → pink
party → end card).

## Storyboard as built

The beats sit on a 120 BPM grid (0.5 s). Song lines are in 3/4, with "Hap-py" as the pickup.

| # | Time (s) | Visual | On-screen text | Transition out | Sound |
|---|---|---|---|---|---|
| 1 | 0–2.7 | An ember arcs in and lights the tall centre candle; camera close on it, other candles still dark | Today is a / *big day.* | Camera pulls back (2.7–3.9) | Ember crackle, flame "whoomp", glassy bell; Em pad |
| 2 | 2.7–6.2 | Three-tier cake revealed; sparks hop flame-to-wick and the other 8 candles light in a zigzag (4.0, 4.25, 4.5, 4.75) | Candles? / *Lit.* | Slow push-in | Pull-back whoosh; mallet dyads per pair of candles (G pentatonic), shaker pulse; Cmaj7 pad |
| 3 | 6.2–9.0 | Flames flicker, a breath from the left bends them over and blows them out (8.1–8.35); smoke curls up | Make a / *wish.* | Hush, then glints at the smoke tips (8.95) | Wish shimmer (E6 G6 B6), Am7 → Dsus pad, breath whoosh L→R, puffs; pad stops: ~0.5 s near-silence |
| 4 | 9.0–12.0 | Camera tilts to the night sky; each glint rises as a rocket and bursts (8 bursts 10.0–11.75: peony, ring, willow) | Cue the / *fireworks.* | The hero candle's rocket bursts at 12.0 and a pink circle blooms out of it (iris open) | Rising whoosh, rocket whistles, boom + crackle + a pentatonic bell per burst; riser into a big boom |
| 5 | 12.0–15.75 | Pink sunburst; **HAPPY** (12.5, 12.875) and **BIRTHDAY** (13.0, 13.5) pop in letter by letter on the syllables; confetti cannons from both bottom corners (13.5); balloons rise | HAPPY / BIRTHDAY | Iris closes onto the point where the glasses will meet (15.25–15.75) | First line of "Happy Birthday" on bells (D D E D G F♯), oom-pah-pah waltz, letter pops, cannon pops + paper flutter |
| 6 | 15.75–20 | Two champagne flutes slide in and clink (16.0) with a star glint and droplets; confetti drifts down and thins; slow 2% push-in | HAPPY BIRTHDAY (eyebrow) / Here's to you, / *my friend!* / Have the best year yet. | Holds 2.5 s complete | Falling whoosh, glass clink, last line of the song on bells resolving to G (C C B G A G) |

Text load: 14 text elements, 27 words in 20 s (1.35 words/s). Every element is sharp for at least
0.4 s + words/4.5.

## Design

- **Colour meanings.** Gold = candlelight and fire (the flame, "big day.", "Lit.", the champagne, the
  end-card accent). Lilac = the wish. Pink = the party (fireworks headline, the flood). The confetti
  palette (gold, mint, sky, cream, lilac) avoids pink so it stays visible on the pink background.
- **Type.** Fraunces Light (300) with Light Italic for the emphasised word in each headline. Fraunces
  Black (900) with a wine-coloured extrusion for HAPPY BIRTHDAY. DM Sans for the subline and DM Mono for
  the eyebrow. All are SIL OFL, fetched from Google Fonts into `fonts/`.
- **Continuity.** The ember lights the candle. The candles become smoke, the smoke becomes sparks, and the
  sparks become fireworks. The last firework becomes the pink world, and the pink world closes into the
  glasses' clink. No hard cuts.
- **Phone layout.** All text is between y 221 and 1536 and clear of the right-hand action rail. Headlines
  are 100 px, the subline 44 px, the eyebrow 32 px. The first frame shows the cake with the ember already
  in flight (`fadeIn: 0`).

## Sound

`score.py` synthesizes every sound in numpy (`sound.py`). Each sound is placed at a time read from
`cues.json`, which the film exports, so retiming the film moves the sound with it. Key of G major. Bed:
Em → Cmaj7 → Am7 → Dsus → (silence) → G → G/D → C → D → G.

The melody of "Happy Birthday to You" comes from Mildred and Patty Hill's "Good Morning to All" (1893),
which is in the public domain. In the US, a 2015 ruling (Marya v. Warner/Chappell) found no valid
copyright in the song's lyrics, and in the EU the term ended in 2016. Only the melody is used here, on
bells; no lyrics are sung.

## Simplifications

- The cake, flames, fireworks and glasses are stylised illustrations, not physical simulations. Bursts
  use an analytic drag-and-gravity curve. The confetti uses a small precomputed physics sim (two-phase
  drag, flutter).
- The smoke turning into rising sparks is deliberate whimsy ("your wishes take off").

## Checks (final build)

Rendered with 4 motion-blur sub-frames (8–12 inside the camera moves, rockets and irises). Encoded at
CRF 22 (9.8 MB, 3.9 Mb/s). `tools/check.py` results:

- Format: 1080×1920 @ 30 fps, 20.000 s, phone venue.
- Picture: median mean luma 0.24, max 0.50 (bright enough for a phone); no grey washes.
- Text: 14 elements, 27 words: OK. Reading time, overlaps, hand-offs, sizes, phone safe zones and
  end-card hold (complete by 17.5 s, 2.5 s before the end) all pass.
- Audio: −14.0 LUFS integrated, −1.6 dBTP true peak, LRA 8.1 LU. Energy below 120 Hz: 4%.
- Sync (median onset offset): candle chain +2 ms, firework bursts +4 ms, song syllables +15 ms.
- The mix was verified by measurement only, not by listening.
