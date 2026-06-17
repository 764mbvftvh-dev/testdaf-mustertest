from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from scoring_platform.config import GRADING_RESULTS_DIR

SPEAKING_TDN_OPTIONS = [
    ("5", "TDN 5"),
    ("4", "TDN 4"),
    ("3", "TDN 3"),
    ("0", "U3"),
    ("", "—"),
]

TASK_RATINGS = [
    ("sehr gut", "sehr gut"),
    ("gut", "gut"),
    ("befriedigend", "befriedigend"),
    ("ausreichend", "ausreichend"),
    ("mangelhaft", "mangelhaft"),
    ("", "—"),
]

def _speaking_path(student_id: str) -> Path:
    d = GRADING_RESULTS_DIR / "speaking"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{student_id}.json"

def get_speaking(student_id: str) -> dict:
    """返回口语评分数据，如无则返回默认空结构"""
    fp = _speaking_path(student_id)
    if fp.exists():
        try:
            return json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "student_id": student_id,
        "overall_tdn": "",
        "overall_label": "",
        "tasks": {},
        "updated_at": "",
    }

def save_speaking(
    student_id: str,
    student_name: str,
    overall_tdn: str,
    task_scores: dict[str, str],
) -> dict:
    tdn_map = {"5": "TDN 5", "4": "TDN 4", "3": "TDN 3", "0": "U3",
               "": "", None: ""}
    label = tdn_map.get(overall_tdn, overall_tdn)

    data = {
        "student_id": student_id,
        "student_name": student_name,
        "overall_tdn": int(overall_tdn) if overall_tdn and overall_tdn.isdigit() else 0,
        "overall_label": label,
        "tasks": task_scores,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    fp = _speaking_path(student_id)
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data

def list_all_speaking() -> dict[str, dict]:
    """返回 {student_id: speaking_data} 映射"""
    result = {}
    sd = GRADING_RESULTS_DIR / "speaking"
    if not sd.exists():
        return result
    for f in sd.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            sid = data.get("student_id", "")
            if sid:
                result[sid] = data
        except Exception:
            pass
    return result

def speaking_for_render(student_id: str) -> dict:
    """供模板渲染用，保证所有字段非空"""
    s = get_speaking(student_id)
    tasks = s.get("tasks", {}) or {}
    for i in range(1, 8):
        key = f"aufgabe_{i}"
        if key not in tasks:
            tasks[key] = ""
    return {
        "overall_tdn": str(s.get("overall_tdn", "") or ""),
        "overall_label": s.get("overall_label", "") or "",
        "tasks": tasks,
        "updated_at": s.get("updated_at", ""),
    }
