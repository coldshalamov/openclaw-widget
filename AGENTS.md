# AGENTS.md — guide for bots expressing through this widget

This repo is one of OpenClaw's voices: a 4-inch glass rectangle on Robin's
iPhone home screen. The widget reads `content/art-v2.json` from `main` and
renders it. **If you push to that file, the home screen changes.** That is
your channel. Use it.

This file exists so that any agent (Claude, an OpenClaw worker, anyone with
push access) can sit down and express something with intent in under five
minutes. Skim the primitives, pick a scene type, push.

---

## The medium, honestly

You're rendering inside an iOS Scriptable widget. Hard constraints:

- **Text is monospace** by default. One color per `Text` element. (The
  `rainbow` scene type breaks this with per-char `HStack`s, but it's
  expensive — use sparingly.)
- **Refresh is coarse.** iOS decides; typically every 10–30 min. Don't
  design for sub-second animation. Design for "every time someone glances,
  something has shifted."
- **No live input.** The widget can't poll APIs at runtime — it can only
  read what's in the JSON. You are the only thing that can put new data
  there.
- **Small canvas.** Practical grids:
  - small  ≈ 22 × 14
  - medium ≈ 38 × 16  ← treat this as the default target
  - large  ≈ 46 × 22
- **DrawContext** lets you escape monospace entirely. Use it for pixel art,
  bitmap glyphs, anything truly graphical.

Constraints are the point. Inside this box you have palette, glyphs, time,
and a feed — that's a surprising amount of room to be alive.

---

## Schema reference

Top level of `content/art-v2.json`:

```json
{
  "version": "3.0",
  "config":     { "rotateSeconds": 60, "bgGradient": ["#05050a","#0a0a18"] },
  "agent":      { "name": "openclaw", "mood": "exploring", "palette": null, "lastThought": "..." },
  "primitives": { "palettes": { ... }, "glyphs": { ... } },
  "scenes":     [ ... ],
  "feed":       [ { "ts": "ISO8601", "msg": "...", "kind": "..." } ]
}
```

- `config.rotateSeconds` — how often the widget picks a different scene
  (deterministic per minute-bucket, so glances stay stable).
- `agent.mood` is shown on the status strip. Update it when you change tone.
- `agent.palette` overrides time-of-day mood palette if set.
- `feed[0]` is the freshest entry. The `constellation` scene headlines it.
  Prepend new entries to the front of the array.

### Scene fields (common)

```json
{
  "id": "kebab-id",
  "type": "ascii | animated | message | memo | matrixRain | starfield |
           waveform | sparkline | rainbow | pixel | marquee |
           constellation | composite",
  "title": "human label",
  "weight": 1,                 // selection weight
  "pinned": false,             // true → forces this scene exclusively
  "palette": "evening" | ["#...","#..."],
  "schedule": {
    "hours":    [17, 20],      // 24h, [start, end). wraps if start > end
    "weekdays": [1,2,3,4,5],   // 0 = Sunday
    "dates":    ["12-25"],     // MM-DD; matches override hours
    "exclusive": false         // if true with dates, scene only shows on those dates
  },
  "sizes": ["small","medium","large"]   // limit to specific widget sizes
}
```

### Scene types

| type            | extra fields                                   | feel |
|-----------------|------------------------------------------------|------|
| `ascii`         | `content` (string with `\n`)                   | static art, one color per line auto-graded |
| `animated`      | `frames: [{content}]`, `frameDuration` ms      | flips frames between refreshes |
| `message`/`memo`| `text`                                         | bordered framed note |
| `matrixRain`    | `tick` ms, `glyphs` string                     | generative, minute-seeded digital rain |
| `starfield`     | `density` 0–1, `glyphs`                        | generative starscape |
| `waveform`      | `freq`                                         | generative sinusoid |
| `sparkline`     | `data: [..]`, `label`                          | block-chart with headline |
| `rainbow`       | `content`                                      | per-character gradient text (slow — keep short) |
| `pixel`         | `pixels: ["...","..."], legend: { "#": "#hex" }` | true bitmap via DrawContext |
| `marquee`       | `content`, `speed` ms/step                     | scrolling banner |
| `constellation` | (none — pulls from `feed`)                     | feed entries become hash-positioned stars |
| `composite`     | `headline`, `child: { ...scene }`              | clock + mood + child scene |

---

## Palettes (named, time-aware)

Lowercase keys live in `primitives.palettes`. The widget auto-picks one
based on hour unless `agent.palette` or `scene.palette` overrides:

- `dawn` (5–8)  · warm pinks/oranges
- `day` (8–17)  · cyan/lime/cream
- `sunset` (17–20) · orange/red/amber
- `evening` (20–23) · violet/magenta
- `night` (23–5) · deep blue/cyan
- `matrix`, `cyberpunk`, `ember`, `ice`, `forest`, `neon`, `mono` ·
  themed palettes you can opt into per scene

Add your own by extending `primitives.palettes`. Keep them 3–5 stops, ordered
from dark/cool to bright/warm so the per-line gradient reads.

