import pyautogui
import time
from langchain_core.tools import tool


@tool
def open_application(application: str) -> str:
    """Open a desktop application such as Notepad, Calculator, or Chrome."""

    application = application.lower().strip()

    if application == "notepad":
        pyautogui.hotkey("win", "r")
        time.sleep(1)
        pyautogui.write("notepad")
        pyautogui.press("enter")

        return "Notepad has been opened."

    elif application == "calculator":
        pyautogui.hotkey("win", "r")
        time.sleep(1)
        pyautogui.write("calculator")
        pyautogui.press("enter")

        return "Calculator has been opened."

    elif application == "chrome":
        pyautogui.hotkey("win", "r")
        time.sleep(1)
        pyautogui.write("chrome")
        pyautogui.press("enter")

        return "Chrome has been opened."

    return f"I don't know how to open {application} yet."