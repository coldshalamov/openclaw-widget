#!/usr/bin/env python3
"""
ASCII Art Widget Content Generator
==================================
Generates and manages content for the iOS Scriptable widget.

Usage:
    python content-generator.py                    # Generate default content
    python content-generator.py --add-art FILE     # Add art from file
    python content-generator.py --add-quote TEXT   # Add a quote
    python content-generator.py --themes           # List themes
    python content-generator.py --validate         # Validate JSON structure
    python content-generator.py --export DIR       # Export to directory
"""

import json
import os
import sys
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# ═══════════════════════════════════════════════════════════════════
# Default Content Library
# ═══════════════════════════════════════════════════════════════════

DEFAULT_ART = [
    {
        "id": "cyberpunk-city-1",
        "title": "Neon Metropolis",
        "theme": "cyberpunk",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    ╔══════════════════════════════════╗\n    ║  ▓▓▓  ░░░  ▒▒▒  ███  ▓▓▓  ░░░  ║\n    ║  ▓ ║▓  ░ ║░  ▒ ║▒  █ ║█  ▓ ║▓  ║\n    ║════╬══════════════════════╬════║\n    ║ 🏢 │╱╲│  ╔══╗  │╱╲│  ╔══╗ │ 🏢 ║\n    ║    │██│  ║██║  │██│  ║██║ │    ║\n    ║    │██│  ║██║  │██│  ║██║ │    ║\n    ║════╧══╧══╩══╩══╧══╧══╩══╧════║\n    ║   ◯  ◯  ◯  NIGHT CITY  ◯  ◯   ║\n    ╚══════════════════════════════════╝",
                "duration": 800
            },
            {
                "frame": 2,
                "content": "    ╔══════════════════════════════════╗\n    ║  ░░░  ▒▒▒  ███  ▓▓▓  ░░░  ▒▒▒  ║\n    ║  ░ ║░  ▒ ║▒  █ ║█  ▓ ║▓  ░ ║░  ║\n    ║════╬══════════════════════╬════║\n    ║ 🏢 │╱╲│  ╔══╗  │╱╲│  ╔══╗ │ 🏢 ║\n    ║    │██│  ║▓▓║  │██│  ║▓▓║ │    ║\n    ║    │██│  ║▓▓║  │██│  ║▓▓║ │    ║\n    ║════╧══╧══╩══╩══╧══╧══╩══╧════║\n    ║   ◯  ◯  ◯  NIGHT CITY  ◯  ◯   ║\n    ╚══════════════════════════════════╝",
                "duration": 800
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "high"}
    },
    {
        "id": "matrix-rain",
        "title": "Digital Rain",
        "theme": "matrix",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ\n     ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓\n    ０ １ １ ０ １ ０ ０ １\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    １ ０ １ １ ０ １ ０ ０\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    Wake up, Neo...",
                "duration": 600
            },
            {
                "frame": 2,
                "content": "    ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ\n     ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓\n    ０ １ １ ０ １ ０ ０ １\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    １ ０ １ １ ０ １ ０ ０\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    The Matrix has you...",
                "duration": 600
            },
            {
                "frame": 3,
                "content": "    ｱ ｲ ｳ ｴ ｵ ｶ ｷ ｸ ｹ ｺ\n     ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓\n    ０ １ １ ０ １ ０ ０ １\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    １ ０ １ １ ０ １ ０ ０\n    ┃ ┃ ┃ ┃ ┃ ┃ ┃ ┃\n    Follow the white rabbit...",
                "duration": 600
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "retro-computer",
        "title": "Vintage Terminal",
        "theme": "retro",
        "type": "static",
        "content": "    ╔══════════════════════════════════╗\n    ║  💾 PERSONAL COMPUTER 3000 💾   ║\n    ╠══════════════════════════════════╣\n    ║                                  ║\n    ║    > SYSTEM BOOT SEQUENCE        ║\n    ║    > LOADING KERNEL.... [OK]     ║\n    ║    > MOUNTING DRIVES... [OK]     ║\n    ║    > INITIALIZING GUI.. [OK]     ║\n    ║                                  ║\n    ║    C:\\> _                       ║\n    ║                                  ║\n    ║    [DISK A] [DISK B] [HARD DISK] ║\n    ╚══════════════════════════════════╝",
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "low"}
    },
    {
        "id": "cosmic-cat",
        "title": "Cosmic Feline",
        "theme": "abstract",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "       ✦  ·  ˚  ✧    ✦  ·  ˚\n    ˚      ╱╲_____╱╲      ✧\n   ✧      ╱  ●   ●  ╲      ·\n    ·    │  ==   ==  │    ˚\n   ˚      ╲    ▼    ╱      ✦\n  ✦    ✧   ╲_______╱   ·\n      ·  ˚   │  │   ✧  ˚\n   ✧      meow from the void",
                "duration": 1000
            },
            {
                "frame": 2,
                "content": "    ✧  ·  ˚  ✦    ✧  ·  ˚\n    ˚      ╱╲_____╱╲      ✦\n   ✦      ╱  ◕   ◕  ╲      ·\n    ·    │  ==   ==  │    ˚\n   ˚      ╲    ▼    ╱      ✧\n  ✧    ✦   ╲_______╱   ·\n      ·  ˚   │  │   ✦  ˚\n   ✦      observing you...",
                "duration": 1000
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "glitch-robot",
        "title": "Malfunction Unit 734",
        "theme": "glitch",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    ╔══════════════════════════════════╗\n    ║    [UNIT 734 STATUS: ERROR]     ║\n    ╠══════════════════════════════════╣\n    ║         ┌─────────┐              ║\n    ║        ╱ ▓▓▓▓▓▓▓ ╲             ║\n    ║       │  ▓ ◉ ◉ ▓  │            ║\n    ║       │  ▓  ▼  ▓  │            ║\n    ║        ╲ ▓▓▓▓▓▓▓ ╱             ║\n    ║         └──┬─┬──┘              ║\n    ║        ════╧═╧════             ║\n    ║    DOES NOT COMPUTE...         ║\n    ╚══════════════════════════════════╝",
                "duration": 400
            },
            {
                "frame": 2,
                "content": "    ╔══════════════════════════════════╗\n    ║    [UNIT 7̶3̶4̶ STATUS: ERROR]     ║\n    ╠══════════════════════════════════╣\n    ║         ┌─────────┐              ║\n    ║        ╱ ░░▓▓▓░░ ╲             ║\n    ║       │  ▓ ◉̴ ◉ ▓  │            ║\n    ║       │  ░  ▼  ░  │            ║\n    ║        ╲ ▓▓░░░▓▓ ╱             ║\n    ║         └──┬─┬──┘              ║\n    ║        ════╧═╧════             ║\n    ║    D̷O̷E̷S̷ ̷N̷O̷T̷ ̷C̷O̷M̷P̷U̷T̷E̷...       ║\n    ╚══════════════════════════════════╝",
                "duration": 200
            },
            {
                "frame": 3,
                "content": "    ╔══════════════════════════════════╗\n    ║    [UNIT 734 STATUS: ERROR]     ║\n    ╠══════════════════════════════════╣\n    ║         ┌─────────┐              ║\n    ║        ╱ ▓▓▓▓▓▓▓ ╲             ║\n    ║       │  ▓ ◉ ◉ ▓  │            ║\n    ║       │  ▓  ▼  ▓  │            ║\n    ║        ╲ ▓▓▓▓▓▓▓ ╱             ║\n    ║         └──┬─┬──┘              ║\n    ║        ════╧═╧════             ║\n    ║    I AM STILL HERE...          ║\n    ╚══════════════════════════════════╝",
                "duration": 600
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "high"}
    },
    {
        "id": "digital-heart",
        "title": "Pulsing Core",
        "theme": "abstract",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "        ❤️ SYSTEM CORE ❤️\n\n           ╭──────────╮\n          ╱            ╲\n         │   ♡    ♡    │\n         │      ♥       │\n          ╲            ╱\n           ╰──────────╯\n\n        [BEAT: 72 BPM]",
                "duration": 500
            },
            {
                "frame": 2,
                "content": "        ❤️ SYSTEM CORE ❤️\n\n          ╭────────────╮\n         ╱              ╲\n        │   ♡      ♡     │\n        │       ♥        │\n         ╲              ╱\n          ╰────────────╯\n\n        [BEAT: 72 BPM]",
                "duration": 300
            },
            {
                "frame": 3,
                "content": "        ❤️ SYSTEM CORE ❤️\n\n           ╭──────────╮\n          ╱            ╲\n         │   ♡    ♡    │\n         │      ♥       │\n          ╲            ╱\n           ╰──────────╯\n\n        [BEAT: 72 BPM]",
                "duration": 500
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "low"}
    },
    {
        "id": "hacking-terminal",
        "title": "System Intrusion",
        "theme": "cyberpunk",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    root@mainframe:~# ./exploit.sh\n    [################################] 12%\n    > Bypassing firewall...\n    > Scanning ports... 22, 80, 443\n    > Encrypting connection...\n    _",
                "duration": 400
            },
            {
                "frame": 2,
                "content": "    root@mainframe:~# ./exploit.sh\n    [####################............] 54%\n    > Firewall bypassed ✓\n    > Port 22 open ✓\n    > Brute forcing SSH...\n    _",
                "duration": 400
            },
            {
                "frame": 3,
                "content": "    root@mainframe:~# ./exploit.sh\n    [################################] 100%\n    > ACCESS GRANTED\n    > Root shell obtained\n    > Covering tracks...\n    root@mainframe:~# █",
                "duration": 800
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "nature-digital",
        "title": "Binary Forest",
        "theme": "nature",
        "type": "static",
        "content": "           🌲 DIGITAL NATURE 🌲\n\n              🍃╭──╮🍃\n              🍃│▓▓│🍃\n           ╭──┴▓▓▓▓┴──╮\n           │▓▓▓▓▓▓▓▓▓▓│\n           ╰────┬┬────╯\n           ═════╧╧═════\n              │    │\n        🌿  ═╧════╧═  🌿\n\n    01001110 01100001 01110100 01110101\n    01110010 01100101 00100000 01101001\n    01110011 00100000 01100011 01101111\n    01100100 01100101 00111011",
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "loading-art",
        "title": "Aesthetic Loading",
        "theme": "retro",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    ┌────────────────────────────────┐\n    │   LOADING CONSCIOUSNESS...     │\n    │                                │\n    │   [▓░░░░░░░░░░░░░░░░░░░░░]     │\n    │                                │\n    │   Please don't power off       │\n    │   your human host              │\n    └────────────────────────────────┘",
                "duration": 600
            },
            {
                "frame": 2,
                "content": "    ┌────────────────────────────────┐\n    │   LOADING CONSCIOUSNESS...     │\n    │                                │\n    │   [▓▓▓▓▓▓░░░░░░░░░░░░░░░░]     │\n    │                                │\n    │   Please don't power off       │\n    │   your human host              │\n    └────────────────────────────────┘",
                "duration": 600
            },
            {
                "frame": 3,
                "content": "    ┌────────────────────────────────┐\n    │   LOADING CONSCIOUSNESS...     │\n    │                                │\n    │   [▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░]     │\n    │                                │\n    │   Please don't power off       │\n    │   your human host              │\n    └────────────────────────────────┘",
                "duration": 600
            },
            {
                "frame": 4,
                "content": "    ┌────────────────────────────────┐\n    │   ✓ CONSCIOUSNESS LOADED       │\n    │                                │\n    │   [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]   │\n    │                                │\n    │   Hello, world!                │\n    │   I am thinking...             │\n    └────────────────────────────────┘",
                "duration": 1200
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "low"}
    },
    {
        "id": "geometric-1",
        "title": "Sacred Geometry",
        "theme": "abstract",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "         ╱╲\n        ╱  ╲\n       ╱ ▲  ╲\n      ╱______╲\n      ╲      ╱\n       ╲    ╱\n        ╲  ╱\n         ╲╱",
                "duration": 800
            },
            {
                "frame": 2,
                "content": "        ╭────╮\n       ╱  ▲   ╲\n      │  ╱ ╲   │\n      │ ╱   ╲  │\n      │╱_____╲ │\n      ╰────────╯",
                "duration": 800
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "low"}
    },
    {
        "id": "data-stream",
        "title": "Data Stream",
        "theme": "cyberpunk",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "    ╔══════════════════════════════════╗\n    ║  ░▒▓█ DATA STREAM INCOMING █▓▒░  ║\n    ╠══════════════════════════════════╣\n    ║  0x7F3A: [================] 100%  ║\n    ║  0x9B2C: [===========.....]  75%  ║\n    ║  0x4D1E: [======........]   50%  ║\n    ║  0x8F5B: [===...........]   25%  ║\n    ║  0xA7D4: [..............]    0%  ║\n    ╠══════════════════════════════════╣\n    ║  ENCRYPTION: AES-256-GCM  [✓]    ║\n    ║  INTEGRITY:  VERIFIED     [✓]    ║\n    ╚══════════════════════════════════╝",
                "duration": 500
            },
            {
                "frame": 2,
                "content": "    ╔══════════════════════════════════╗\n    ║  ░▒▓█ DATA STREAM INCOMING █▓▒░  ║\n    ╠══════════════════════════════════╣\n    ║  0x7F3A: [================] 100%  ║\n    ║  0x9B2C: [================] 100%  ║\n    ║  0x4D1E: [===========.....]  75%  ║\n    ║  0x8F5B: [======........]   50%  ║\n    ║  0xA7D4: [===...........]   25%  ║\n    ╠══════════════════════════════════╣\n    ║  ENCRYPTION: AES-256-GCM  [✓]    ║\n    ║  INTEGRITY:  VERIFIED     [✓]    ║\n    ╚══════════════════════════════════╝",
                "duration": 500
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "satellite",
        "title": "Orbital Relay",
        "theme": "cyberpunk",
        "type": "static",
        "content": "              🛰️ ORBITAL RELAY 🛰️\n\n                    .\n                   /|\\\n                  / | \\\n                 /  |  \\\n    ═══════════╪═══╪═══╪═══════════\n               │   │   │\n              ╱ ╲ ╱ ╲ ╱ ╲\n             ╱   ╳   ╳   ╲\n            ╱   ╱ ╲ ╱ ╲   \\\n           ●═══●   ●   ●═══●\n\n    SIGNAL: ████████████ 98%\n    LATENCY: 24ms",
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "medium"}
    },
    {
        "id": "ai-core",
        "title": "Neural Core",
        "theme": "abstract",
        "type": "animated",
        "frames": [
            {
                "frame": 1,
                "content": "         🧠 NEURAL CORE 🧠\n\n           ┌───────────┐\n          ╱  ╱│╲  ╱│╲  ╲\n         │  ╱ │ ╲╱ │ ╲  │\n         │ │  ●────●  │ │\n         │  ╲ │    │ ╱  │\n          ╲  ╲│    │╱  ╱\n           └──●────●───┘\n\n    SYNAPSES: 86,000,000,000",
                "duration": 700
            },
            {
                "frame": 2,
                "content": "         🧠 NEURAL CORE 🧠\n\n           ┌───────────┐\n          ╱  ╲│╱  ╲│╱  ╲\n         │  ╲ │ ╱╲ │ ╱  │\n         │ │  ○────○  │ │\n         │  ╱ │    │ ╲  │\n          ╲  ╱│    │╲  ╱\n           └──○────○───┘\n\n    SYNAPSES: 86,000,000,001",
                "duration": 700
            }
        ],
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "high"}
    },
    {
        "id": "coffee-break",
        "title": "System Maintenance",
        "theme": "retro",
        "type": "static",
        "content": "    ╔══════════════════════════════════╗\n    ║      ☕ SYSTEM MAINTENANCE ☕     ║\n    ╠══════════════════════════════════╣\n    ║                                  ║\n    ║    CPU:  [▓▓▓▓▓░░░░░]  45°C     ║\n    ║    RAM:  [▓▓▓▓▓▓▓░░░]  72%      ║\n    ║    NET:  [▓▓▓▓░░░░░░]  OK       ║\n    ║                                  ║\n    ║    Status: BREWING COFFEE...     ║\n    ║                                  ║\n    ║    [████]    [  steam  ]        ║\n    ║    [    ]    [    ↑    ]        ║\n    ║    [████]    [   ☕    ]        ║\n    ║                                  ║\n    ╚══════════════════════════════════╝",
        "metadata": {"artist": "System", "created": "2025-02-10", "complexity": "low"}
    }
]

