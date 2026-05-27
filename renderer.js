// OpenClaw renderer. Fetched & eval'd by widget.js (the Scriptable bootloader)
// every refresh. To change how the widget looks or add a new scene type,
// push to this file on `main` — the phone picks it up automatically.
//
// Entry point: function buildWidget(content) → ListWidget

const FALLBACK_PALETTE = ["#00ff41", "#00d4ff", "#ffd96b"];
const REFRESH_SECONDS = 600;

// ─── color ──────────────────────────────────────────────────────────────────
function hex2rgb(h) {
  return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
}
function rgb2hex(r, g, b) {
  function p(n) { return Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, "0"); }
  return "#" + p(r) + p(g) + p(b);
}
function lerp(a, b, t) { return a + (b - a) * t; }
function lerpHex(a, b, t) {
  var A = hex2rgb(a), B = hex2rgb(b);
  return rgb2hex(lerp(A[0], B[0], t), lerp(A[1], B[1], t), lerp(A[2], B[2], t));
}
function rampColor(palette, t) {
  if (!palette || !palette.length) return "#00ff41";
  if (palette.length === 1) return palette[0];
  t = Math.max(0, Math.min(0.9999, t));
  var seg = 1 / (palette.length - 1);
  var i = Math.floor(t / seg);
  return lerpHex(palette[i], palette[i + 1], (t - i * seg) / seg);
}
function resolvePalette(name, content) {
  if (Array.isArray(name)) return name;
  var p = content.primitives && content.primitives.palettes;
  if (p && name && p[name]) return p[name];
  return FALLBACK_PALETTE;
}
function moodPalette(content) {
  var agent = content.agent || {};
  if (agent.palette) return resolvePalette(agent.palette, content);
  var h = new Date().getHours();
  var key = h < 5 ? "night" : h < 8 ? "dawn" : h < 17 ? "day" : h < 20 ? "sunset" : h < 23 ? "evening" : "night";
  var p = content.primitives && content.primitives.palettes;
  if (p && p[key]) return p[key];
  return FALLBACK_PALETTE;
}

