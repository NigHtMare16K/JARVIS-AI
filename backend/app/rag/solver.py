import os

SEARCH_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.join(os.path.dirname(__file__), "..", "..", "documents"),
]


def find_pdf_path(filename: str) -> str | None:
    for directory in SEARCH_DIRS:
        candidate = os.path.join(directory, filename)
        if os.path.exists(candidate):
            return candidate
    return None