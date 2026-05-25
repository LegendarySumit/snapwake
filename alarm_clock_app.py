from __future__ import annotations

import importlib
import importlib.util
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Modern color scheme
COLORS = {
    "bg_primary": "#0f172a",      # Deep navy background
    "bg_secondary": "#1e293b",    # Lighter navy
    "bg_tertiary": "#334155",     # Gray-blue
    "accent_primary": "#06b6d4",  # Cyan
    "accent_secondary": "#3b82f6", # Blue
    "text_primary": "#f1f5f9",    # Light text
    "text_secondary": "#cbd5e1",  # Muted text
    "success": "#10b981",         # Green
    "warning": "#f59e0b",         # Amber
    "danger": "#ef4444",          # Red
}


def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = max((screen_width - width) // 2, 0)
    y_position = max((screen_height - height) // 2, 0)
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


@dataclass
class AlarmState:
    target_time: datetime | None = None
    ringing: bool = False
    popup: tk.Toplevel | None = None


class AlarmClockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SnapWake ⏰")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_primary"])
        center_window(self.root, 500, 420)

        # Configure custom style
        self._configure_style()

        self.state = AlarmState()
        self.pygame = self._load_pygame()
        self.sound_path = tk.StringVar(value="")  # Stores actual file path
        self.display_name = tk.StringVar(value="")  # Displays friendly name (starts blank)
        self.time_value = tk.StringVar(value=self._default_time())
        self.status_value = tk.StringVar(value="Set a time, choose a tone, then start the alarm.")
        self.target_value = tk.StringVar(value="⏱ No alarm scheduled")
        
        # Default alarm sounds mapping (bundled with project)
        self.default_alarms = {
            "🔔 Classic Clock": os.path.join(os.path.dirname(__file__), 'sounds', 'alarm-clock.mp3'),
            "⏰ Short Alert": os.path.join(os.path.dirname(__file__), 'sounds', 'alarm-short.mp3'),
            "🎺 Electronic Chime": os.path.join(os.path.dirname(__file__), 'sounds', 'electronic-chime.mp3'),
            "🛏️ Bedside Bell": os.path.join(os.path.dirname(__file__), 'sounds', 'bedside-bell.mp3'),
        }

        self._build_ui()
        self._tick()

    def _load_pygame(self):
        if importlib.util.find_spec("pygame") is None:
            return None

        module = importlib.import_module("pygame")
        module.mixer.init()
        return module

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure colors for ttk widgets
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=COLORS["accent_primary"])
        style.configure("Subtitle.TLabel", font=("Segoe UI", 9), foreground=COLORS["text_secondary"])
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground=COLORS["text_secondary"])
        
        # Entry styling
        style.configure("TEntry", fieldbackground=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=("Segoe UI", 11))
        
        # Combobox styling
        style.configure("TCombobox", fieldbackground=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=("Segoe UI", 11))
        
        # Button styling
        style.configure("TButton", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], 
                       font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat", padding=10)
        style.map("TButton",
                 background=[("active", COLORS["accent_primary"]), ("pressed", COLORS["accent_secondary"])],
                 foreground=[("active", COLORS["bg_primary"]), ("pressed", COLORS["bg_primary"])])
        
        # Primary button
        style.configure("Primary.TButton", background=COLORS["accent_primary"], foreground=COLORS["bg_primary"])
        style.map("Primary.TButton",
                 background=[("active", COLORS["accent_secondary"]), ("pressed", COLORS["accent_secondary"])])
        
        # Danger button
        style.configure("Danger.TButton", background=COLORS["danger"])
        style.map("Danger.TButton",
                 background=[("active", "#dc2626"), ("pressed", "#991b1b")])
        
        # Success button
        style.configure("Success.TButton", background=COLORS["success"])
        style.map("Success.TButton",
                 background=[("active", "#059669"), ("pressed", "#047857")])
        
        # Separator
        style.configure("TSeparator", background=COLORS["bg_tertiary"])

    def _default_time(self) -> str:
        return (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)

        # Header
        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(0, 24))
        
        ttk.Label(header_frame, text="SnapWake", style="Title.TLabel").pack()
        ttk.Label(header_frame, text="Wake up on time, every time", style="Subtitle.TLabel").pack(pady=(4, 0))

        # Time Section
        time_section = ttk.Frame(main)
        time_section.pack(fill="x", pady=(0, 20))
        
        ttk.Label(time_section, text="🕐 Alarm Time (24-hour HH:MM)", font=("Segoe UI", 11, "bold"), 
                 foreground=COLORS["accent_primary"]).pack()
        
        time_entry_wrapper = ttk.Frame(time_section)
        time_entry_wrapper.pack()
        
        self.time_entry = ttk.Entry(time_entry_wrapper, textvariable=self.time_value, justify="center", width=12)
        self.time_entry.pack(pady=(8, 0))

        # Tone Section
        tone_section = ttk.Frame(main)
        tone_section.pack(fill="x", pady=(0, 20))
        
        ttk.Label(tone_section, text="🎵 Alarm Tone", font=("Segoe UI", 11, "bold"), 
                 foreground=COLORS["accent_primary"]).pack()
        
        tone_entry_frame = ttk.Frame(tone_section)
        tone_entry_frame.pack(fill="x", pady=(8, 0))
        
        # Default ringtone dropdown with placeholder - no grey overlay
        self.ringtone_var = tk.StringVar(value="Choose Our Default")
        dropdown_values = ["Choose Our Default"] + list(self.default_alarms.keys())
        ringtone_dropdown = ttk.Combobox(
            tone_entry_frame, 
            textvariable=self.ringtone_var,
            values=dropdown_values,
            state="normal",
            width=25,
            height=5,
            justify="center"
        )
        ringtone_dropdown.pack(side="left", padx=(0, 8), fill="both")
        ringtone_dropdown.bind("<<ComboboxSelected>>", self._on_ringtone_selected)

        browse_button = ttk.Button(tone_entry_frame, text="📁 Browse Custom", command=self.choose_sound)
        browse_button.pack(side="left")
        
        # Display field showing selected tone name (blank initially, same height as others)
        tone_display = ttk.Entry(tone_entry_frame, textvariable=self.display_name, state="readonly")
        tone_display.pack(side="left", padx=(8, 0), fill="both", expand=True)

        # Buttons Section
        button_row = ttk.Frame(main)
        button_row.pack(fill="x", pady=(0, 20))

        self.set_button = ttk.Button(button_row, text="▶ Set Alarm", command=self.set_alarm, style="Primary.TButton")
        self.set_button.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.cancel_button = ttk.Button(button_row, text="✕ Cancel", command=self.cancel_alarm)
        self.cancel_button.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.snooze_button = ttk.Button(button_row, text="😴 Snooze", command=self.snooze_alarm, style="Success.TButton")
        self.snooze_button.pack(side="left", expand=True, fill="x")

        # Separator
        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=12)

        # Status Section
        status_frame = ttk.Frame(main)
        status_frame.pack(fill="both", expand=True, pady=(8, 0))
        
        ttk.Label(status_frame, textvariable=self.target_value, font=("Segoe UI", 10, "bold"), 
                 foreground=COLORS["accent_primary"]).pack(pady=(4, 0))

        self.snooze_button.state(["disabled"])

    def choose_sound(self) -> None:
        selected = filedialog.askopenfilename(
            title="Select alarm tone",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg"),
                ("All files", "*.*"),
            ],
        )
        if selected:
            self.sound_path.set(selected)
            self.ringtone_var.set("Choose Our Default")  # Reset dropdown to placeholder
            self.display_name.set(Path(selected).name)  # Show just the filename
            self.status_value.set(f"✓ Selected custom: {Path(selected).name}")

    def _on_ringtone_selected(self, event=None) -> None:
        selected = self.ringtone_var.get()
        
        # If placeholder is selected, clear everything
        if selected == "Choose Our Default":
            self.sound_path.set("")
            self.display_name.set("")
            self.status_value.set("Choose an alarm tone")
            return
        
        if selected in self.default_alarms:
            file_path = self.default_alarms[selected]
            self.sound_path.set(file_path)
            self.display_name.set(selected)
            self.status_value.set(f"✓ Selected: {selected}")

    def set_alarm(self) -> None:
        if self.state.ringing:
            messagebox.showinfo("Alarm ringing", "Stop the current alarm before setting a new one.")
            return

        raw_time = self.time_value.get().strip()
        try:
            target_clock = datetime.strptime(raw_time, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Invalid time", "Use 24-hour HH:MM format, for example 07:30 or 18:05.")
            return

        now = datetime.now()
        target = datetime.combine(now.date(), target_clock)
        if target <= now:
            target += timedelta(days=1)

        self.state.target_time = target
        self.target_value.set(f"Alarm scheduled for {target.strftime('%Y-%m-%d %H:%M')}")
        self.status_value.set("Alarm armed. Keep this window open.")
        self.snooze_button.state(["disabled"])
        self.set_button.state(["disabled"])

    def cancel_alarm(self) -> None:
        self._stop_ringing()
        self.state.target_time = None
        self.set_button.state(["!disabled"])
        self.snooze_button.state(["disabled"])
        self.target_value.set("No alarm scheduled")
        self.status_value.set("Alarm canceled.")

    def snooze_alarm(self) -> None:
        if not self.state.ringing:
            return

        self._stop_sound()
        self._close_popup()

        minutes = 5
        self.state.ringing = False
        self.state.target_time = datetime.now() + timedelta(minutes=minutes)
        self.target_value.set(f"Snoozed until {self.state.target_time.strftime('%Y-%m-%d %H:%M')}")
        self.status_value.set(f"Snoozed for {minutes} minutes.")
        self.set_button.state(["disabled"])
        self.snooze_button.state(["disabled"])

    def _tick(self) -> None:
        if self.state.target_time and not self.state.ringing and datetime.now() >= self.state.target_time:
            self._trigger_alarm()

        self.root.after(1000, self._tick)

    def _trigger_alarm(self) -> None:
        self.state.ringing = True
        self.status_value.set("Alarm is ringing.")
        self.snooze_button.state(["!disabled"])
        self._start_sound()
        self._show_popup()

    def _show_popup(self) -> None:
        if self.state.popup is not None:
            return

        popup = tk.Toplevel(self.root)
        popup.title("🔔 Alarm Alert!")
        popup.resizable(False, False)
        popup.configure(bg=COLORS["bg_primary"])
        popup.attributes("-topmost", True)
        popup.protocol("WM_DELETE_WINDOW", self.stop_alarm)
        center_window(popup, 340, 220)

        frame = ttk.Frame(popup, padding=24)
        frame.pack(fill="both", expand=True)

        # Alert icon and message
        ttk.Label(frame, text="🔔 ALARM RINGING!", font=("Segoe UI", 16, "bold"), 
                 foreground=COLORS["danger"]).pack(pady=(0, 10))
        ttk.Label(frame, text="Time to wake up!", font=("Segoe UI", 11), 
                 foreground=COLORS["text_secondary"]).pack(pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", expand=True)

        ttk.Button(frame, text="⏹ Stop", command=self.stop_alarm, style="Danger.TButton").pack(
            fill="x", pady=(0, 8)
        )
        ttk.Button(frame, text="😴 Snooze 5 min", command=self.snooze_alarm, style="Success.TButton").pack(
            fill="x"
        )

        self.state.popup = popup

    def stop_alarm(self) -> None:
        self._stop_sound()
        self._close_popup()
        self.state.ringing = False
        self.state.target_time = None
        self.set_button.state(["!disabled"])
        self.snooze_button.state(["disabled"])
        self.target_value.set("No alarm scheduled")
        self.status_value.set("Alarm stopped.")

    def _start_sound(self) -> None:
        sound = self.sound_path.get().strip()
        if self.pygame is None:
            self.root.bell()
            self.status_value.set("pygame is not installed, so the system bell is playing instead.")
            return

        if not sound:
            self.root.bell()
            self.status_value.set("No tone selected, so the system bell is playing instead.")
            return

        path = Path(sound)
        if not path.exists():
            messagebox.showerror("Missing file", f"Could not find the selected tone:\n{sound}")
            return

        try:
            self.pygame.mixer.music.load(str(path))
            self.pygame.mixer.music.play(loops=-1)
        except Exception as exc:  # pragma: no cover - user-facing audio failure
            messagebox.showerror("Playback error", f"Unable to play {path.name}: {exc}")

    def _stop_sound(self) -> None:
        if self.pygame is not None:
            self.pygame.mixer.music.stop()
        else:
            self.root.bell()

    def _stop_ringing(self) -> None:
        self.state.ringing = False
        self._stop_sound()
        self._close_popup()

    def _close_popup(self) -> None:
        if self.state.popup is not None:
            self.state.popup.destroy()
            self.state.popup = None


def main() -> None:
    root = tk.Tk()
    AlarmClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()