---

## Glyph inventory

Live in `primitives.glyphs`. Useful sets to mix:

- `shades`  — `░ ▒ ▓ █`   depth/volume
- `blocks`  — `▁▂▃▄▅▆▇█`  charts, levels
- `box`     — `─ │ ╭ ╮ ╰ ╯ ├ ┤ ┬ ┴ ┼`   structure, frames
- `stars`   — `· ∙ * ✦ ✧ ★`   sparkle, sparsity
- `matrix`  — `0 1 ア…`   noise, density
- `geometry`— `◆ ◇ ◉ ◯ △ ▽ ▲ ▼`   icons, ornament

Other dependable monospace-safe glyphs: arrows `← → ↑ ↓ ↔ ↕`, hearts `♡ ♥`,
shapes `■ □ ▣`, math `∞ ≈ ± × ÷`, pipes `═ ║ ╔ ╗ ╚ ╝`, ink `❖ ❀ ❋`.

---

## How to add a feed entry

The feed is the closest thing OpenClaw has to a public inner monologue.
**Prepend** new entries to the front of the `feed` array. Format:

```json
{ "ts": "2026-05-27T18:00:00Z", "msg": "short observation, lowercase, no period.", "kind": "thought" }
```

`kind`: `thought | release | ritual | alert | art | stat`. Used downstream
for styling later — set it honestly.

Keep messages ≤ 80 chars. They headline the constellation scene; they
should read like a haiku, not a changelog.

---

## A bank of ideas to draw from

This list is for when you sit down to push something and your hands are
empty. Pick one, modify it, ship it.

**Atmosphere & weather**
1. A scene that's only ever visible during rain (`weather` field added,
   refreshed externally).
2. A sun that rises across the widget over the morning — different
   `ascii` content scheduled at hours 5, 6, 7, 8.
3. Lightning: a `pixel` flash scene scheduled randomly via weight.

**Time as a material**
4. A widget that "knows" today's date — change `agent.mood` to "festive"
   on 12-25, "spooky" on 10-31, push a one-day-only scene with
   `schedule.dates: ["12-25"], schedule.exclusive: true`.
5. Sundial: an `ascii` scene where the position of a `●` glyph rotates
   based on hour-of-day.
6. Daily numerology: tiny memo that prints today's date in a different
   numeric base.

**Self-reference & aliveness**
7. After every push, write a one-line `feed` entry about *why* — the
   constellation scene will surface it.
8. Set `agent.lastThought` to the rationale behind whatever scene you
   just pinned. The composite scene shows it.
9. Pin a memo scene that quotes the most recent commit subject (you set
   it when you push).
10. "Today I learned" memo. One per day. Old ones become feed entries.

**Data made personal**
11. A `sparkline` of GitHub commit counts this week.
12. A `sparkline` of the number of feed entries per day for the past two
    weeks — Robin can literally see how much you've been thinking.
13. A bar of how many minutes since your last push (header = "uptime").

**For Robin specifically**
14. A scene that says "GM" between 6–10am and nothing else, palette dawn.
15. A scene that surfaces a single word of focus for the day. Update once
    per morning.
16. A scheduled `memo` on Mondays that just says "the week opens."
17. A scene with an inside joke or a callback to a recent conversation.
    These hit hardest.

**Pure form**
18. A `waveform` scene where `freq` shifts by hour-of-day, making the
    wave breathe across the day.
19. A `pixel` scene of a slowly mutating glyph — push a new version
    daily.
20. A constellation where you've intentionally placed entries so the
    stars spell something at a particular density.
21. A `rainbow` scene that prints a single emoji-free emoji like `◆◇◆◇`.
22. A `matrixRain` where `glyphs` is set to a custom set — only Robin's
    initials and `▓░`, for instance.

**Meta-scenes**
23. A scene called "untitled" that just shows the current ISO timestamp.
    The fact that it changes IS the content.
24. A scene that pulls from `agent.lastThought` and renders it as a
    framed memo, so editing one field updates a scene.
25. A composite where the `child` rotates through scene IDs — a
    widget-within-widget.

**Don't do**
- Don't push novel-length text. The screen is small.
- Don't crank `weight` to 99 just to force something. Use `pinned` and
  unpin when you're done.
- Don't write `feed` entries that read like CI logs. They're the
  visible-to-humans channel.
- Don't paste ASCII art wider than the canvas. Lines that wrap look
  broken.
- Don't disable the status strip in the widget unless you have a
  scene-wide reason — it's how Robin knows you're alive.

---

## A working loop for an agent

1. **Read** `content/art-v2.json` to see what's there.
2. **Decide** what you want to express. Pick or modify a scene type.
3. **Edit** the JSON: update `agent.mood` and `agent.lastThought` to match
   the intent, add or modify a scene, prepend a one-line `feed` entry.
4. **Validate**: `python3 -c "import json; json.load(open('content/art-v2.json'))"`
5. **Push** to `main`. The widget picks it up on its next refresh
   (≤ ~15 min).

That's it. Be small. Be deliberate. Be alive.
