import urllib.parse
import pyautogui
import time

from langchain_core.tools import tool

@tool
def play_spotify(song: str) -> str:
    """Open the Spotify desktop app and search for a song."""

    song = song.strip()

    if not song:
        return "Please provide a song to play."

    encoded_song = urllib.parse.quote(song)

    pyautogui.hotkey("win","r")
    time.sleep(1)

    pyautogui.write("spotify:")
    pyautogui.press("enter")

    time.sleep(4)

    pyautogui.hotkey("ctrl","l")
    time.sleep(1)

    pyautogui.write(f"spotify:search:{encoded_song}")
    pyautogui.press("enter")

    time.sleep(4)

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")

    time.sleep(2)

    return f"Playing  {song} on Spotify."

