from time import sleep
import win32api
import pyautogui
import tkinter as tk
import threading

MAX_POLLING_TIME = 600


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
        self.thread: threading.Thread | None = None
        self.stop_flag: threading.Event | None = None
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
            self.stop_flag = threading.Event()
            self.thread = threading.Thread(
                target=self.start_afk_monitoring,
                args=[self.stop_flag, afk_time_int]
            )
            self.thread.daemon = True
            self.thread.start()
            self.monitoring_active.set(True)

    def deactivate_monitoring(self) -> None:
        if self.thread is not None:
            if self.stop_flag is not None:
                self.stop_flag.set()
            self.thread = None

        self.title_text.set("AFK Monitoring Idle")
        self.monitoring_active.set(False)

    def on_button_click(self) -> None:
        if self.monitoring_active.get():
            self.deactivate_monitoring()
        else:
            self.activate_monitoring()

    def start_afk_monitoring(
            self, stop_flag: threading.Event, afk_time: int) -> None:
        while not stop_flag.is_set():
            # Calculate values
            idle_time_seconds = _get_idle_time_seconds()
            if idle_time_seconds > afk_time:
                pyautogui.keyDown('[')
                pyautogui.keyDown(']')
                sleep(1)
                pyautogui.keyUp('[')
                pyautogui.keyUp(']')
                break
            else:
                sleep(min(afk_time - idle_time_seconds, MAX_POLLING_TIME))

        self.thread = None
        self.deactivate_monitoring()


if __name__ == "__main__":
    root = tk.Tk()
    AfkMonitoringApp(root)
    root.mainloop()
