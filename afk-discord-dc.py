from time import sleep
import win32api
import pyautogui
import tkinter as tk

MAX_POLLING_TIME = 600
MIN_POLLING_TIME = 1


def _get_idle_time_seconds() -> int:
    """
    Retrieves the tick count when the last input event was received.
    Returns the tick count in milliseconds.
    """
    last_input_tick_count = win32api.GetLastInputInfo()
    current_tick_count = win32api.GetTickCount()
    return (current_tick_count - last_input_tick_count) // 1000


class AfkMonitoringApp:
    def __init__(self, root: tk.Tk):
        # Setup root
        root.title("Discord AFK Auto Kicker")
        root.geometry("300x200")
        icon = tk.PhotoImage(file="Screenshot_2025-01-03_202415.png")
        root.iconphoto(True, icon)
        self.title_text = tk.StringVar(value="AFK Monitoring Idle")
        label = tk.Label(root, textvariable=self.title_text)
        label.pack(pady=20)

        entry_instructions = tk.Label(
            root, text="Enter the AFK threshold in seconds:")
        entry_instructions.pack(pady=(20, 3))
        self.afk_time_str = tk.StringVar(value="3600")
        entry = tk.Entry(root, width=15, textvariable=self.afk_time_str)
        entry.pack()

        self.button = tk.Button(
            root, text="Toggle Monitoring", command=self.on_button_click)
        self.button.pack(pady=(20, 0))

        # Global & State Variables
        self.root = root
        self.monitoring_active: tk.BooleanVar = tk.BooleanVar(value=False)

    def activate_monitoring(self) -> None:
        try:
            # Validate that entry is an int
            afk_time_int = int(self.afk_time_str.get())
        except ValueError:
            old_txt = self.title_text.get()
            self.title_text.set("Invalid time in seconds for AFK threshold!")
            self.root.after(1000, lambda: self.title_text.set(old_txt))
        else:
            self.title_text.set("AFK Monitoring Active")
            self.monitoring_active.set(True)
            self.schedule_afk_check(afk_time_int)

    def deactivate_monitoring(self) -> None:
        self.title_text.set("AFK Monitoring Idle")
        self.monitoring_active.set(False)

    def on_button_click(self) -> None:
        if self.monitoring_active.get():
            self.deactivate_monitoring()
        else:
            self.activate_monitoring()

    def schedule_afk_check(self, afk_time: int) -> None:
        if not self.monitoring_active.get():
            return

        # Calculate values
        print(afk_time)
        idle_time_seconds = _get_idle_time_seconds()
        if idle_time_seconds > afk_time:
            pyautogui.keyDown('[')
            pyautogui.keyDown(']')
            sleep(1)
            pyautogui.keyUp('[')
            pyautogui.keyUp(']')
            self.deactivate_monitoring()
        else:
            next_poll = afk_time - idle_time_seconds
            delay = max(
                MIN_POLLING_TIME,
                min(MAX_POLLING_TIME, next_poll)
            ) * 1000
            self.root.after(delay, self.schedule_afk_check, afk_time)


if __name__ == "__main__":
    root = tk.Tk()
    AfkMonitoringApp(root)
    root.mainloop()
