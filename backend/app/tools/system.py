import pyautogui
import time
from langchain_core.tools import tool
import urllib.parse


APPLICATIONS = {
    "notepad": "notepad",
    "calculator": "calculator",
    "chrome": "chrome",
    "edge": "msedge",
    "vscode": "code",
    "explorer": "explorer",
    "file explorer": "explorer",
    "command prompt": "cmd",
    "cmd": "cmd",
    "powershell": "powershell",
    "spotify": "spotify",
    "discord": "discord",
}


@tool
def open_application(application: str) -> str:
    """Open an allowed desktop application."""

    application = application.lower().strip()

    if application not in APPLICATIONS:
        available = ", ".join(APPLICATIONS.keys())
        return (
            f"I can't open {application}. "
            f"Available applications are: {available}."
        )

    app_command = APPLICATIONS[application]

    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write(app_command)
    pyautogui.press("enter")

    return f"Opening {application}."


@tool
def search_youtube(query: str)->str:
    """Search for a video or song on Youtube."""

    query = query.strip()

    if not query:
        return "Please provide something to search for a Youtube."

    encoded_query = urllib.parse.quote_plus(query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write(url)
    pyautogui.press("enter")

    return f"Searching Youtube for {query}."


@tool
def play_youtube(query: str) -> str:
    """Search for a video or song on YouTube and play the first result."""

    query = query.strip()

    if not query:
        return "Please provide a video or song to play."

    encoded_query = urllib.parse.quote_plus(query)

    url = (
        f"https://www.youtube.com/results?"
        f"search_query={encoded_query}"
    )

    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write(url)
    pyautogui.press("enter")

    # Wait for YouTube results to load
    time.sleep(8)

    # Click approximately on the first video result
    pyautogui.click(x=500, y=350)

    return f"Playing {query} on YouTube."