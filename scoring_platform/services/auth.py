from __future__ import annotations

from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

from scoring_platform.config import STUDENTS_DIR, STUDENT_ATTEMPTS_DIR, GRADING_RESULTS_DIR
from shared.file_io.atomic_json import read_json


def resolve_student(token: str | None) -> dict | None:
    if not token:
        return None
    session_file = STUDENTS_DIR / "sessions" / f"{token}.json"
    if not session_file.exists():
        return None
    try:
        session = read_json(session_file)
    except Exception:
        return None
    expires_str = session.get("expires_at", "")
    try:
        expires = datetime.fromisoformat(expires_str)
        if datetime.now(timezone.utc) > expires:
            session_file.unlink(missing_ok=True)
            return None
    except ValueError:
        return None
    student_id = session.get("student_id", "")
    accounts = read_json(STUDENTS_DIR / "accounts.json") if (STUDENTS_DIR / "accounts.json").exists() else {}
    account = accounts.get(student_id)
    if not account:
        return None
    return {
        "student_id": student_id,
        "name": account.get("name", student_id),
        "role": account.get("role", "student"),
    }


def get_user(request) -> dict | None:
    import starlette.requests
    token = request.cookies.get("student_session")
    user = resolve_student(token)
    if user:
        return user
    host = request.client.host if request.client else "127.0.0.1"
    if host in ("127.0.0.1", "::1", "localhost"):
        return {"student_id": "_teacher", "name": "教师", "role": "teacher"}
    return None


def _load_accounts():
    return read_json(STUDENTS_DIR / "accounts.json") if (STUDENTS_DIR / "accounts.json").exists() else {}


def list_all_students() -> list[dict]:
    accounts = _load_accounts()
    return [
        {"student_id": sid, "name": a.get("name", sid), "role": a.get("role", "student")}
        for sid, a in accounts.items()
    ]