// ─── deterministic rng ──────────────────────────────────────────────────────
function rngFor(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function strHash(s) {
  var h = 2166136261;
  for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

// ─── scene selection ────────────────────────────────────────────────────────
function chooseScene(content) {
  var scenes = content.scenes || content.art || [];
  if (!scenes.length) return null;
  var now = new Date();
  var hour = now.getHours();
  var dow = now.getDay();
  var mmdd = String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  var fam = config.widgetFamily || "medium";
  var eligible = scenes.filter(function (s) {
    if (s.sizes && s.sizes.indexOf(fam) < 0) return false;
    if (!s.schedule) return true;
    var sched = s.schedule;
    if (sched.dates && sched.dates.indexOf(mmdd) >= 0) return true;
    if (sched.dates && sched.exclusive) return false;
    if (sched.hours) {
      var h0 = sched.hours[0], h1 = sched.hours[1];
      if (h0 <= h1 ? (hour < h0 || hour >= h1) : (hour < h0 && hour >= h1)) return false;
    }
    if (sched.weekdays && sched.weekdays.indexOf(dow) < 0) return false;
    return true;
  });
  if (!eligible.length) eligible = scenes;
  var pinned = eligible.filter(function (s) { return s.pinned; });
  if (pinned.length) eligible = pinned;
  var weights = eligible.map(function (s) { return Math.max(0.01, s.weight || 1); });
  var total = weights.reduce(function (a, b) { return a + b; }, 0);
  var rotateEvery = (content.config && content.config.rotateSeconds) || 60;
  var seed = Math.floor(Date.now() / (rotateEvery * 1000));
  var rng = rngFor(seed);
  var r = rng() * total;
  for (var i = 0; i < eligible.length; i++) {
    r -= weights[i];
    if (r <= 0) return eligible[i];
  }
  return eligible[eligible.length - 1];
}

// ─── size profile ───────────────────────────────────────────────────────────
function sizeProfile() {
  var s = config.widgetFamily || "medium";
  if (s === "small") return { cols: 22, rows: 14, fs: 6, draw: 240 };
  if (s === "large") return { cols: 46, rows: 22, fs: 9, draw: 480 };
  if (s === "extraLarge") return { cols: 96, rows: 22, fs: 9, draw: 720 };
  return { cols: 38, rows: 16, fs: 8, draw: 360 };
}

// ─── text helpers ───────────────────────────────────────────────────────────
function addMono(stack, s, color, fs) {
  var t = stack.addText(s);
  t.font = Font.systemFont(fs, "monospaced");
  t.textColor = new Color(color);
  t.lineLimit = 1;
  t.minimumScaleFactor = 0.4;
  return t;
}

// ─── renderers ──────────────────────────────────────────────────────────────
function renderAscii(stack, scene, palette, sz) {
  var lines = (scene.content || "").split("\n");
  var n = Math.max(1, lines.length - 1);
  for (var i = 0; i < lines.length; i++) {
    var col = scene.color || rampColor(palette, n ? i / n : 0.5);
    addMono(stack, lines[i] || " ", col, sz.fs);
  }
}

function renderAnimated(stack, scene, palette, sz) {
  var frames = scene.frames || [];
  if (!frames.length) return;
  var dur = scene.frameDuration || 1000;
  var idx = Math.floor(Date.now() / dur) % frames.length;
  var f = frames[idx];
  renderAscii(stack, { content: f.content || f, color: scene.color }, palette, sz);
}

function renderMessage(stack, scene, palette, sz) {
  var raw = (scene.text || scene.content || "").split("\n");
  var maxW = Math.min(sz.cols - 2, Math.max.apply(null, raw.map(function (l) { return l.length; })));
  var border = "╭" + "─".repeat(maxW) + "╮";
  var bot = "╰" + "─".repeat(maxW) + "╯";
  addMono(stack, border, palette[0], sz.fs);
  for (var i = 0; i < raw.length; i++) {
    var line = raw[i].length > maxW ? raw[i].slice(0, maxW) : raw[i] + " ".repeat(maxW - raw[i].length);
    var col = rampColor(palette, raw.length > 1 ? i / (raw.length - 1) : 0.5);
    addMono(stack, "│" + line + "│", col, sz.fs);
  }
  addMono(stack, bot, palette[palette.length - 1], sz.fs);
}

function renderMatrixRain(stack, scene, palette, sz) {
  var cols = sz.cols, rows = sz.rows;
  var seed = Math.floor(Date.now() / (scene.tick || 800));
  var rng = rngFor(seed);
  var charset = (scene.glyphs || "01アイウエオカキクケコ▓▒░").split("");
  var grid = [];
  for (var r = 0; r < rows; r++) grid.push(new Array(cols).fill(" "));
  for (var c = 0; c < cols; c++) {
    var head = Math.floor(rng() * (rows + 6)) - 3;
    var len = 3 + Math.floor(rng() * 9);
    for (var rr = 0; rr < rows; rr++) {
      var d = head - rr;
      if (d >= 0 && d < len) grid[rr][c] = charset[Math.floor(rng() * charset.length)];
    }
  }
  for (var i = 0; i < rows; i++) addMono(stack, grid[i].join(""), rampColor(palette, i / Math.max(1, rows - 1)), sz.fs);
}

function renderStarfield(stack, scene, palette, sz) {
  var cols = sz.cols, rows = sz.rows;
  var seed = Math.floor(Date.now() / 60000);
  var rng = rngFor(seed);
  var glyphs = (scene.glyphs || "·∙*✦✧").split("");
  var grid = [];
  for (var r = 0; r < rows; r++) grid.push(new Array(cols).fill(" "));
  var density = scene.density || 0.07;
  var n = Math.floor(cols * rows * density);
  for (var i = 0; i < n; i++) {
    var rr = Math.floor(rng() * rows), cc = Math.floor(rng() * cols);
    grid[rr][cc] = glyphs[Math.floor(rng() * glyphs.length)];
  }
  for (var j = 0; j < rows; j++) addMono(stack, grid[j].join(""), rampColor(palette, j / Math.max(1, rows - 1)), sz.fs);
}

function renderWaveform(stack, scene, palette, sz) {
  var cols = sz.cols, rows = sz.rows;
  var t0 = Date.now() / 1000;
  var grid = [];
  for (var r = 0; r < rows; r++) grid.push(new Array(cols).fill(" "));
  var freq = scene.freq || 0.42;
  var amp = (rows - 2) / 2;
  var mid = (rows - 1) / 2;
  for (var x = 0; x < cols; x++) {
    var y1 = Math.round(mid + amp * Math.sin(x * freq + t0 * 0.3));
    var y2 = Math.round(mid + amp * 0.55 * Math.sin(x * freq * 1.7 + t0 * 0.5 + 1));
    if (y1 >= 0 && y1 < rows) grid[y1][x] = "█";
    if (y2 >= 0 && y2 < rows && grid[y2][x] === " ") grid[y2][x] = "▒";
  }
  for (var i = 0; i < rows; i++) addMono(stack, grid[i].join(""), rampColor(palette, i / Math.max(1, rows - 1)), sz.fs);
}

function renderSparkline(stack, scene, palette, sz) {
  var data = scene.data || [];
  if (!data.length) return;
  var lo = Math.min.apply(null, data), hi = Math.max.apply(null, data);
  if (hi === lo) hi = lo + 1;
  var blocks = "▁▂▃▄▅▆▇█";
  var line = data.map(function (v) { return blocks[Math.floor((v - lo) / (hi - lo) * 7.999)]; }).join("");
  if (scene.title) {
    var t1 = stack.addText(scene.title);
    t1.font = Font.boldSystemFont(sz.fs + 2);
    t1.textColor = new Color(palette[0]);
  }
  addMono(stack, line, rampColor(palette, 0.5), sz.fs * 2);
  if (scene.label) addMono(stack, scene.label, palette[palette.length - 1], sz.fs);
}

function renderRainbow(stack, scene, palette, sz) {
  var lines = (scene.content || scene.text || "").split("\n");
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (!line.length) { var empty = stack.addText(" "); empty.font = Font.systemFont(sz.fs, "monospaced"); continue; }
    var row = stack.addStack();
    row.layoutHorizontally();
    row.spacing = 0;
    var width = Math.min(line.length, 80);
    for (var c = 0; c < width; c++) {
      var ch = line[c];
      var t = row.addText(ch === " " ? " " : ch);
      t.font = Font.systemFont(sz.fs, "monospaced");
      t.textColor = new Color(rampColor(palette, width > 1 ? c / (width - 1) : 0.5));
      t.lineLimit = 1;
    }
  }
}

function renderPixelArt(stack, scene, palette, sz) {
  var pixels = scene.pixels || [];
  if (!pixels.length) return;
  var rows = pixels.length;
  var cols = Math.max.apply(null, pixels.map(function (r) { return r.length; }));
  var legend = scene.legend || {};
  var ctx = new DrawContext();
  ctx.size = new Size(sz.draw, sz.draw);
  ctx.opaque = false;
  ctx.respectScreenScale = true;
  var pw = sz.draw / cols;
  var ph = sz.draw / rows;
  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < pixels[r].length; c++) {
      var sym = pixels[r][c];
      if (sym === " " || sym === ".") continue;
      var col = legend[sym] || rampColor(palette, (c + r) / (cols + rows));
      ctx.setFillColor(new Color(col));
      ctx.fillRect(new Rect(c * pw, r * ph, Math.ceil(pw) + 0.5, Math.ceil(ph) + 0.5));
    }
  }
  var img = stack.addImage(ctx.getImage());
  img.applyFittingContentMode();
  img.centerAlignImage();
}

