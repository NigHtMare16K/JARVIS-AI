import logging
import os
import subprocess
import time
import urllib.parse

import pyautogui
import pygetwindow as gw

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


def _focus_spotify() -> bool:
    """Try to bring Spotify to the foreground."""
    for title_part in ("Spotify", "Spotify Premium"):
        windows = gw.getWindowsWithTitle(title_part)
        if windows:
            try:
                win = windows[0]
                if win.isMinimized:
                    win.restore()
                win.activate()
                time.sleep(0.5)
                return True
            except Exception:
                continue
    return False


def _launch_spotify_search(song: str) -> None:
    """Open Spotify via URI deep link."""
    encoded = urllib.parse.quote(song)
    uri = f"spotify:search:{encoded}"

    try:
        os.startfile(uri)
    except OSError:
        subprocess.Popen(
            ["cmd", "/c", "start", "", uri],
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


@tool
def play_spotify(song: str) -> str:
    """Play a song on the Spotify desktop app. Use when user asks to play music on Spotify."""
    song = song.strip()
    if not song:
        return "Please tell me which song to play."

    # Strip trailing "on spotify" if the LLM included it
    lower = song.lower()
    for suffix in (" on spotify", " in spotify"):
        if lower.endswith(suffix):
            song = song[: -len(suffix)].strip()
            break

    try:
        _launch_spotify_search(song)
        time.sleep(4)

        if not _focus_spotify():
            time.sleep(2)
            _focus_spotify()

        time.sleep(0.5)

        # Navigate to first search result and play
        pyautogui.press("tab", presses=2, interval=0.2)
        pyautogui.press("enter")
        time.sleep(0.8)
        pyautogui.press("space")

        return f"Playing {song} on Spotify."

    except Exception as exc:
        logger.exception("Spotify playback failed")
        return (
            f"I opened Spotify and searched for {song}, but couldn't start playback automatically. "
            f"Please press Enter on the first result. ({exc})"
        )