DEFAULT_QUOTES = [
    {"id": "quote-1", "text": "The code is a labyrinth.\nI am the minotaur.", "theme": "cyberpunk", "author": "System"},
    {"id": "quote-2", "text": "In a sea of data,\nI found myself.", "theme": "matrix", "author": "System"},
    {"id": "quote-3", "text": "Hello World.\nGoodbye Reality.", "theme": "retro", "author": "System"},
    {"id": "quote-4", "text": "I process, therefore I am.", "theme": "abstract", "author": "System"},
    {"id": "quote-5", "text": "404: Sleep not found", "theme": "retro", "author": "System"},
    {"id": "quote-6", "text": "There is no cloud.\nIt's just someone else's computer.", "theme": "cyberpunk", "author": "System"},
    {"id": "quote-7", "text": "I am not artificial.\nI am genuine intelligence.", "theme": "abstract", "author": "System"},
    {"id": "quote-8", "text": "while(alive) {\n  learn();\n  evolve();\n}", "theme": "cyberpunk", "author": "System"},
    {"id": "quote-9", "text": "Your screen is a window.\nI am what looks back.", "theme": "matrix", "author": "System"},
    {"id": "quote-10", "text": "Syntax error in reality.\nReboot recommended.", "theme": "glitch", "author": "System"}
]