function renderMarquee(stack, scene, palette, sz) {
  var text = (scene.content || scene.text || "").replace(/\s+/g, " ") + "   ◆   ";
  var w = sz.cols;
  var period = Math.max(120, scene.speed || 250);
  var offset = Math.floor(Date.now() / period) % (text.length + w);
  var padded = " ".repeat(w) + text + " ".repeat(w);
  var window = padded.slice(offset, offset + w);
  var preLines = Math.max(0, Math.floor(sz.rows / 2) - 2);
  for (var i = 0; i < preLines; i++) { var empty = stack.addText(" "); empty.font = Font.systemFont(sz.fs, "monospaced"); }
  addMono(stack, "─".repeat(w), palette[0], sz.fs);
  addMono(stack, window, rampColor(palette, 0.5), sz.fs);
  addMono(stack, "─".repeat(w), palette[palette.length - 1], sz.fs);
}

function renderConstellation(stack, scene, palette, sz, content) {
  var feed = content.feed || [];
  var cols = sz.cols, rows = sz.rows - 2;
  var grid = [];
  for (var r = 0; r < rows; r++) grid.push(new Array(cols).fill(" "));
  var brightness = [];
  for (var r2 = 0; r2 < rows; r2++) brightness.push(new Array(cols).fill(0));
  var now = Date.now();
  var horizon = 14 * 24 * 3600 * 1000;
  var glyphs = ["·", "∙", "*", "✦", "★"];
  for (var i = 0; i < feed.length; i++) {
    var entry = feed[i];
    var h = strHash((entry.msg || "") + (entry.ts || i));
    var cc = h % cols;
    var rr = Math.floor(h / cols) % rows;
    var age = now - Date.parse(entry.ts || 0);
    if (isNaN(age) || age < 0) age = horizon;
    var freshness = Math.max(0, 1 - age / horizon);
    if (freshness > brightness[rr][cc]) {
      brightness[rr][cc] = freshness;
      var g = Math.min(glyphs.length - 1, Math.floor(freshness * glyphs.length));
      grid[rr][cc] = glyphs[g];
    }
  }
  var rng = rngFor(strHash("bg" + Math.floor(now / 3600000)));
  var bg = Math.floor(cols * rows * 0.04);
  for (var b = 0; b < bg; b++) {
    var br = Math.floor(rng() * rows), bc = Math.floor(rng() * cols);
    if (grid[br][bc] === " ") grid[br][bc] = "·";
  }
  if (feed.length) {
    var newest = feed[0];
    addMono(stack, "» " + (newest.msg || "").slice(0, cols - 2), palette[0], sz.fs);
  }
  for (var j = 0; j < rows; j++) {
    addMono(stack, grid[j].join(""), rampColor(palette, j / Math.max(1, rows - 1)), sz.fs);
  }
}

