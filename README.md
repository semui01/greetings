# greetings

**`happy-birthday.mp4`**: a 20-second vertical (1080×1920, 9:16) birthday greeting for a good friend,
with a synthesized soundtrack. It's sized for phones, so it works in messaging apps, Stories, Reels and Shorts.
`happy-birthday-poster.jpg` is its last frame, which you can use as a cover image.

A candle lights, the camera pulls back to a cake whose candles catch one by one ("Candles? *Lit.*"), you
make a wish and blow them out, and the smoke rises as fireworks. The last firework floods the screen pink,
and **HAPPY BIRTHDAY** lands letter by letter on the notes of the song while confetti cannons fire and
balloons float up. An iris closes onto two champagne glasses that clink: *"Here's to you, my friend! Have
the best year yet."*

## Put your friend's name on it

Edit `video/greeting.js`:

```js
window.GREETING = { name: 'Alex' };   // end card: "Here's to you, Alex!"
```

Then rebuild (needs Node 18+ with Playwright/Chromium, ffmpeg, Python 3 with numpy):

```bash
cd video
./build.sh /tmp/frames ../happy-birthday.mp4      # about 3–5 minutes; DRAFT=1 for a quick preview
```

You can also open `video/film.html` in a browser for a live preview (space bar = play/pause, arrow keys = step).

## What's inside

| Path | What |
|---|---|
| `video/film.html` | The film: a deterministic canvas animation. Every frame is a pure function of time |
| `video/score.py` | The soundtrack, synthesized in numpy from the film's cue times so every sound lands on its frame |
| `video/greeting.js` | Personalisation (the friend's name) |
| `video/NOTES.md` | Storyboard, timings, design choices and the check results |
| `video/engine.js`, `render.mjs`, `build.sh`, `sound.py`, `tools/` | Render engine: headless Chromium frames, motion blur, ffmpeg encode, automatic checks |
| `video/fonts/` | Fraunces, DM Sans, DM Mono (SIL Open Font License) |