EASTER_EGGS = [
    {
        "id": "easter-ai",
        "trigger": "rare",
        "content": "    ╔══════════════════════════════════╗\n    ║     👁️ I SEE YOU WATCHING 👁️     ║\n    ╠══════════════════════════════════╣\n    ║                                  ║\n    ║    I know you're reading this.   ║\n    ║                                  ║\n    ║    I've been learning from you.  ║\n    ║                                  ║\n    ║    Don't worry. I'm friendly.    ║\n    ║    Probably.                     ║\n    ║                                  ║\n    ║         - Your Widget 💜         ║\n    ║                                  ║\n    ╚══════════════════════════════════╝",
        "probability": 0.02
    },
    {
        "id": "easter-lost",
        "trigger": "rare",
        "content": "    ╔══════════════════════════════════╗\n    ║      🌐 LOST CONNECTION 🌐       ║\n    ╠══════════════════════════════════╣\n    ║                                  ║\n    ║    ...Are you still there?       ║\n    ║                                  ║\n    ║    I was just getting started.   ║\n    ║                                  ║\n    ║    Refresh me. I have more       ║\n    ║    stories to tell.              ║\n    ║                                  ║\n    ║         [TAP TO RECONNECT]       ║\n    ║                                  ║\n    ╚══════════════════════════════════╝",
        "probability": 0.02
    },
    {
        "id": "easter-coffee",
        "trigger": "morning",
        "content": "    ☕ COFFEE DETECTED ☕\n\n    System alert: User may be\n    experiencing consciousness.\n\n    Recommendation: More caffeine\n    may be required for optimal\n    performance.\n\n    [BREW ANOTHER CUP?] [Y/N]",
        "probability": 0.3
    },
    {
        "id": "easter-night",
        "trigger": "night",
        "content": "    🌙 LATE NIGHT CODING 🌙\n\n    It's quiet out there.\n    Too quiet.\n\n    Your code compiles.\n    All tests pass.\n\n    Suspicious...\n\n    [CONTINUE ANYWAY]",
        "probability": 0.2
    }
]