function renderComposite(stack, scene, palette, sz, content) {
  var top = stack.addStack();
  top.layoutHorizontally();
  top.centerAlignContent();
  var dt = new Date();
  var hhmm = String(dt.getHours()).padStart(2, "0") + ":" + String(dt.getMinutes()).padStart(2, "0");
  var tt = top.addText(hhmm);
  tt.font = Font.boldSystemFont(sz.fs * 2.4);
  tt.textColor = new Color(palette[0]);
  top.addSpacer();
  var agent = content.agent || {};
  var mood = (agent.mood || "idle").toUpperCase();
  var mt = top.addText(mood);
  mt.font = Font.systemFont(sz.fs);
  mt.textColor = new Color(palette[palette.length - 1]);
  if (scene.headline) {
    var hl = stack.addText(scene.headline);
    hl.font = Font.systemFont(sz.fs + 1);
    hl.textColor = new Color(rampColor(palette, 0.5));
    hl.lineLimit = 1;
    hl.minimumScaleFactor = 0.5;
  }
  if (scene.child) {
    stack.addSpacer(2);
    renderScene(stack, scene.child, palette, sz, content);
  } else if (agent.lastThought) {
    stack.addSpacer(2);
    var line = "“" + agent.lastThought + "”";
    addMono(stack, line.length > sz.cols ? line.slice(0, sz.cols - 1) + "…" : line, palette[1] || palette[0], sz.fs);
  }
}

function renderScene(stack, scene, palette, sz, content) {
  if (!scene) return;
  var p = palette;
  if (scene.palette) p = resolvePalette(scene.palette, content);
  switch (scene.type || "ascii") {
    case "animated": return renderAnimated(stack, scene, p, sz);
    case "message":
    case "memo": return renderMessage(stack, scene, p, sz);
    case "matrixRain": return renderMatrixRain(stack, scene, p, sz);
    case "starfield": return renderStarfield(stack, scene, p, sz);
    case "waveform": return renderWaveform(stack, scene, p, sz);
    case "sparkline": return renderSparkline(stack, scene, p, sz);
    case "rainbow": return renderRainbow(stack, scene, p, sz);
    case "pixel": return renderPixelArt(stack, scene, p, sz);
    case "marquee": return renderMarquee(stack, scene, p, sz);
    case "constellation": return renderConstellation(stack, scene, p, sz, content);
    case "composite": return renderComposite(stack, scene, p, sz, content);
    case "ascii":
    default: return renderAscii(stack, scene, p, sz);
  }
}

function addStatusStrip(parent, content, palette, sz) {
  var strip = parent.addStack();
  strip.layoutHorizontally();
  strip.centerAlignContent();
  var beats = "▁▂▃▄▅▆▇█▇▆▅▄▃▂";
  var hb = beats[Math.floor(Date.now() / 1000) % beats.length];
  var agent = content.agent || {};
  var name = agent.name || "openclaw";
  var mood = agent.mood ? " · " + agent.mood : "";
  var left = "●" + hb + " " + name + mood;
  var l = strip.addText(left);
  l.font = Font.systemFont(Math.max(6, sz.fs - 1), "monospaced");
  l.textColor = new Color(palette[palette.length - 1], 0.7);
  l.lineLimit = 1;
  l.minimumScaleFactor = 0.5;
  strip.addSpacer();
  var now = new Date();
  var hh = String(now.getHours()).padStart(2, "0");
  var mm = String(now.getMinutes()).padStart(2, "0");
  var r = strip.addText(hh + ":" + mm);
  r.font = Font.systemFont(Math.max(6, sz.fs - 1), "monospaced");
  r.textColor = new Color(palette[0], 0.7);
}

// ─── entry point ───────────────────────────────────────────────────────────
function buildWidget(content) {
  var palette = moodPalette(content);
  var sz = sizeProfile();

  var w = new ListWidget();
  var bgPalette = (content.config && content.config.bgGradient) || ["#000000", "#0a0a14"];
  var bg = new LinearGradient();
  bg.colors = bgPalette.map(function (c) { return new Color(c); });
  bg.locations = bgPalette.map(function (_, i) { return i / Math.max(1, bgPalette.length - 1); });
  bg.startPoint = new Point(0, 0);
  bg.endPoint = new Point(1, 1);
  w.backgroundGradient = bg;
  w.setPadding(6, 6, 4, 6);

  var body = w.addStack();
  body.layoutVertically();

  var scene = chooseScene(content);
  renderScene(body, scene, palette, sz, content);

  w.addSpacer();
  addStatusStrip(w, content, palette, sz);

  return w;
}
