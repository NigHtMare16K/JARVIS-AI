import pygetwindow as gw
import time
import re

def get_active_window_title():
    window = gw.getActiveWindow()

    if window is None:
        return None

    return window.title

def get_active_pdf():
    title = get_active_window_title()

    if not title:
        return None

    match = re.search(r'[^\\/:*?"<>|\r\n]+\.pdf\b', title, re.IGNORECASE)

    if match:
        return match.group(0)

    return None

if __name__ == "__main__":
    print("Focus your PDF window...")
    time.sleep(5)

    pdf = get_active_pdf()

    if pdf:
        print("📖 Active PDF:", pdf)
    else:
        print("❌ Active window is not a PDF")

    title = get_active_window_title()
    print("🪟 Active window:", title)