"""每笔 API 调用记录 JSONL 日志，用于统计 token / 音频用量。"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path


def _default_log_dir() -> Path:
    from testdaf_platform.config import PROJECT_ROOT

    return PROJECT_ROOT / "logs"


class ApiCallStats:
    """线程安全的 API 调用统计记录器。

    输出格式（JSONL）：每行一条 JSON 记录，写入 ``logs/api_calls.jsonl``。
    """

    def __init__(self, log_dir: Path | None = None) -> None:
        self.log_dir = log_dir or _default_log_dir()
        self._lock = threading.Lock()

    @property
    def log_path(self) -> Path:
        return self.log_dir / "api_calls.jsonl"

    def _ensure_dir(self) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def record_text(
        self,
        *,
        model: str,
        api_key: str = "",
        status: str = "ok",
        status_code: int | None = None,
        error_message: str = "",
        elapsed_seconds: float = 0,
    ) -> None:
        self._ensure_dir()
        entry = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "type": "text_generation",
            "model": model,
            "status": status,
            "status_code": status_code,
        }
        if error_message:
            entry["error"] = error_message[:200]
        if elapsed_seconds:
            entry["elapsed_s"] = round(elapsed_seconds, 2)
        self._write(entry)

    def record_tts(
        self,
        *,
        model: str,
        voice: str,
        text_len: int,
        status: str = "ok",
        status_code: int | None = None,
        error_message: str = "",
        elapsed_seconds: float = 0,
        audio_size_kb: float = 0,
    ) -> None:
        self._ensure_dir()
        entry = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "type": "tts",
            "model": model,
            "voice": voice,
            "text_len": text_len,
            "status": status,
            "status_code": status_code,
        }
        if error_message:
            entry["error"] = error_message[:200]
        if elapsed_seconds:
            entry["elapsed_s"] = round(elapsed_seconds, 2)
        if audio_size_kb:
            entry["audio_kb"] = round(audio_size_kb, 1)
        self._write(entry)

    def _write(self, entry: dict) -> None:
        line = json.dumps(entry, ensure_ascii=False) + "\n"
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(line)


_api_stats: ApiCallStats | None = None


def get_api_stats() -> ApiCallStats:
    global _api_stats
    if _api_stats is None:
        _api_stats = ApiCallStats()
    return _api_stats
