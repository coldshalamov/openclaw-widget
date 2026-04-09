const CONFIG = {
  CONTENT_URL: "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/content/art-v2.json",
  UPDATE_INTERVAL: 300,
  CACHE_FILE: "ascii_art_cache.json"
};

async function createWidget() {
  const widget = new ListWidget();
  widget.backgroundColor = new Color("#0a0a0a");
  widget.setPadding(0, 0, 0, 0);

  const content = await fetchContent();
  const art = selectArtPiece(content);

  const mainStack = widget.addStack();
  mainStack.layoutVertically();
  mainStack.centerAlignContent();
  mainStack.setPadding(0, 0, 0, 0);

  const size = config.widgetFamily || "medium";
  var fontSize;
  if (size === "small") fontSize = 6;
  else if (size === "large") fontSize = 13;
  else fontSize = 9;

  var raw = art.content;
  if (art.type === "animated" && art.frames) {
    var fi = Math.floor(Date.now() / 600) % art.frames.length;
    raw = art.frames[fi].content;
  }

  var lines = (raw || "").split("\n");
  for (var i = 0; i < lines.length; i++) {
    var t = mainStack.addText(lines[i]);
    t.font = Font.systemFont(fontSize, "monospaced");
    t.textColor = new Color("#00ff41");
    t.lineLimit = 1;
    t.minimumScaleFactor = 0.01;
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
      var p = fm.joinPath(fm.documentsDirectory(), CONFIG.CACHE_FILE);
      if (fm.fileExists(p)) return JSON.parse(fm.readString(p));
    } catch (e2) {}
    return { art: [{ content: "╔═══════════════╗\n║   OFFLINE    ║\n╚═══════════════╝" }] };
  }
}

function selectArtPiece(content) {
  var art = content.art || [];
  if (art.length === 0) return { content: "No art" };
  return art[Math.floor(Math.random() * art.length)];
}

var widget = await createWidget();
if (config.runsInWidget) Script.setWidget(widget);
else widget.presentMedium();
Script.complete();
