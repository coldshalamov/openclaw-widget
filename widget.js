const CONFIG = {
  CONTENT_URL: "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/content/art-v2.json",
  UPDATE_INTERVAL: 900,
  WIDGET_SIZE: config.widgetFamily || "medium",
  CACHE_FILE: "ascii_art_cache.json",
  SHOW_META: false,
  FRAME_DURATION: 600,
  GLITCH_MODE: false,
  THEME_PREF: "dark"
};

const THEMES = {
  light: {
    bg: new Color("#0a0a0a"),
    fg: new Color("#00ff41"),
    accent: new Color("#00f5ff"),
    meta: new Color("#666666")
  },
  dark: {
    bg: new Color("#0a0a0a"),
    fg: new Color("#00ff41"),
    accent: new Color("#00f5ff"),
    meta: new Color("#888888")
  }
};

async function createWidget() {
  const widget = new ListWidget();
  const theme = THEMES.dark;
  widget.backgroundColor = theme.bg;

  const content = await fetchContent();
  const art = selectArtPiece(content);

  const mainStack = widget.addStack();
  mainStack.layoutVertically();
  mainStack.centerAlignContent();
  mainStack.setPadding(4, 6, 4, 6);

  var fontSize;
  if (CONFIG.WIDGET_SIZE === "small") fontSize = 5;
  else if (CONFIG.WIDGET_SIZE === "large") fontSize = 11;
  else fontSize = 8;

  var rawContent;
  if (art.type === "animated" && art.frames) {
    var fi = Math.floor(Date.now() / CONFIG.FRAME_DURATION) % art.frames.length;
    rawContent = art.frames[fi].content;
  } else {
    rawContent = art.content;
  }

  var lines = (rawContent || "").split("\n");
  for (var i = 0; i < lines.length; i++) {
    var t = mainStack.addText(lines[i]);
    t.font = Font.systemFont(fontSize, "monospaced");
    t.textColor = theme.fg;
    t.lineLimit = 1;
    t.minimumScaleFactor = 0.5;
  }

  widget.refreshAfterDate = new Date(Date.now() + CONFIG.UPDATE_INTERVAL * 1000);
  widget.url = "scriptable:///run?scriptName=" + Script.name();
  return widget;
}

async function fetchContent() {
  try {
    var req = new Request(CONFIG.CONTENT_URL);
    req.timeoutInterval = 10;
    var data = await req.loadJSON();
    var fm = FileManager.local();
    fm.writeString(fm.joinPath(fm.documentsDirectory(), CONFIG.CACHE_FILE), JSON.stringify(data));
    return data;
  } catch (e) {
    try {
      var fm = FileManager.local();
      var path = fm.joinPath(fm.documentsDirectory(), CONFIG.CACHE_FILE);
      if (fm.fileExists(path)) return JSON.parse(fm.readString(path));
    } catch (e2) {}
    return { art: [{ id: "fb", title: "Offline", theme: "retro", type: "static", content: "╔═══════════╗\n║ OFFLINE  ║\n╚═══════════╝" }] };
  }
}

function selectArtPiece(content) {
  var art = content.art || [];
  if (art.length === 0) return { title: "Empty", theme: "retro", content: "No art" };
  var idx = Math.floor(Math.random() * art.length);
  return art[idx];
}

var widget = await createWidget();
if (config.runsInWidget) {
  Script.setWidget(widget);
} else {
  widget.presentMedium();
}
Script.complete();
