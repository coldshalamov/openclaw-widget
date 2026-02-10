// ═══════════════════════════════════════════════════════════════
// ASCII ART STREAMING WIDGET v2.0
// For iOS Scriptable - The Badass Edition
// ═══════════════════════════════════════════════════════════════
//
// Setup:
// 1. Install Scriptable app from App Store
// 2. Create new script, paste this code
// 3. Add widget to home screen (Small/Medium/Large)
// 4. Configure widget to run this script
// 5. Enjoy your digital art gallery
//
// ═══════════════════════════════════════════════════════════════

// ═══ Configuration ═══
const CONFIG = {
  // GitHub content URL (raw)
  CONTENT_URL: "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/content/art-v2.json",
  
  // Update interval in seconds (Scriptable limits: min 15 min background)
  UPDATE_INTERVAL: 900, // 15 minutes
  
  // Widget size detection
  WIDGET_SIZE: config.widgetFamily || "medium",
  
  // Local cache file
  CACHE_FILE: "ascii_art_cache.json",
  
  // Show metadata footer
  SHOW_META: true,
  
  // Animation frame timing (ms)
  FRAME_DURATION: 600,
  
  // Enable glitch effects
  GLITCH_MODE: true,
  
  // Theme preference: 'auto', 'light', 'dark'
  THEME_PREF: "auto"
};

// ═══ Color Schemes ═══
const THEMES = {
  light: {
    bg: new Color("#ffffff"),
    fg: new Color("#1a1a1a"),
    accent: new Color("#00f5ff"),
    secondary: new Color("#ff00ff"),
    meta: new Color("#666666")
  },
  dark: {
    bg: new Color("#0a0a0a"),
    fg: new Color("#00ff41"),
    accent: new Color("#00f5ff"),
    secondary: new Color("#ff00ff"),
    meta: new Color("#888888")
  },
  cyberpunk: {
    bg: new Color("#0d0221"),
    fg: new Color("#00f5ff"),
    accent: new Color("#ff00ff"),
    secondary: new Color("#ff3864"),
    meta: new Color("#7209b7")
  },
  matrix: {
    bg: new Color("#000000"),
    fg: new Color("#00ff41"),
    accent: new Color("#008F11"),
    secondary: new Color("#003B00"),
    meta: new Color("#00ff41")
  },
  retro: {
    bg: new Color("#1a1a2e"),
    fg: new Color("#4ecdc4"),
    accent: new Color("#ff6b6b"),
    secondary: new Color("#ffe66d"),
    meta: new Color("#95e1d3")
  }
};

// ═══ Main Widget Builder ═══
async function createWidget() {
  const widget = new ListWidget();
  
  // Set background
  const isDark = await isDarkMode();
  const theme = isDark ? THEMES.dark : THEMES.light;
  widget.backgroundColor = theme.bg;
  
  // Add gradient background for extra style
  const gradient = new LinearGradient();
  gradient.colors = [theme.bg, new Color(theme.bg.hex, 0.8)];
  gradient.locations = [0, 1];
  widget.backgroundGradient = gradient;
  
  // Fetch content
  const content = await fetchContent();
  
  // Select art piece
  const art = selectArtPiece(content);
  
  // Build content stack
  const mainStack = widget.addStack();
  mainStack.layoutVertically();
  mainStack.centerAlignContent();
  mainStack.setPadding(8, 12, 8, 12);
  
  // Render art
  await renderArt(mainStack, art, theme);
  
  // Add metadata footer
  if (CONFIG.SHOW_META) {
    mainStack.addSpacer(4);
    const metaStack = mainStack.addStack();
    metaStack.layoutHorizontally();
    
    const metaText = metaStack.addText(`${art.theme} · ${art.title}`);
    metaText.font = Font.systemFont(8);
    metaText.textColor = theme.meta;
    metaText.lineLimit = 1;
    
    metaStack.addSpacer();
    
    const refreshIcon = metaStack.addText("↻");
    refreshIcon.font = Font.systemFont(8);
    refreshIcon.textColor = theme.meta;
  }
  
  // Set refresh interval
  widget.refreshAfterDate = new Date(Date.now() + (CONFIG.UPDATE_INTERVAL * 1000));
  
  // Tap action
  widget.url = "scriptable:///run/ASCII%20Art%20Widget";
  
  return widget;
}

