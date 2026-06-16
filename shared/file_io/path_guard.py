"""Path safety helpers shared by file-based systems."""

from __future__ import annotations

from pathlib import Path


def resolve_inside(base: Path, relative_path: str, error_message: str = "路径非法") -> Path:
    if not relative_path:
        raise RuntimeError(error_message)
    base_path = base.resolve()
    candidate = (base / relative_path).resolve()
    try:
        candidate.relative_to(base_path)
    except ValueError as exc:
        raise RuntimeError(error_message) from exc
    return candidate
