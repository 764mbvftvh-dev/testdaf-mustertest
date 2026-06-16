"""Atomic JSON read/write helpers shared by local systems."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4


def read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json_atomic(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()