// ═══ Content Fetching ═══
async function fetchContent() {
  try {
    // Try to fetch fresh content
    const req = new Request(CONFIG.CONTENT_URL);
    req.timeoutInterval = 10;
    const data = await req.loadJSON();
    
    // Cache the content
    const cache = JSON.stringify(data);
    const fm = FileManager.local();
    const path = fm.joinPath(fm.documentsDirectory(), CONFIG.CACHE_FILE);
    fm.writeString(path, cache);
    
    return data;
  } catch (e) {
    // Fall back to cached content
    console.log("Fetch failed, using cache: " + e.message);
    return loadCachedContent();
  }
}

function loadCachedContent() {
  const fm = FileManager.local();
  const path = fm.joinPath(fm.documentsDirectory(), CONFIG.CACHE_FILE);
  
  if (fm.fileExists(path)) {
    const cache = fm.readString(path);
    return JSON.parse(cache);
  }
  
  // Return minimal fallback
  return getFallbackContent();
}

function getFallbackContent() {
  return {
    art: [{
      id: "fallback",
      title: "Offline Mode",
      theme: "retro",
      type: "static",
      content: "╔══════════════╗\n║  📡 OFFLINE  ║\n╠══════════════╣\n║              ║\n║  Cached art  ║\n║  will return ║\n║              ║\n╚══════════════╝"
    }],
    themes: {}
  };
}

// ═══ Art Selection ═══
function selectArtPiece(content) {
  const { art, quotes, easterEggs } = content;
  
  // Check for easter eggs (rare)
  if (easterEggs && Math.random() < 0.05) {
    const hour = new Date().getHours();
    const timeBased = easterEggs.filter(e => {
      if (e.trigger === "morning" && hour >= 6 && hour < 12) return true;
      if (e.trigger === "night" && hour >= 22) return true;
      if (e.trigger === "rare") return Math.random() < e.probability;
      return false;
    });
    
    if (timeBased.length > 0) {
      const egg = timeBased[Math.floor(Math.random() * timeBased.length)];
      return {
        id: egg.id,
        title: "Easter Egg",
        theme: "glitch",
        type: "static",
        content: egg.content,
        isEasterEgg: true
      };
    }
  }
  
  // Get current index from stored state
  const currentIndex = getState("artIndex") || 0;
  const nextIndex = (currentIndex + 1) % art.length;
  setState("artIndex", nextIndex);
  
  // Occasionally show a quote instead (20% chance)
  if (quotes && Math.random() < 0.2) {
    const quote = quotes[Math.floor(Math.random() * quotes.length)];
    return {
      id: quote.id,
      title: "Quote",
      theme: quote.theme,
      type: "static",
      content: formatQuote(quote),
      isQuote: true
    };
  }
  
  return art[currentIndex];
}

function formatQuote(quote) {
  const boxWidth = 32;
  const padding = " ";
  
  let result = `╔${"═".repeat(boxWidth)}╗\n`;
  result += `║${padding.repeat(boxWidth)}║\n`;
  
  const lines = quote.text.split("\n");
  for (const line of lines) {
    const padded = line.padStart((boxWidth + line.length) / 2).padEnd(boxWidth);
    result += `║${padded}║\n`;
  }
  
  result += `║${padding.repeat(boxWidth)}║\n`;
  const author = `— ${quote.author}`;
  const authorPadded = author.padStart((boxWidth + author.length) / 2).padEnd(boxWidth);
  result += `║${authorPadded}║\n`;
  result += `║${padding.repeat(boxWidth)}║\n`;
  result += `╚${"═".repeat(boxWidth)}╝`;
  
  return result;
}

// ═══ Art Rendering ═══
async function renderArt(stack, art, theme) {
  // Apply glitch effect randomly
  if (CONFIG.GLITCH_MODE && !art.isEasterEgg && Math.random() < 0.15) {
    await renderGlitchArt(stack, art, theme);
    return;
  }
  
  if (art.type === "animated" && art.frames) {
    // For widget, we pick one frame based on time
    const frameIndex = Math.floor(Date.now() / CONFIG.FRAME_DURATION) % art.frames.length;
    const frame = art.frames[frameIndex];
    renderTextBlock(stack, frame.content, theme);
  } else {
    renderTextBlock(stack, art.content, theme);
  }
}

