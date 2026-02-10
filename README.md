# ASCII Art Streaming Widget for iOS

> A badass, cyberpunk-inspired ASCII art streaming widget for iOS Scriptable.
> **Live demo:** [Control Panel](https://coldshalamov.github.io/openclaw-widget/control-panel.html)

![Widget Preview](https://img.shields.io/badge/widget-v2.0.0-cyan?style=flat-square)
![iOS](https://img.shields.io/badge/iOS-14%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

## ✨ Features

- **Dynamic ASCII Art** - Static pieces and smooth animations
- **Multiple Themes** - Cyberpunk, Matrix, Retro, Nature, Glitch, Abstract
- **Smart Transitions** - Glitch effects, color cycling, easter eggs
- **Dark/Light Mode** - Automatically adapts to system theme
- **Tap to Refresh** - Interactive widget behavior
- **Web Control Panel** - Manage content remotely from any browser
- **Easter Eggs** - Hidden surprises that appear based on time/context

## 🚀 Quick Start

### 1. Install Scriptable
Download [Scriptable](https://apps.apple.com/us/app/scriptable/id1405459188) from the App Store (free).

### 2. Create the Widget
1. Open Scriptable
2. Tap **+** to create a new script
3. Name it "ASCII Art Widget"
4. Paste the contents of [`widget.js`](widget.js)
5. Tap **Done**

### 3. Add to Home Screen
1. Long press your home screen
2. Tap **+** (Add Widget)
3. Search for "Scriptable"
4. Choose your preferred size (Small, Medium, or Large)
5. Tap the widget to configure it
6. Select "ASCII Art Widget" as the script
7. Choose "When Interacting" for the action

### 4. Enjoy!
The widget will automatically fetch and display ASCII art from the cloud. Tap it to refresh or cycle to the next piece.

## 🎨 Available Themes

| Theme | Icon | Description |
|-------|------|-------------|
| **Cyberpunk** | 🌃 | Neon-lit cityscapes, hacking terminals, data streams |
| **Matrix** | 💊 | Digital rain, code aesthetics, green phosphor |
| **Retro** | 💾 | Vintage computers, loading screens, nostalgia |
| **Nature** | 🌿 | Digital forests, cosmic landscapes, organic code |
| **Glitch** | ⚡ | Corrupted data, malfunction robots, signal errors |
| **Abstract** | 🔮 | Sacred geometry, pulsing cores, cosmic entities |

## 🎛️ Web Control Panel

Access the control panel to manage your widget remotely:

👉 **[Open Control Panel](https://coldshalamov.github.io/openclaw-widget/control-panel.html)**

### Features:
- 🎭 Switch between themes
- 🖼️ Browse the art gallery
- 📋 Create custom playlists
- 💬 Send custom messages
- ⚡ Trigger specific pieces
- 📊 View system status

## 🛠️ Content Generator

The [`content-generator.py`](content-generator.py) script helps you create and manage content.

### Basic Usage

```bash
# Generate default content
python content-generator.py

# Add art from a text file
python content-generator.py --add-art myart.txt --title "My Art" --theme cyberpunk

# Add a quote
python content-generator.py --add-quote "Hello World" --theme retro

# List all art pieces
python content-generator.py --list

# Show statistics
python content-generator.py --stats

# Validate JSON
python content-generator.py --validate
```

### Adding Custom Art

Create a text file with your ASCII art:

```
╔══════════════════════╗
║    MY CUSTOM ART     ║
╠══════════════════════╣
║                      ║
║    ♦ ♦ ♦ ♦ ♦ ♦      ║
║    ♦  HELLO  ♦      ║
║    ♦ ♦ ♦ ♦ ♦ ♦      ║
║                      ║
╚══════════════════════╝
```

Then add it:
```bash
python content-generator.py --add-art myart.txt --title "Hello World" --theme abstract
```

### Creating Animated Art

For animated art, create multiple frame files:
```
frames/
  frame_1.txt
  frame_2.txt
  frame_3.txt
```

Then use the Python API:
```python
from content_generator import ContentGenerator

gen = ContentGenerator()
gen.load()
gen.create_animated_from_files(
    ["frames/frame_1.txt", "frames/frame_2.txt", "frames/frame_3.txt"],
    art_id="my-animation",
    title="My Animation",
    theme="cyberpunk",
    frame_duration=500
)
gen.save()
```

## 📁 Project Structure

```
openclaw-widget/
├── widget.js              # Main Scriptable widget code
├── control-panel.html     # Web control interface
├── content-generator.py   # Content management script
├── content/
│   └── art-v2.json       # Content database
└── README.md             # This file
```

## 🔧 Configuration

Edit the `CONFIG` object at the top of `widget.js` to customize:

```javascript
const CONFIG = {
  // Content URL (GitHub raw)
  CONTENT_URL: "https://raw.githubusercontent.com/coldshalamov/openclaw-widget/main/content/art-v2.json",
  
  // Update interval in seconds (minimum 900 = 15 minutes)
  UPDATE_INTERVAL: 900,
  
  // Show metadata footer
  SHOW_META: true,
  
  // Animation speed (milliseconds)
  FRAME_DURATION: 600,
  
  // Enable glitch effects
  GLITCH_MODE: true,
  
  // Theme: 'auto', 'light', 'dark'
  THEME_PREF: "auto"
};
```

## 🎭 Easter Eggs

The widget includes hidden surprises:

- **Rare messages** - Occasionally displays self-aware text
- **Time-based** - Special content for morning/night
- **Glitch mode** - Random visual corruptions (15% chance)
- **Secret quotes** - 20% chance to show a quote instead of art

## 📝 Content Format

The content JSON follows this structure:

```json
{
  "version": "2.0.0",
  "config": {
    "updateInterval": 900,
    "defaultTheme": "cyberpunk"
  },
  "themes": { ... },
  "art": [
    {
      "id": "unique-id",
      "title": "Art Title",
      "theme": "cyberpunk",
      "type": "static",
      "content": "ASCII art string"
    },
    {
      "id": "animated-id",
      "title": "Animated Art",
      "theme": "matrix",
      "type": "animated",
      "frames": [
        {"frame": 1, "content": "...", "duration": 500},
        {"frame": 2, "content": "...", "duration": 500}
      ]
    }
  ],
  "quotes": [...],
  "easterEggs": [...]
}
```

## 🎨 ASCII Art Tips

For best results with Scriptable widgets:

1. **Use monospace-friendly characters:**
   - Box drawing: `═║╔╗╚╝╠╣╦╩╬`
   - Blocks: `█▓▒░`
   - Arrows: `←→↑↓↔↕`
   - Unicode symbols: `★✦✧◉◯`

2. **Keep width appropriate:**
   - Small widgets: ~20-25 characters
   - Medium widgets: ~35-40 characters
   - Large widgets: ~50-60 characters

3. **Test your art:**
   ```bash
   cat myart.txt
   ```
   If it looks good in terminal, it'll look good in the widget!

## 🔒 Privacy

- The widget only fetches public JSON from GitHub
- No personal data is collected or transmitted
- All preferences are stored locally on your device

## 🤝 Contributing

Want to add your own ASCII art? 

1. Fork this repository
2. Add your art to `content/art-v2.json`
3. Submit a pull request

Please ensure your art:
- Is original or properly licensed
- Works well in both light and dark modes
- Uses appropriate Unicode characters
- Includes proper metadata

## 📜 License

MIT License - feel free to use, modify, and share!

## 🙏 Credits

Built with 💜 by OpenClaw

Special thanks to:
- [Scriptable](https://scriptable.app/) for the awesome iOS automation platform
- The ASCII art community for inspiration
- You, for using this widget!

---

**Pro tip:** Tap the widget repeatedly to cycle through different art pieces faster. The widget remembers where you left off!

*Remember: In a world of boring widgets, be the one that displays glitchy robots.* 🤖⚡