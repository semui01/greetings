"""Score for the birthday film. Every time comes from cues.json (exported by film.cues).

usage: python3 score.py frames/cues.json soundtrack.wav

Key of G major. The bed moves Em → Cmaj7 → Am7 → (silence when the candles go out) → G → G/D (song) →
C → D → G on the end card. The letters of HAPPY BIRTHDAY land on the first line of "Happy Birthday to
You" (public domain) and the end card resolves on its last line, both played on bells.
One sound per kind of event: candles light on mallets, rockets whistle, bursts boom and crackle,
confetti cannons pop, glasses clink.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound import (SR, Score, bell, boom, curve, fft_filter, highpass, hz, mallet, noise, pop,  # noqa: E402
                   riser, tick, tt, whoosh)

cues = json.load(open(sys.argv[1]))
dur = cues['dur']
phone = os.environ.get('VENUE') == 'phone' or cues.get('H', 1080) > cues.get('W', 1920)
sc = Score(dur, seed=11, profile='phone' if phone else 'speakers')
W = cues.get('W', 1080)
panx = lambda x: max(-.8, min(.8, (x / W - .5) * 1.6))   # noqa: E731
R = np.random.default_rng(5)


def band(d, fc, q=.7):
    y = fft_filter(noise(d), lambda f: np.exp(-(np.log(f / fc) / q) ** 2))
    return y / (np.abs(y).max() + 1e-9)


def fwump(d=.4, fc=650):
    """The soft whoomp of a flame catching."""
    t = tt(d)
    return band(d, fc, .8) * np.minimum(1, t / .015) * np.exp(-t / .09)


def puff(d=.12):
    t = tt(d)
    return band(d, 1100, .9) * np.minimum(1, t / .004) * np.exp(-t / .03)


def shaker(d=.06):
    t = tt(d)
    return highpass(noise(d), 5500) * np.minimum(1, t / .006) * np.exp(-t / .018)


def whistle(d, f0=800, f1=2300):
    """A rocket climbing: a rising tone with a little vibrato over a hiss."""
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d) * (1 + .012 * np.sin(2 * np.pi * 13 * t))
    s = .7 * np.sin(2 * np.pi * np.cumsum(f) / SR) + .35 * highpass(noise(d), 3500)
    return s * np.minimum(1, t / .06) * (1 - .7 * t / d)


def crackle(d, n, seed, late=0.):
    """Glitter after a burst: many tiny high clicks, denser early (or later for willows)."""
    rg = np.random.default_rng(seed)
    out = np.zeros(int(d * SR))
    for _ in range(n):
        t0 = late + (d - late - .02) * rg.random() ** (1.6 if not late else 1.0)
        s = tick(rg.uniform(2400, 7500), .012, .0013) * rg.uniform(.25, 1)
        i = int(t0 * SR)
        k = min(len(s), len(out) - i)
        if k > 0:
            out[i:i + k] += s[:k]
    return out


def flutter(d=1.6):
    """Paper confetti in the air: bright noise that thins out."""
    t = tt(d)
    y = highpass(noise(d), 3000) * (.6 + .4 * np.abs(np.sin(2 * np.pi * 9 * t + 3 * np.sin(2 * np.pi * 2.3 * t))))
    return y * np.minimum(1, t / .01) * np.exp(-t / .45)


def clink(f=2600, d=1.6):
    """Two champagne flutes touching: inharmonic glass partials."""
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * r * t + r) * np.exp(-t / tau)
            for r, a, tau in [(1, 1, .55), (1.47, .6, .38), (2.09, .45, .26), (2.76, .3, .17), (3.91, .2, .1)])
    return s * np.minimum(1, t / .0008)


# ---------------------------------------------------------------- bed
pull0, pull1 = cues['pull']
push0 = cues['push'][0]
g0, g1 = cues['gust']
off_end = max(cues['offs'])
glint = cues['glint']
hero = cues['hero']
close0, close1 = cues['close']
s1, s4 = cues['song1'], cues['song4']
bright = curve([(0, 450), (pull1, 1000), (push0, 1600), (g0, 2000), (off_end, 500), (glint, 700),
                (hero - .2, 3000), (hero, 4200), (close0, 3200), (s4[0], 2400), (dur, 1800)])
sc.chord(['E2', 'B2', 'E3', 'G3', 'B3', 'F#4'], .02, pull1, bright, gain=.06, att=.25)
sc.chord(['C2', 'C3', 'G3', 'B3', 'E4', 'G4'], pull0 + .2, push0 + .1, bright, gain=.06)
sc.chord(['A2', 'E3', 'G3', 'C4', 'E4'], push0, g0 + .1, bright, gain=.06)
sc.chord(['D3', 'A3', 'D4', 'G4'], g0, off_end - .05, bright, gain=.05, rel=.25)             # suspended; it stops when the candles go out
sc.chord(['G2', 'D3', 'G3', 'A3', 'B3', 'D4'], glint, hero + .1, bright, gain=.055, att=.8)
sc.chord(['G2', 'D3', 'G3', 'B3', 'D4', 'G4'], hero, s1[4], bright, gain=.06, att=.05)
sc.chord(['D3', 'A3', 'D4', 'F#4', 'A4'], s1[4], close1, bright, gain=.06, att=.08)
sc.chord(['C3', 'G3', 'C4', 'E4', 'G4'], close0 + .2, s4[3] + .5, bright, gain=.06, att=.4)
sc.chord(['D3', 'A3', 'D4', 'F#4'], s4[4] - .05, s4[5], bright, gain=.055, att=.1)
sc.chord(['G2', 'D3', 'G3', 'B3', 'D4', 'G4'], s4[5] - .05, dur + .3, bright, gain=.065, att=.1)

# ---------------------------------------------------------------- 1. the first candle
for k in range(9):   # the travelling ember crackles
    sc.add(tick(R.uniform(3000, 6500), .01, .0012), .02 + k * cues['ignite'] / 9 + R.uniform(0, .03), .05, -.6 + k * .07)
sc.add(whoosh(cues['ignite'] + .1, 500, 1800, q=.5, peak=.85), 0, .1, -.4)
sc.add(fwump(), cues['ignite'], .32, 0, rev=.3)
sc.add(bell(hz('D6'), 3, .9, 2.0, 1.2), cues['ignite'], .13, .1, rev=.6)

# ---------------------------------------------------------------- 2. pull back, the candles light in a chain
sc.add(whoosh(pull1 - pull0 + .2, 2600, 500, q=.5, peak=.35), pull0 - .1, .16, rev=.2)
dyads = [('G4', 'B4'), ('A4', 'D5'), ('B4', 'E5'), ('D5', 'G5')]
for k, t in enumerate(cues['chain']):
    for side, nt in ((-1, dyads[k][0]), (1, dyads[k][1])):
        p = side * (.2 + .15 * k)
        sc.add(tick(6000, .008, .0012), t - .22, .02, p)                  # the spark leaves
        sc.add(mallet(hz(nt), .7, .18), t, .12, p, rev=.45)
        sc.add(tick(4200, .008, .0015), t, .035, p)
        sc.add(fwump(.25, 900), t, .08, p)
pulse = np.arange(cues['chain'][0], push0 + 1.6, .25)
for k, t in enumerate(pulse):   # a light shaker keeps time while the candles burn
    sc.add(shaker(), t, .03 if k % 2 else .045, .3 if k % 2 else -.3)

# ---------------------------------------------------------------- 3. make a wish, blow
for k, nt in enumerate(['E6', 'G6', 'B6']):
    sc.add(bell(hz(nt), 2.4, .8, 2.0, 1.0), push0 + .45 + k * .09, .05, -.3 + .3 * k, rev=.8)
breath = whoosh(g1 - g0 + .2, 1600, 260, q=.9, peak=.55)
sc.add(np.vstack([breath * np.linspace(1, .35, len(breath)), breath * np.linspace(.35, 1, len(breath))]), g0, .3, rev=.15)
for k, t in enumerate(cues['offs']):
    sc.add(puff(), t, .06, -.6 + k * .15)

# ---------------------------------------------------------------- 4. the wishes rise as fireworks
for k, nt in enumerate(['G6', 'B6', 'D7', 'G7']):
    sc.add(bell(hz(nt), 1.8, .5, 2.0, .9), glint + k * .045, .045, -.5 + .33 * k, rev=.7)
t0, t1 = cues['tilt']
sc.add(whoosh(t1 - t0 + .2, 400, 3000, q=.55, peak=.7), t0 - .05, .18, rev=.2)
for t, x in zip(cues['launches'], cues['launchX']):
    sc.add(whistle(1.0), t, .035, panx(x), rev=.3)
penta = ['G5', 'B5', 'D6', 'E6', 'A5', 'D6', 'B5', 'G6']
for k, (t, x, kind) in enumerate(zip(cues['bursts'], cues['burstX'], cues['burstType'])):
    p = panx(x)
    sc.add(boom(1.3, 95, 50, .3, .5), t, .2, p * .5, rev=.35)
    sc.add(bell(hz(penta[k]), 2.0, .7, 2.0, 1.1), t, .06, p, rev=.6)
    sc.add(crackle(2.2, 70 if kind == 'willow' else 40, k, late=.35 if kind == 'willow' else 0), t + .05, .05, p, rev=.3)
sc.add(riser(1.0), hero - 1.0, .3, rev=.3)
sc.add(whistle(1.0, 600, 2000), hero - 1.0, .05, 0, rev=.3)
sc.add(boom(2.4, 85, 42, .6), hero, .5, rev=.45)
sc.add(crackle(2.6, 110, 99), hero + .05, .07, 0, rev=.4)
for k, nt in enumerate(['G5', 'B5', 'D6', 'G6']):
    sc.add(bell(hz(nt), 2.4, .9, 2.0, 1.1), hero + .02 * k, .07, -.3 + .2 * k, rev=.7)

# ---------------------------------------------------------------- 5. HAPPY BIRTHDAY (first line of the song) with a waltz
line1 = ['D5', 'D5', 'E5', 'D5', 'G5', 'F#5']
lens1 = [.35, .12, .5, .5, .5, 1.0]
for t, nt, ln in zip(s1, line1, lens1):
    sc.add(bell(hz(nt), 1.2 + ln * 2, .35 + ln * .6, 2.0, 1.1), t, .17, 0, rev=.5)
    sc.add(mallet(hz(nt) / 2, .6, .2), t, .09, 0, rev=.3)
    sc.add(tick(5000, .008, .0012), t, .04, 0)
for k, t in enumerate(cues['letters']):
    sc.add(pop(), t, .05, -.5 + (k % 5) * .25)
bar = s1[2]                                                   # downbeat on "birth"
oom = [(bar, 'G2'), (bar + 1.5, 'D3')]
pah = [(bar + .5, ['G3', 'B3', 'D4']), (bar + 1.0, ['G3', 'B3', 'D4']), (bar + 2.0, ['F#3', 'A3', 'D4'])]
for t, nt in oom:
    sc.add(boom(.7, 120, 60, .16, .45), t, .2, 0)
    sc.add(mallet(hz(nt), .7, .2), t, .1, 0)
for t, ch in pah:
    for nt in ch:
        sc.add(mallet(hz(nt), .4, .09), t, .05, R.uniform(-.3, .3))
    sc.add(shaker(), t, .05, .2)
c = cues['cannons']
for side in (-1, 1):
    sc.add(pop(), c + (.0 if side < 0 else .03), .3, .75 * side, rev=.3)
    sc.add(flutter(), c + .02, .09, .6 * side, rev=.3)

# ---------------------------------------------------------------- 6. iris closes, glasses clink, the song resolves
sc.add(whoosh(close1 - close0 + .15, 2400, 450, q=.5, peak=.4), close0, .18, rev=.2)
cl = cues['clink']
sc.add(clink(2600), cl, .22, -.15, rev=.6)
sc.add(clink(3080), cl + .009, .17, .15, rev=.6)
for k in range(10):
    sc.add(tick(R.uniform(5000, 8000), .01, .0015), cl + .05 + k * .05 + R.uniform(0, .03), .03, R.uniform(-.6, .6), rev=.5)
line4 = ['C5', 'C5', 'B4', 'G4', 'A4', 'G4']
lens4 = [.35, .12, .5, .5, .5, 1.0]
for t, nt, ln in zip(s4, line4, lens4):
    sc.add(bell(hz(nt), 1.4 + ln * 2.2, .4 + ln * .8, 2.0, 1.0), t, .15, 0, rev=.6)
    sc.add(bell(hz(nt) * 2, 1.2 + ln * 1.5, .3 + ln * .5, 2.0, .8), t, .04, .3, rev=.7)
    sc.add(tick(4600, .008, .0012), t, .02, 0)
sc.add(bell(hz('G6'), 3.0, 1.2, 3.5, 1.0), s4[5] + .02, .04, .4, rev=.8)

sc.write(sys.argv[2])
