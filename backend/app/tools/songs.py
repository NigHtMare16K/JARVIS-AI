import urllib.parse
import pyautogui
import time

from langchain_core.tools import tool

@tool
def play_spotify(song: str) -> str:
    """Open Spotify desktop app, search for a song, and play it."""

    song = song.strip()

    if not song:
        return "Please provide a song to play."

    encoded_song = urllib.parse.quote(song)

    # Open Spotify
    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write("spotify:")
    pyautogui.press("enter")

    time.sleep(4)

    # Search
    pyautogui.hotkey("ctrl", "l")
    time.sleep(1)

    pyautogui.write(f"spotify:search:{encoded_song}")
    pyautogui.press("enter")

    time.sleep(4)

    # Navigate to first result
    pyautogui.press("tab", presses=3, interval=0.3)
    pyautogui.press("enter")

    time.sleep(2)

    # Play
    pyautogui.press("space")

    return f"Playing {song} on Spotify."