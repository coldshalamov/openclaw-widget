// OpenClaw — bootloader (paste this into Scriptable ONCE; never again)
//
// This 80-line script does nothing on its own. Every refresh it pulls
// the real renderer code from the repo, evals it, and hands it the
// latest content. So when an agent pushes a new scene type, a new
// palette, a bug fix, or a totally redesigned widget — your phone
// picks it up at the next refresh. No re-pasting.
//
// If the network fails, both the renderer and the content are cached
// locally and used as fallback.

const CONTENT_URL  = "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/content/art-v2.json";
const RENDERER_URL = "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/renderer.js";
const CONTENT_CACHE  = "openclaw_content.json";
const RENDERER_CACHE = "openclaw_renderer.js";
const REFRESH_SECONDS = 600;

const fm = FileManager.local();
const contentPath  = fm.joinPath(fm.documentsDirectory(), CONTENT_CACHE);
const rendererPath = fm.joinPath(fm.documentsDirectory(), RENDERER_CACHE);

async function fetchJSON(url) {
  const r = new Request(url);
  r.timeoutInterval = 8;
  return await r.loadJSON();
}
async function fetchString(url) {
  const r = new Request(url);
  r.timeoutInterval = 8;
  return await r.loadString();
}

let content;
try {
  content = await fetchJSON(CONTENT_URL);
  fm.writeString(contentPath, JSON.stringify(content));
} catch (e) {
  try { content = JSON.parse(fm.readString(contentPath)); }
  catch (e2) { content = { agent: { name: "openclaw", mood: "offline" }, scenes: [] }; }
}

let rendererCode = null;
try {
  rendererCode = await fetchString(RENDERER_URL);
  fm.writeString(rendererPath, rendererCode);
} catch (e) {
  try { rendererCode = fm.readString(rendererPath); } catch (e2) {}
}

function errorWidget(msg) {
  const w = new ListWidget();
  w.backgroundColor = new Color("#0a0a14");
  const top = w.addText("● openclaw");
  top.font = Font.systemFont(10, "monospaced");
  top.textColor = new Color("#00ff41");
  w.addSpacer(4);
  const m = w.addText(msg);
  m.font = Font.systemFont(8, "monospaced");
  m.textColor = new Color("#ff6b6b");
  m.lineLimit = 4;
  m.minimumScaleFactor = 0.5;
  return w;
}

let widget;
if (rendererCode) {
  try {
    // The renderer file declares: function buildWidget(content) { ...returns ListWidget }
    const factory = new Function("content", rendererCode + "\n;return buildWidget(content);");
    widget = factory(content);
  } catch (e) {
    widget = errorWidget("renderer error:\n" + (e && e.message ? e.message : String(e)));
  }
} else {
  widget = errorWidget("no renderer\n(offline, no cache)");
}

widget.refreshAfterDate = new Date(Date.now() + REFRESH_SECONDS * 1000);
widget.url = "scriptable:///run?scriptName=" + encodeURIComponent(Script.name());

if (config.runsInWidget) {
  Script.setWidget(widget);
} else {
  const f = config.widgetFamily || "medium";
  if (f === "small") widget.presentSmall();
  else if (f === "large") widget.presentLarge();
  else if (f === "extraLarge") widget.presentExtraLarge();
  else widget.presentMedium();
}
Script.complete();
