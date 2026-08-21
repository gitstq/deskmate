<div align="center">

# 🐾 DeskMate

### Cross-Platform Desktop Virtual Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Tests](https://img.shields.io/badge/tests-27%20passed-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)**

---

</div>

## 🎉 Introduction

**DeskMate** is a lightweight, cross-platform desktop virtual companion. It raises an adorable virtual pet on your desktop to keep you company while you work and study, with a built-in Pomodoro focus timer and system resource monitor — so your desktop is never lonely again.

### ✨ Inspiration

Inspired by `desktop-fly` (a 3D fruit fly for macOS desktop) from GitHub Trending. We've made comprehensive differentiating improvements:

- 🌍 **Cross-Platform**: No longer limited to macOS — runs perfectly on Windows / macOS / Linux
- 🎨 **Multiple Characters**: Cat / Dog / Bunny / Fox — each with unique appearance and animations
- 🖼️ **Programmatic Rendering**: All characters drawn purely in code with QPainter — **zero external image assets**, tiny package size
- 🍅 **Productivity Features**: Built-in Pomodoro timer and system monitor — not just cute, but actually boosts productivity
- ⚙️ **Highly Customizable**: Scale, pet switching, feature toggles — everything under your control

### 🎯 Problems Solved

- Working long hours in front of a screen feels lonely — you need a cute companion
- Pomodoro tools are too boring, lacking fun and sustained usage motivation
- System monitoring tools are too heavy — you just want a lightweight CPU/MEM glance
- Desktop pet tools are either platform-locked or depend on tons of external assets

---

## ✨ Key Features

### 🐾 Four Adorable Pet Characters

| Character | Traits | Signature Moves |
|-----------|--------|----------------|
| 🐱 **Cat** | Orange fur, playful tail | Tail wagging, paw licking |
| 🐶 **Dog** | Brown floppy ears, energetic | Tail wagging, tongue out |
| 🐰 **Bunny** | Snow-white fluff, long ears | Ear wiggling, hopping |
| 🦊 **Fox** | Orange-red coat, golden slit eyes | Big tail sway, fire effects |

### 🎭 Rich States & Animations

- **8 States**: Idle / Walking / Sleeping / Eating / Playing / Happy / Sad / Curious
- **Smart State Machine**: Auto behavior switching based on hunger, happiness, and energy
- **Smooth Animations**: 60fps refresh — breathing, blinking, walking, tail wagging, all included
- **Speech Bubbles**: Pets say fun lines based on their current state

### 🍅 Built-in Pomodoro Timer

- ⏱️ Customizable work/break duration (default 25 min work + 5 min break)
- 📊 Real-time countdown display with visual progress bar
- 🔔 Completion reminders — your pet celebrates with you
- 📈 Auto-tracks completed Pomodoro sessions

### 💻 Lightweight System Monitor

- 📊 Real-time CPU usage display
- 🧠 Real-time memory usage display
- 🪶 Zero-dependency `/proc` reading on Linux; optional psutil on other platforms
- 🎨 Semi-transparent floating info bar — doesn't block your work

### 🖼️ Transparent Always-On-Top Window

- 👻 Fully transparent background — the pet appears to float on your desktop
- 📌 Always on top — never hidden behind other windows
- 🖱️ Drag to move — place it anywhere you want
- 🖱️ Left-click to pet, double-click to play, right-click for menu

### 🔧 System Tray Integration

- 📥 Minimize to tray — doesn't clutter your taskbar
- 🎛️ Tray menu for quick pet switching and Pomodoro control
- 🔔 System notification alerts
- 👁️ One-click show/hide pet

---

## 🚀 Quick Start

### 📋 Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 10+ / macOS 10.14+ / Linux (X11/Wayland supported)
- **Dependency**: PyQt5 5.15+

### 📦 Installation

#### Option 1: pip install (Recommended)

```bash
# Clone the repository
git clone https://github.com/gitstq/deskmate.git
cd deskmate

# Install dependencies
pip install -r requirements.txt

# Install as CLI tool
pip install -e .
```

#### Option 2: Run directly

```bash
git clone https://github.com/gitstq/deskmate.git
cd deskmate
pip install PyQt5
python -m deskmate.main
```

### ▶️ Launch

```bash
# Start DeskMate
deskmate

# Or via module
python -m deskmate.main

# Start with a specific pet
deskmate --pet fox --name Blaze

# List all available pets
deskmate --list-pets

# Show version
deskmate --version
```

After launching, your pet appears at the bottom-right of the screen. Right-click the pet to open the interaction menu!

---

## 📖 Usage Guide

### 🖱️ Interactions

| Action | Effect |
|--------|--------|
| **Left Click** | Pet your companion, happiness +10 |
| **Left Double-Click** | Play with your pet, happiness +25 |
| **Left Drag** | Move the pet anywhere on screen |
| **Right Click** | Open the function menu |
| **Tray Left Click** | Show / hide the pet |

### 🍖 Pet Care

Use the right-click menu to care for your pet:

- **🍖 Feed**: Hunger +30, pet enters eating state
- **🎾 Play**: Happiness +25, energy -10, pet happily hops around
- **🤚 Pet**: Happiness +10, pet shows a content expression
- **😴 Sleep**: Energy +40, pet enters sleep state (Zzz appears)
- **🧼 Clean**: Cleanliness restored to full, pet sparkles

All four stats slowly decrease over time — remember to care for your pet regularly!

### 🍅 Using the Pomodoro Timer

1. Right-click pet → "🍅 Start Focus" to begin a Pomodoro session
2. A countdown status bar appears above the pet — red for work, green for break
3. Auto-switches to break when work ends, pet pops up a celebration message
4. Pause / stop / skip break anytime

