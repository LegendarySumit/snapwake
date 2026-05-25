<div align="center">

# ⏰ SnapWake

**Modern desktop alarm clock — Wake up on time, every time**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)

**Simple • Lightweight • Beautiful • Works Offline**

[📥 Download .exe](#-quick-start) • [✨ Features](#-features) • [🚀 Getting Started](#-getting-started) • [📖 Guide](#-guide)

</div>

---

## 📖 About

SnapWake is a sleek, lightweight desktop alarm clock application designed for developers, students, and anyone who needs a minimal, distraction-free alarm solution. Built with Python and Tkinter, it delivers a beautiful dark-mode interface with intuitive controls.

Whether you're working late, need a quick timer, or just want a reliable alarm—SnapWake has got you covered. Set custom wake-up times, choose from 4 carefully curated alarm tones, use your own audio files, or create sophisticated snooze patterns. All with zero bloat and offline support.

**Perfect for:** Night owls 🌙 • Developers coding 💻 • Students 📚 • Anyone who loves minimalist tools ⚡

---

## ✨ Features

- ✅ **24-Hour Time Format** — Simple HH:MM input, no confusion with AM/PM
- ✅ **4 Preset Alarms** — Beautiful curated sounds (Classic Clock, Short Alert, Electronic Chime, Bedside Bell)
- ✅ **Custom Audio Support** — Browse and use any `.mp3`, `.wav`, or `.ogg` file
- ✅ **Smart Snooze** — 5-minute default snooze with persistent popup alerts
- ✅ **Dark Theme UI** — Modern dark navy + cyan design, easy on the eyes
- ✅ **Lightweight & Fast** — Pure Python, minimal dependencies, instant startup
- ✅ **Offline Ready** — No internet required, runs completely locally
- ✅ **Background Monitoring** — Window can stay minimized, alarm still triggers
- ✅ **Standalone Executable** — Download `.exe` and run—no Python installation needed

---

## 🛠️ Tech Stack

### Core
- **Python** 3.13.12 — Programming language
- **Tkinter** — Native GUI framework (built-in with Python)
- **pygame** 2.6.1 — Audio playback engine
- **Threading** — Background alarm monitoring

### Build & Distribution
- **PyInstaller** — Package as standalone `.exe`
- **Git** — Version control

---

## 📁 Project Structure

```
snapwake/
├── alarm_clock_app.py          # Main application file (~350 lines)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
├── sounds/                     # Bundled alarm audio files
│   ├── alarm-clock.mp3         # Classic clock sound
│   ├── alarm-short.mp3         # Short alert
│   ├── electronic-chime.mp3    # Electronic chime
│   └── bedside-bell.mp3        # Bedside bell
└── dist/
    └── SnapWake.exe            # Standalone Windows executable
```

---

## 🚀 Quick Start

### Option 1: **Easy Way** (Recommended for everyone)

No Python? No problem! Download and run the executable:

1. Go to [GitHub Releases](https://github.com/LegendarySumit/snapwake/releases)
2. Download `SnapWake.exe`
3. Double-click → **App launches instantly** ✨
4. That's it! No installation, no dependencies

**Supported:** Windows 7 and later

---

### Option 2: **Developer Way** (Python users)

Clone the repository and run from source:

```bash
# Clone the repository
git clone https://github.com/LegendarySumit/snapwake.git
cd snapwake

# Install dependencies
pip install -r requirements.txt

# Run the app
python alarm_clock_app.py
```

**Requirements:**
- Python 3.10+
- Tkinter (included with Python)
- pygame 2.5.0+

---

## 📚 Guide

### Setting an Alarm

1. **Enter Time** — Type alarm time in 24-hour format (e.g., `07:30`, `14:45`)
2. **Choose Tone** — Select from 4 presets or click "Browse" for custom audio
3. **Set Alarm** — Click "Set Alarm" button
4. **Wait** — Keep window open (can minimize). Alarm monitors in background
5. **Wake Up** — Popup alert appears at scheduled time with Stop/Snooze buttons

### Using Custom Audio

1. Click **"Browse"** in the Tone selector
2. Navigate to your audio file (`.mp3`, `.wav`, `.ogg`)
3. Select and confirm
4. Your custom sound is now the active alarm

### Snoozing

When the alarm rings:
- **Snooze:** Click "Snooze" for 5-minute delay
- **Stop:** Click "Stop" to cancel the alarm immediately

---

## ⚙️ Configuration

### Default Alarm Tones

The app comes with 4 preset sounds located in `sounds/` folder:

| Sound | File | Use Case |
|-------|------|----------|
| 🔔 Classic Clock | `alarm-clock.mp3` | Traditional alarm feel |
| ⏰ Short Alert | `alarm-short.mp3` | Quick, crisp notification |
| 🎺 Electronic Chime | `electronic-chime.mp3` | Modern electronic sound |
| 🛏️ Bedside Bell | `bedside-bell.mp3` | Gentle but persistent |

### Snooze Duration

Default snooze time: **5 minutes**

To modify, edit [alarm_clock_app.py](alarm_clock_app.py) and find the `snooze_alarm()` method, change the timedelta value.

---

## 🎨 UI Features

- **Dark Navy Theme** (#0f172a) — Reduces eye strain
- **Cyan Accents** (#06b6d4) — Modern, clean aesthetic
- **Responsive Layout** — Proper spacing and alignment
- **Status Messages** — Real-time feedback on alarm state
- **Always-on-Top Popup** — Alert stays visible even when minimized

---

## 🐛 Troubleshooting

### "Alarm doesn't ring"
- ✅ Keep the SnapWake window open (minimize is fine)
- ✅ Check system volume is not muted
- ✅ Ensure selected audio file exists and is playable

### "No sound on alarm"
- ✅ Check your audio output device is working
- ✅ Try a different preset alarm sound
- ✅ Verify pygame is installed: `pip install pygame`

### "Time format error"
- ✅ Use 24-hour format: `07:30` not `7:30`
- ✅ Valid range: `00:00` to `23:59`

### ".exe doesn't launch"
- ✅ Ensure Windows 7 or later
- ✅ Disable antivirus temporarily (false positive)
- ✅ Run as Administrator if prompted

---

## 🔮 Future Enhancements

- [ ] Multiple simultaneous alarms
- [ ] Recurring alarms (daily, weekly)
- [ ] Alarm history/statistics
- [ ] Customizable snooze duration via UI
- [ ] Sunrise simulation mode
- [ ] System tray integration
- [ ] Settings persistence (saved alarms)
- [ ] macOS & Linux support

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Lines of Code** | ~350 |
| **Dependencies** | 2 (pygame + Tkinter) |
| **Build Size** | ~12 MB (.exe) |
| **Startup Time** | < 1 second |
| **Memory Usage** | ~50 MB |
| **Python Version** | 3.10+ |

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

```
Copyright (c) 2026 Legendary Sumit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, modify, and distribute it freely.
```

---

## 👨‍💻 Author

**Legendary Sumit**

- **GitHub:** [@LegendarySumit](https://github.com/LegendarySumit)
- **Repository:** [SnapWake](https://github.com/LegendarySumit/snapwake)
- **Live Demo:** Download from [Releases](https://github.com/LegendarySumit/snapwake/releases)

---

<div align="center">

### 🌅 Wake Up Right, Every Time

**Give it a ⭐ if you found it helpful!**

*Built with ❤️ by [Legendary Sumit](https://github.com/LegendarySumit)*

</div>