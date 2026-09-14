import pygetwindow as gw
import time

def get_active_window_title():
    window = gw.getActiveWindow()

    if window is None:
        return None

    return window.title

if __name__ == "__main__":
    print("Focus your PDF window...")
    time.sleep(5)

    title = get_active_window_title()
    print("🪟 Active window:", title)