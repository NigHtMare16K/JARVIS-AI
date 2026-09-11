import os

from langchain_core.tools import tool


SPECIAL_FOLDERS = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "download": os.path.join(os.path.expanduser("~"), "Downloads"),

    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "document": os.path.join(os.path.expanduser("~"), "Documents"),

    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),

    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "pictures folder": os.path.join(os.path.expanduser("~"), "Pictures"),

    "music": os.path.join(os.path.expanduser("~"), "Music"),

    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
}


@tool
def open_file_or_folder(path: str) -> str:
    """Open a file or folder on the Windows computer."""

    path = path.strip().lower()

    # Remove common natural-language words
    path = path.replace("my ", "")
    path = path.replace("the ", "")
    path = path.replace(" folder", "")

    # Check known Windows folders
    if path in SPECIAL_FOLDERS:
        actual_path = SPECIAL_FOLDERS[path]
    else:
        # Treat it as a normal Windows path
        actual_path = os.path.expanduser(path)

    if not os.path.exists(actual_path):
        return f"I couldn't find {actual_path}."

    try:
        os.startfile(actual_path)
        return f"Opening {actual_path}."

    except Exception as e:
        return f"I couldn't open it: {str(e)}"