Customize duration:
```bash
deskmate  # then edit ~/.deskmate/config.json
```
```json
{
  "pomodoro_work_minutes": 25,
  "pomodoro_break_minutes": 5
}
```

### 💻 System Monitor

- When enabled, a semi-transparent info bar shows at the pet's top-left: `💻 CPU 23%  MEM 56%`
- On Linux, reads `/proc/stat` and `/proc/meminfo` directly — zero extra dependencies
- On Windows / macOS, install psutil for more accurate readings
- Disable in config: `"enable_system_monitor": false`

### 🔍 Scale Adjustment

Right-click menu → "🔍 Scale" — choose 75% / 100% / 125% / 150% to fit different screen resolutions.

### ⚙️ Configuration File

Located at `~/.deskmate/config.json`. All settings can be manually edited:

```json
{
  "pet_species": "cat",
  "pet_name": "Mate",
  "scale": 1.0,
  "always_on_top": true,
  "enable_pomodoro": true,
  "pomodoro_work_minutes": 25,
  "pomodoro_break_minutes": 5,
  "enable_system_monitor": true,
  "sound_enabled": false,
  "language": "zh_CN"
}
```

### 🎬 Screenshots

> 📸 Add screenshots here

---

## 💡 Design & Roadmap

### 🏗️ Architecture

```
deskmate/
├── deskmate/
│   ├── __init__.py          # Version info
│   ├── main.py              # GUI entry point
│   ├── cli.py               # CLI entry point
│   ├── pet.py               # Pet base class + state machine
│   ├── window.py            # Transparent desktop window + renderer
│   ├── tray.py              # System tray integration
│   ├── pets/                # Pet character definitions
│   │   ├── cat.py           # 🐱 Cat
│   │   ├── dog.py           # 🐶 Dog
│   │   ├── bunny.py         # 🐰 Bunny
│   │   └── fox.py           # 🦊 Fox
│   └── utils/               # Utility modules
│       ├── config.py        # JSON config manager
│       ├── pomodoro.py      # Pomodoro timer
│       └── system_monitor.py # System resource monitor
├── tests/                   # Unit tests (27 total)
├── build.sh                 # Cross-platform build script
├── requirements.txt         # Dependencies
└── setup.py                 # Package setup
```

### 🎯 Technology Choices

| Technology | Why |
|-----------|-----|
| **Python** | Cross-platform, high dev efficiency, rich ecosystem |
| **PyQt5** | Mature & stable, supports transparent windows / tray / HiDPI, active community |
| **QPainter Procedural Drawing** | Zero external assets, tiny package, infinitely scalable, easy to customize |
| **JSON Config** | Human-readable, easy to edit, no extra dependencies |
| **/proc Direct Reading** | Zero-dependency system info on Linux, no psutil needed |

### 🗺️ Roadmap

- [ ] 🎵 Sound effects support (pet sounds, interaction feedback)
- [ ] 🌙 Dark / light theme auto-adaptation
- [ ] 🎨 More pet characters (panda, hamster, dragon, etc.)
- [ ] 👗 Pet skins / costume system
- [ ] 📊 Pomodoro data statistics & weekly reports
- [ ] 🌐 Multi-language UI (Japanese / Korean / Spanish)
- [ ] 🖼️ Enhanced interaction animations (chase cursor, dodge clicks)
- [ ] 📱 Mobile adaptation
- [ ] 🔄 Auto-start on boot configuration

### 🤝 Community Contributions

- Add new pet characters (see `CONTRIBUTING.md`)
- Translate docs to more languages
- Report bugs and suggest features
- Optimize animations and performance

---

## 📦 Build & Deploy

### 🐧 Linux Build

```bash
# Install build tool
pip install pyinstaller

# Run build script
chmod +x build.sh
./build.sh linux

# Output in release/linux/
# DeskMate-1.0.0-linux-x86_64
```

### 🍎 macOS Build

```bash
pip install pyinstaller
chmod +x build.sh
./build.sh macos

# Output in release/macos/
# DeskMate-1.0.0-macos
```

### 🪟 Windows Build

```bash
pip install pyinstaller
build.sh windows

# Or in PowerShell
pyinstaller --name DeskMate --windowed --onefile deskmate/main.py

# Output in dist/DeskMate.exe
```

### 📋 Compatibility

| Platform | Minimum Version | Transparent Window | System Tray |
|----------|----------------|-------------------|-------------|
| Windows | 10 | ✅ | ✅ |
| macOS | 10.14 (Mojave) | ✅ | ✅ |
| Linux (X11) | Any major distro | ✅ (compositor required) | ✅ |
| Linux (Wayland) | Any major distro | ⚠️ Partial | ✅ |

> ⚠️ **Linux Note**: Transparent windows require a desktop compositor. GNOME/KDE enable it by default; some lightweight window managers need manual configuration.

---

## 🤝 Contributing

We welcome all forms of contribution! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### 📝 Commit Convention

Follow the Angular commit message convention:

```
feat: New feature
fix: Bug fix
docs: Documentation
style: Code formatting
refactor: Code refactoring
test: Testing
chore: Build/tools
```

### 🧪 Run Tests

```bash
python -m pytest tests/ -v
# or
python -m unittest discover tests/ -v
```

---

## 📄 License

This project is open-sourced under the **MIT License**. See [LICENSE](LICENSE) for details.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided you include the original copyright notice and permission notice in all copies.

---

<div align="center">

**If DeskMate brings you joy, please give it a ⭐ Star!**

Made with ❤️ by DeskMate Team

</div>
