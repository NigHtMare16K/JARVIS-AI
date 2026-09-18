import logging
import os
import re
from pathlib import Path

from langchain_core.tools import tool

from app.rag.document_manager import get_document_manager

logger = logging.getLogger(__name__)

SPECIAL_FOLDERS = {
    "downloads": Path.home() / "Downloads",
    "download": Path.home() / "Downloads",
    "documents": Path.home() / "Documents",
    "document": Path.home() / "Documents",
    "desktop": Path.home() / "Desktop",
    "pictures": Path.home() / "Pictures",
    "picture": Path.home() / "Pictures",
    "music": Path.home() / "Music",
    "videos": Path.home() / "Videos",
    "video": Path.home() / "Videos",
    "home": Path.home(),
}


def _normalize_request(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r"^(open|show|launch)\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^(my|the)\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+folder$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+file$", "", text, flags=re.IGNORECASE)
    return text.strip()


def _resolve_path(request: str) -> tuple[str | None, str | None]:
    """Returns (path, error_message)."""
    normalized = _normalize_request(request)
    key = normalized.lower()

    # Known Windows folders
    if key in SPECIAL_FOLDERS:
        path = SPECIAL_FOLDERS[key]
        if path.exists():
            return str(path), None
        return None, f"The {key} folder doesn't exist at {path}."

    # Explicit path (preserve case)
    expanded = os.path.expanduser(request.strip())
    if os.path.isabs(expanded) or expanded.startswith("~"):
        if os.path.exists(expanded):
            return expanded, None
        return None, f"I couldn't find {expanded}."

    # Filename with extension (e.g. Python_Lab_2.pdf)
    if "." in normalized:
        candidate = Path(normalized)
        if candidate.exists():
            return str(candidate.resolve()), None

        manager = get_document_manager()
        resolved, error = manager.resolve_pdf_path(normalized)
        if resolved:
            return resolved, None
        if error:
            return None, error

        # Search by filename in allowlisted dirs
        matches = manager.search_in_dirs(normalized)
        if len(matches) == 1:
            return matches[0], None
        if len(matches) > 1:
            return None, (
                f"Multiple files named {normalized} found: "
                f"{', '.join(matches[:3])}. Please be more specific."
            )
        return None, f"I couldn't find a file named {normalized}."

    # Folder name without extension — try as subfolder of home
    home_candidate = Path.home() / normalized
    if home_candidate.exists():
        return str(home_candidate), None

    # Try special folder partial match
    for name, folder_path in SPECIAL_FOLDERS.items():
        if key == name or key.endswith(name):
            if folder_path.exists():
                return str(folder_path), None

    return None, f"I couldn't find '{request}'. Try a folder name like Downloads or a full file path."


@tool
def open_file_or_folder(path: str) -> str:
    """Open a file or folder on the Windows computer. Supports Downloads, Desktop, Documents, and known PDF files."""
    path = path.strip()
    if not path:
        return "Please tell me which file or folder to open."

    actual_path, error = _resolve_path(path)
    if error:
        return error
    if not actual_path:
        return f"I couldn't find {path}."

    try:
        os.startfile(actual_path)
        name = Path(actual_path).name
        return f"Opening {name}."
    except Exception as exc:
        logger.exception("Failed to open %s", actual_path)
        return f"I couldn't open it: {exc}"