function renderTextBlock(stack, content, theme) {
  const lines = content.split("\n");
  
  for (let i = 0; i < lines.length; i++) {
    const lineText = stack.addText(lines[i]);
    
    // Dynamic font sizing based on widget size
    const fontSize = getFontSize();
    lineText.font = Font.monospacedSystemFont(fontSize);
    
    // Color based on content patterns
    lineText.textColor = getLineColor(lines[i], theme);
    
    lineText.lineLimit = 1;
    lineText.minimumScaleFactor = 0.5;
    
    if (i < lines.length - 1) {
      // Minimal spacing for tight ASCII art
    }
  }
}

function getFontSize() {
  switch (CONFIG.WIDGET_SIZE) {
    case "small": return 7;
    case "large": return 10;
    default: return 8;
  }
}

function getLineColor(line, theme) {
  // Detect special characters and apply accent colors
  if (line.includes("█") || line.includes("▓") || line.includes("▒")) {
    return theme.accent;
  }
  if (line.includes("★") || line.includes("✦") || line.includes("✧")) {
    return theme.secondary;
  }
  if (line.includes("⚠") || line.includes("▲") || line.includes("▼")) {
    return new Color("#ff3864");
  }
  if (line.includes("✓") || line.includes("✔") || line.includes("✅")) {
    return new Color("#00ff41");
  }
  return theme.fg;
}

// ═══ Glitch Effect ═══
async function renderGlitchArt(stack, art, theme) {
  const content = art.type === "animated" 
    ? art.frames[0].content 
    : art.content;
  
  const glitched = applyGlitchEffect(content);
  renderTextBlock(stack, glitched, theme);
  
  // Add glitch indicator
  stack.addSpacer(2);
  const glitchText = stack.addText("⚡ SIGNAL DEGRADED ⚡");
  glitchText.font = Font.systemFont(6);
  glitchText.textColor = new Color("#ff3864");
  glitchText.centerAlignText();
}

function applyGlitchEffect(text) {
  const glitchChars = "▓▒░█▄▀▌▐═║╪Ø₣₦¶§¥£€¢∞§¶•ªº–≠œ∑´®†¥¨ˆøπ";
  const lines = text.split("\n");
  const result = [];
  
  for (const line of lines) {
    if (Math.random() < 0.3) {
      // Corrupt this line
      let corrupted = "";
      for (const char of line) {
        if (Math.random() < 0.15 && char !== " ") {
          corrupted += glitchChars[Math.floor(Math.random() * glitchChars.length)];
        } else {
          corrupted += char;
        }
      }
      result.push(corrupted);
    } else {
      result.push(line);
    }
  }
  
  return result.join("\n");
}

// ═══ Utility Functions ═══
async function isDarkMode() {
  if (CONFIG.THEME_PREF !== "auto") {
    return CONFIG.THEME_PREF === "dark";
  }
  
  // Check system appearance
  const app = Device;
  return Device.isUsingDarkAppearance();
}

function getState(key) {
  const fm = FileManager.local();
  const path = fm.joinPath(fm.documentsDirectory(), "widget_state.json");
  
  if (fm.fileExists(path)) {
    const data = JSON.parse(fm.readString(path));
    return data[key];
  }
  return null;
}

function setState(key, value) {
  const fm = FileManager.local();
  const path = fm.joinPath(fm.documentsDirectory(), "widget_state.json");
  
  let data = {};
  if (fm.fileExists(path)) {
    data = JSON.parse(fm.readString(path));
  }
  
  data[key] = value;
  fm.writeString(path, JSON.stringify(data));
}

// ═══ Run Widget ═══
async function run() {
  const widget = await createWidget();
  
  if (config.runsInWidget) {
    Script.setWidget(widget);
  } else {
    // Preview in app
    widget.presentMedium();
  }
  
  Script.complete();
}

// Execute
run();