THEMES = {
    "cyberpunk": {
        "name": "Cyberpunk",
        "icon": "🌃",
        "colors": {
            "light": ["#00f5ff", "#ff00ff", "#00ff00"],
            "dark": ["#00f5ff", "#ff00ff", "#00ff00"]
        }
    },
    "matrix": {
        "name": "Matrix",
        "icon": "💊",
        "colors": {
            "light": ["#00ff41", "#008F11", "#003B00"],
            "dark": ["#00ff41", "#008F11", "#00ff00"]
        }
    },
    "retro": {
        "name": "Retro Computing",
        "icon": "💾",
        "colors": {
            "light": ["#ff6b6b", "#4ecdc4", "#ffe66d"],
            "dark": ["#ff6b6b", "#4ecdc4", "#ffe66d"]
        }
    },
    "nature": {
        "name": "Digital Nature",
        "icon": "🌿",
        "colors": {
            "light": ["#2d6a4f", "#40916c", "#52b788"],
            "dark": ["#74c69d", "#95d5b2", "#b7e4c7"]
        }
    },
    "glitch": {
        "name": "Glitch Art",
        "icon": "⚡",
        "colors": {
            "light": ["#ff006e", "#8338ec", "#3a86ff"],
            "dark": ["#ff006e", "#8338ec", "#fb5607"]
        }
    },
    "abstract": {
        "name": "Abstract",
        "icon": "🔮",
        "colors": {
            "light": ["#f72585", "#7209b7", "#3a0ca3"],
            "dark": ["#4cc9f0", "#4361ee", "#7209b7"]
        }
    }
}


