"""Document registry and PDF path resolution for RAG."""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

# Allowlisted search locations (no full-drive scan)
SEARCH_DIRS: list[Path] = [
    Path.home() / "Desktop",
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Videos",
    Path.home() / "Music",
    Path.home() / "OneDrive",
    Path.home() / "OneDrive" / "Desktop",
    Path.home() / "OneDrive" / "Documents",
    _BACKEND_DIR,
    _BACKEND_DIR / "documents",
]


class DocumentManager:
    """Tracks indexed PDFs and resolves filenames to local paths."""

    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = Path(registry_path or settings.DOCUMENT_REGISTRY_PATH)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict:
        if self.registry_path.exists():
            try:
                with open(self.registry_path, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Could not load document registry: %s", exc)
        return {"documents": {}, "path_cache": {}}

    def _save(self) -> None:
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
        except OSError as exc:
            logger.error("Could not save document registry: %s", exc)

    def _doc_key(self, full_path: str) -> str:
        return str(Path(full_path).resolve()).lower()

    def get_document(self, full_path: str) -> Optional[dict]:
        return self._data["documents"].get(self._doc_key(full_path))

    def register_path(self, full_path: str, file_name: Optional[str] = None) -> None:
        path = Path(full_path).resolve()
        if not path.exists():
            return

        name = file_name or path.name
        mtime = path.stat().st_mtime

        key = self._doc_key(str(path))
        existing = self._data["documents"].get(key, {})

        self._data["documents"][key] = {
            "file_name": name,
            "full_path": str(path),
            "last_modified": mtime,
            "indexing_status": existing.get("indexing_status", "pending"),
            "last_indexed": existing.get("last_indexed"),
        }

        cache = self._data.setdefault("path_cache", {})
        paths = cache.setdefault(name.lower(), [])
        path_str = str(path)
        if path_str not in paths:
            paths.append(path_str)

        self._save()

    def mark_indexed(self, full_path: str) -> None:
        path = Path(full_path).resolve()
        key = self._doc_key(str(path))
        mtime = path.stat().st_mtime

        self._data["documents"][key] = {
            "file_name": path.name,
            "full_path": str(path),
            "last_modified": mtime,
            "indexing_status": "indexed",
            "last_indexed": time.time(),
        }
        self.register_path(str(path))
        self._save()

    def needs_reindex(self, full_path: str) -> bool:
        path = Path(full_path)
        if not path.exists():
            return False

        doc = self.get_document(str(path))
        if not doc or doc.get("indexing_status") != "indexed":
            return True

        current_mtime = path.stat().st_mtime
        return current_mtime > doc.get("last_modified", 0)

    def is_indexed(self, full_path: str) -> bool:
        doc = self.get_document(full_path)
        return bool(doc and doc.get("indexing_status") == "indexed" and not self.needs_reindex(full_path))

    def search_in_dirs(self, file_name: str, max_depth: int = 3) -> list[str]:
        """Search allowlisted directories for a PDF filename."""
        matches: list[str] = []
        target = file_name.lower()

        for base in SEARCH_DIRS:
            if not base.exists():
                continue
            try:
                for root, dirs, files in os.walk(base):
                    depth = len(Path(root).relative_to(base).parts)
                    if depth >= max_depth:
                        dirs.clear()
                        continue

                    for fname in files:
                        if fname.lower() == target:
                            matches.append(str(Path(root) / fname))
            except (OSError, ValueError):
                continue

        return matches

    def resolve_pdf_path(self, file_name: str) -> tuple[Optional[str], Optional[str]]:
        """
        Resolve a PDF filename to a full path.
        Returns (path, error_message). path is None on failure.
        """
        if not file_name or not file_name.lower().endswith(".pdf"):
            file_name = f"{file_name}.pdf" if file_name else file_name

        normalized = Path(file_name).name
        cache_key = normalized.lower()

        # 1. Registry cache
        cached = self._data.get("path_cache", {}).get(cache_key, [])
        valid_cached = [p for p in cached if Path(p).exists()]
        if len(valid_cached) == 1:
            self.register_path(valid_cached[0], normalized)
            return valid_cached[0], None
        if len(valid_cached) > 1:
            return None, (
                f"I found multiple copies of {normalized}. "
                f"Please specify which one: {', '.join(valid_cached)}"
            )

        # 2. Registry documents by file_name
        registry_matches = [
            d["full_path"]
            for d in self._data.get("documents", {}).values()
            if d.get("file_name", "").lower() == cache_key and Path(d["full_path"]).exists()
        ]
        if len(registry_matches) == 1:
            return registry_matches[0], None
        if len(registry_matches) > 1:
            return None, (
                f"Multiple {normalized} files are registered: {', '.join(registry_matches)}"
            )

        # 3. Search allowlisted directories
        found = self.search_in_dirs(normalized)
        if len(found) == 1:
            self.register_path(found[0], normalized)
            return found[0], None
        if len(found) > 1:
            # Prefer most recently modified
            found.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
            self.register_path(found[0], normalized)
            for p in found:
                self.register_path(p, normalized)
            return None, (
                f"I found multiple copies of {normalized}. "
                f"Using the most recent: {found[0]}. "
                f"Other locations: {', '.join(found[1:3])}"
            )

        return None, f"I couldn't find {normalized} on your computer."

    def ensure_indexed(self, full_path: str) -> tuple[bool, str]:
        """Ingest PDF if missing or stale. Returns (success, message)."""
        from app.rag.ingest import ingest_pdf

        path = Path(full_path)
        if not path.exists():
            return False, f"PDF not found: {full_path}"

        if self.is_indexed(str(path)):
            return True, "Already indexed"

        try:
            ingest_pdf(str(path))
            self.mark_indexed(str(path))
            return True, f"Indexed {path.name}"
        except Exception as exc:
            logger.exception("Failed to index PDF: %s", full_path)
            return False, f"Failed to index PDF: {exc}"


# Singleton
_manager: Optional[DocumentManager] = None


def get_document_manager() -> DocumentManager:
    global _manager
    if _manager is None:
        _manager = DocumentManager()
    return _manager