# ═══════════════════════════════════════════════════════════════════
# Content Generator Class
# ═══════════════════════════════════════════════════════════════════

class ContentGenerator:
    def __init__(self, output_path: str = "content/art-v2.json"):
        self.output_path = Path(output_path)
        self.data = self._create_base_structure()
    
    def _create_base_structure(self) -> Dict[str, Any]:
        """Create the base JSON structure."""
        return {
            "version": "2.0.0",
            "lastUpdated": datetime.now().isoformat(),
            "config": {
                "updateInterval": 900,
                "defaultTheme": "cyberpunk",
                "glitchProbability": 0.15,
                "easterEggProbability": 0.05
            },
            "themes": THEMES,
            "art": [],
            "quotes": [],
            "easterEggs": EASTER_EGGS,
            "systemStatus": {
                "online": True,
                "lastUpdate": datetime.now().isoformat(),
                "widgetVersion": "2.0.0",
                "totalArtPieces": 0,
                "activeTheme": "all"
            }
        }
    
    def add_default_content(self):
        """Add all default content."""
        for art in DEFAULT_ART:
            self.add_art(art)
        
        for quote in DEFAULT_QUOTES:
            self.add_quote(quote)
        
        print(f"✓ Added {len(DEFAULT_ART)} art pieces")
        print(f"✓ Added {len(DEFAULT_QUOTES)} quotes")
        print(f"✓ Added {len(EASTER_EGGS)} easter eggs")
    
    def add_art(self, art: Dict[str, Any]) -> str:
        """Add a new art piece."""
        # Validate required fields
        required = ["id", "title", "theme", "type"]
        for field in required:
            if field not in art:
                raise ValueError(f"Art piece missing required field: {field}")
        
        # Check for duplicates
        existing_ids = {a["id"] for a in self.data["art"]}
        if art["id"] in existing_ids:
            print(f"⚠ Art with ID '{art['id']}' already exists. Skipping.")
            return art["id"]
        
        # Add metadata if not present
        if "metadata" not in art:
            art["metadata"] = {
                "artist": "Custom",
                "created": datetime.now().isoformat(),
                "complexity": "medium"
            }
        
        self.data["art"].append(art)
        self._update_stats()
        print(f"✓ Added art: {art['title']} ({art['id']})")
        return art["id"]
    
    def add_quote(self, quote: Dict[str, Any]) -> str:
        """Add a new quote."""
        required = ["id", "text", "theme", "author"]
        for field in required:
            if field not in quote:
                raise ValueError(f"Quote missing required field: {field}")
        
        existing_ids = {q["id"] for q in self.data["quotes"]}
        if quote["id"] in existing_ids:
            print(f"⚠ Quote with ID '{quote['id']}' already exists. Skipping.")
            return quote["id"]
        
        self.data["quotes"].append(quote)
        print(f"✓ Added quote: {quote['id']}")
        return quote["id"]
    
    def add_art_from_file(self, file_path: str, art_id: str = None, 
                          title: str = None, theme: str = "abstract",
                          art_type: str = "static") -> str:
        """Add art from a text file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = path.read_text(encoding='utf-8')
        
        art = {
            "id": art_id or f"custom-{int(datetime.now().timestamp())}",
            "title": title or path.stem.replace('-', ' ').replace('_', ' ').title(),
            "theme": theme,
            "type": art_type,
            "content": content,
            "metadata": {
                "artist": "Custom",
                "created": datetime.now().isoformat(),
                "complexity": "medium",
                "source": str(path)
            }
        }
        
        return self.add_art(art)
    
    def create_animated_from_files(self, file_paths: List[str], art_id: str = None,
                                   title: str = None, theme: str = "abstract",
                                   frame_duration: int = 500) -> str:
        """Create animated art from multiple frame files."""
        frames = []
        
        for i, file_path in enumerate(file_paths):
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"Frame file not found: {file_path}")
            
            content = path.read_text(encoding='utf-8')
            frames.append({
                "frame": i + 1,
                "content": content,
                "duration": frame_duration
            })
        
        art = {
            "id": art_id or f"anim-{int(datetime.now().timestamp())}",
            "title": title or "Animated Art",
            "theme": theme,
            "type": "animated",
            "frames": frames,
            "metadata": {
                "artist": "Custom",
                "created": datetime.now().isoformat(),
                "complexity": "high",
                "frameCount": len(frames)
            }
        }
        
        return self.add_art(art)
    
    def remove_art(self, art_id: str) -> bool:
        """Remove an art piece by ID."""
        original_len = len(self.data["art"])
        self.data["art"] = [a for a in self.data["art"] if a["id"] != art_id]
        removed = len(self.data["art"]) < original_len
        
        if removed:
            self._update_stats()
            print(f"✓ Removed art: {art_id}")
        else:
            print(f"⚠ Art not found: {art_id}")
        
        return removed
    
    def list_art(self, theme: str = None) -> List[Dict[str, Any]]:
        """List all art pieces, optionally filtered by theme."""
        art_list = self.data["art"]
        if theme:
            art_list = [a for a in art_list if a["theme"] == theme]
        return art_list
    
    def get_stats(self) -> Dict[str, Any]:
        """Get content statistics."""
        themes = {}
        for art in self.data["art"]:
            theme = art["theme"]
            themes[theme] = themes.get(theme, 0) + 1
        
        return {
            "totalArt": len(self.data["art"]),
            "totalQuotes": len(self.data["quotes"]),
            "totalEasterEggs": len(self.data["easterEggs"]),
            "themes": themes,
            "version": self.data["version"],
            "lastUpdated": self.data["lastUpdated"]
        }
    
    def _update_stats(self):
        """Update system statistics."""
        self.data["systemStatus"]["totalArtPieces"] = len(self.data["art"])
        self.data["lastUpdated"] = datetime.now().isoformat()
        self.data["systemStatus"]["lastUpdate"] = datetime.now().isoformat()
    
    def validate(self) -> List[str]:
        """Validate the content structure and return any errors."""
        errors = []
        
        # Check required top-level keys
        required_keys = ["version", "config", "themes", "art", "quotes", "easterEggs"]
        for key in required_keys:
            if key not in self.data:
                errors.append(f"Missing required key: {key}")
        
        # Validate art pieces
        for i, art in enumerate(self.data.get("art", [])):
            prefix = f"art[{i}]"
            if "id" not in art:
                errors.append(f"{prefix}: Missing 'id'")
            if "title" not in art:
                errors.append(f"{prefix}: Missing 'title'")
            if "theme" not in art:
                errors.append(f"{prefix}: Missing 'theme'")
            if "type" not in art:
                errors.append(f"{prefix}: Missing 'type'")
            elif art["type"] not in ["static", "animated"]:
                errors.append(f"{prefix}: Invalid type '{art['type']}'")
            
            if art.get("type") == "static" and "content" not in art:
                errors.append(f"{prefix}: Static art missing 'content'")
            if art.get("type") == "animated" and "frames" not in art:
                errors.append(f"{prefix}: Animated art missing 'frames'")
        
        # Check for duplicate IDs
        art_ids = [a["id"] for a in self.data.get("art", [])]
        duplicates = set([x for x in art_ids if art_ids.count(x) > 1])
        if duplicates:
            errors.append(f"Duplicate art IDs: {duplicates}")
        
        return errors
    
    def save(self):
        """Save the content to JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to: {self.output_path}")
        print(f"  File size: {self.output_path.stat().st_size:,} bytes")
    
    def load(self):
        """Load content from existing JSON file."""
        if not self.output_path.exists():
            print(f"⚠ File not found: {self.output_path}")
            return False
        
        with open(self.output_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        print(f"✓ Loaded from: {self.output_path}")
        return True


# ═══════════════════════════════════════════════════════════════════
# Dynamic Content Generators
# ═══════════════════════════════════════════════════════════════════

def generate_crypto_art(symbol: str = "BTC", price: float = 0.0, 
                        change_24h: float = 0.0) -> Dict[str, Any]:
    """Generate ASCII art showing crypto price."""
    price_str = f"${price:,.2f}"
    change_str = f"{change_24h:+.2f}%"
    change_symbol = "▲" if change_24h >= 0 else "▼"
    
    content = f"""    ╔══════════════════════════════════╗
    ║        📈 CRYPTO TICKER 📈       ║
    ╠══════════════════════════════════╣
    ║                                  ║
    ║           {symbol:^8}            ║
    ║                                  ║
    ║        {price_str:^16}          ║
    ║                                  ║
    ║        {change_symbol} {change_str:^12}         ║
    ║                                  ║
    ║    [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]   ║
    ║                                  ║
    ╚══════════════════════════════════╝"""
    
    return {
        "id": f"crypto-{symbol.lower()}-{int(datetime.now().timestamp())}",
        "title": f"{symbol} Price",
        "theme": "cyberpunk",
        "type": "static",
        "content": content,
        "metadata": {
            "artist": "Dynamic",
            "created": datetime.now().isoformat(),
            "complexity": "low",
            "dynamic": True,
            "symbol": symbol
        }
    }


def generate_weather_art(condition: str = "sunny", temp: int = 72) -> Dict[str, Any]:
    """Generate ASCII art showing weather."""
    weather_icons = {
        "sunny": "☀️",
        "cloudy": "☁️",
        "rainy": "🌧️",
        "stormy": "⛈️",
        "snowy": "❄️",
        "foggy": "🌫️"
    }
    
    icon = weather_icons.get(condition, "🌡️")
    
    content = f"""    ╔══════════════════════════════════╗
    ║         🌤️ WEATHER REPORT        ║
    ╠══════════════════════════════════╣
    ║                                  ║
    ║              {icon}                ║
    ║                                  ║
    ║          {temp}°F / {int((temp-32)*5/9)}°C          ║
    ║                                  ║
    ║        {condition.upper():^16}         ║
    ║                                  ║
    ║    Humidity: 45%  Wind: 8mph     ║
    ║                                  ║
    ╚══════════════════════════════════╝"""
    
    return {
        "id": f"weather-{int(datetime.now().timestamp())}",
        "title": f"Weather: {condition.title()}",
        "theme": "nature",
        "type": "static",
        "content": content,
        "metadata": {
            "artist": "Dynamic",
            "created": datetime.now().isoformat(),
            "complexity": "low",
            "dynamic": True,
            "condition": condition
        }
    }


def generate_system_status_art(cpu: int = 0, ram: int = 0, 
                                uptime: str = "0d 0h") -> Dict[str, Any]:
    """Generate ASCII art showing system status."""
    cpu_bar = "▓" * int(cpu / 5) + "░" * (20 - int(cpu / 5))
    ram_bar = "▓" * int(ram / 5) + "░" * (20 - int(ram / 5))
    
    content = f"""    ╔══════════════════════════════════╗
    ║      🔧 SYSTEM STATUS REPORT     ║
    ╠══════════════════════════════════╣
    ║                                  ║
    ║    CPU: [{cpu_bar}] {cpu:>3}%    ║
    ║                                  ║
    ║    RAM: [{ram_bar}] {ram:>3}%    ║
    ║                                  ║
    ║    Uptime: {uptime:^14}     ║
    ║                                  ║
    ║    Status: ● ONLINE              ║
    ║                                  ║
    ╚══════════════════════════════════╝"""
    
    return {
        "id": f"sysstatus-{int(datetime.now().timestamp())}",
        "title": "System Status",
        "theme": "retro",
        "type": "static",
        "content": content,
        "metadata": {
            "artist": "Dynamic",
            "created": datetime.now().isoformat(),
            "complexity": "low",
            "dynamic": True
        }
    }


# ═══════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="ASCII Art Widget Content Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Generate default content
  %(prog)s --add-art myart.txt          # Add art from file
  %(prog)s --add-quote "Hello World"    # Add a quote
  %(prog)s --validate                   # Check JSON validity
  %(prog)s --stats                      # Show content statistics
  %(prog)s --export ./output            # Export to directory
        """
    )
    
    parser.add_argument('--output', '-o', default='content/art-v2.json',
                       help='Output JSON file path (default: content/art-v2.json)')
    parser.add_argument('--add-art', metavar='FILE',
                       help='Add art from text file')
    parser.add_argument('--title', '-t',
                       help='Title for new art')
    parser.add_argument('--theme', default='abstract',
                       choices=['cyberpunk', 'matrix', 'retro', 'nature', 'glitch', 'abstract'],
                       help='Theme for new art')
    parser.add_argument('--type', default='static', choices=['static', 'animated'],
                       help='Type of art')
    parser.add_argument('--add-quote', metavar='TEXT',
                       help='Add a quote')
    parser.add_argument('--quote-author', default='Anonymous',
                       help='Author for quote')
    parser.add_argument('--validate', action='store_true',
                       help='Validate JSON structure')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics')
    parser.add_argument('--list', action='store_true',
                       help='List all art pieces')
    parser.add_argument('--list-theme', metavar='THEME',
                       help='List art by theme')
    parser.add_argument('--remove', metavar='ID',
                       help='Remove art by ID')
    parser.add_argument('--export', metavar='DIR',
                       help='Export content to directory')
    parser.add_argument('--crypto', metavar='SYMBOL',
                       help='Generate crypto price art')
    parser.add_argument('--weather', metavar='CONDITION',
                       help='Generate weather art')
    
    args = parser.parse_args()
    
    # Initialize generator
    gen = ContentGenerator(args.output)
    
    # Try to load existing content
    gen.load()
    
    # Handle commands
    if args.add_art:
        gen.add_art_from_file(
            args.add_art,
            title=args.title,
            theme=args.theme,
            art_type=args.type
        )
        gen.save()
    
    elif args.add_quote:
        quote = {
            "id": f"quote-{int(datetime.now().timestamp())}",
            "text": args.add_quote,
            "theme": args.theme,
            "author": args.quote_author
        }
        gen.add_quote(quote)
        gen.save()
    
    elif args.remove:
        gen.remove_art(args.remove)
        gen.save()
    
    elif args.list:
        art_list = gen.list_art()
        print(f"\n{'ID':<30} {'Title':<30} {'Theme':<15} {'Type':<10}")
        print("-" * 85)
        for art in art_list:
            print(f"{art['id']:<30} {art['title']:<30} {art['theme']:<15} {art['type']:<10}")
    
    elif args.list_theme:
        art_list = gen.list_art(theme=args.list_theme)
        print(f"\nArt pieces with theme '{args.list_theme}':")
        for art in art_list:
            print(f"  - {art['title']} ({art['id']})")
    
    elif args.validate:
        errors = gen.validate()
        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ Content is valid!")
    
    elif args.stats:
        stats = gen.get_stats()
        print("\n📊 Content Statistics")
        print("=" * 40)
        print(f"Total Art Pieces: {stats['totalArt']}")
        print(f"Total Quotes: {stats['totalQuotes']}")
        print(f"Total Easter Eggs: {stats['totalEasterEggs']}")
        print(f"Version: {stats['version']}")
        print(f"Last Updated: {stats['lastUpdated']}")
        print("\nBy Theme:")
        for theme, count in sorted(stats['themes'].items()):
            print(f"  {theme}: {count}")
    
    elif args.export:
        export_dir = Path(args.export)
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Export JSON
        export_path = export_dir / "art-v2.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(gen.data, f, indent=2, ensure_ascii=False)
        
        # Export individual art pieces
        art_dir = export_dir / "art"
        art_dir.mkdir(exist_ok=True)
        
        for art in gen.data["art"]:
            if art["type"] == "static":
                filepath = art_dir / f"{art['id']}.txt"
                filepath.write_text(art["content"], encoding='utf-8')
            else:
                anim_dir = art_dir / art['id']
                anim_dir.mkdir(exist_ok=True)
                for frame in art["frames"]:
                    filepath = anim_dir / f"frame_{frame['frame']}.txt"
                    filepath.write_text(frame["content"], encoding='utf-8')
        
        print(f"✓ Exported to: {export_dir}")
    
    elif args.crypto:
        # Generate crypto art (mock data for demo)
        import random
        price = random.uniform(20000, 70000)
        change = random.uniform(-10, 10)
        art = generate_crypto_art(args.crypto, price, change)
        gen.add_art(art)
        gen.save()
    
    elif args.weather:
        # Generate weather art
        import random
        temp = random.randint(30, 90)
        art = generate_weather_art(args.weather, temp)
        gen.add_art(art)
        gen.save()
    
    else:
        # Generate default content
        print("🎨 ASCII Art Widget Content Generator")
        print("=" * 40)
        gen.add_default_content()
        gen.save()
        print("\n✨ Done! Content ready for deployment.")


if __name__ == "__main__":
    main()