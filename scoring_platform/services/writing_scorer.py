from __future__ import annotations

import json
import re
from pathlib import Path

from testdaf_platform.config import CONFIG_FILE, QWEN_TEXT_MODEL, DASHSCOPE_BASE_URL
from testdaf_platform.services.text_generation import TextGenerationClient
from scoring_platform.config import DIMENSION_LABELS


def _load_api_key() -> str:
    """Read API key from the shared config file."""
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f).get("api_key", "")
        except Exception:
            return ""
    return ""


def _extract_student_text(attempt_meta: dict, answers: dict | list) -> str:
    if isinstance(answers, dict):
        for v in answers.values():
            if isinstance(v, str) and len(v) > 50:
                return v
    if isinstance(answers, list):
        for v in answers:
            if isinstance(v, str) and len(v) > 50:
                return v
    return ""


def _extract_writing_prompt(question_id: str) -> str:
    from scoring_platform.config import QUESTION_BANK_DIR
    from shared.file_io.atomic_json import read_json

    for path in QUESTION_BANK_DIR.rglob(question_id):
        if path.is_dir() and ".trash" not in path.parts and (path / "manifest.json").exists():
            manifest = read_json(path / "manifest.json")
            prompts_asset = manifest.get("assets", {}).get("prompt")
            if prompts_asset and (path / prompts_asset).exists():
                prompt_data = read_json(path / prompts_asset)
                if isinstance(prompt_data, str):
                    return prompt_data
                if isinstance(prompt_data, dict):
                    return prompt_data.get("prompt", str(prompt_data))
                if isinstance(prompt_data, list):
                    return "\n".join(str(p) for p in prompt_data)
            return manifest.get("title", "")
    return ""


def score_writing(attempt_meta: dict, answers: dict | list) -> dict | None:
    api_key = _load_api_key()
    if not api_key:
        return {
            "error": "未配置 API Key，无法进行写作评分。请在出题系统中设置。",
            "tdn": 0,
            "tdn_label": "—",
            "dimensionen": {},
            "kommentar": "",
        }

    student_text = _extract_student_text(attempt_meta, answers)
    if not student_text or len(student_text) < 100:
        return {
            "error": "学生作文不足 100 字符，无法评分。",
            "tdn": 0,
            "tdn_label": "—",
            "dimensionen": {},
            "kommentar": "",
        }

    question_id = attempt_meta.get("question_id", "")
    prompt_info = _extract_writing_prompt(question_id)

    dim_keys = ["gesamteindruck", "aufgabenbezug", "textaufbau", "satzstrukturen", "wortschatz"]
    dim_list = "\n".join(f"- {DIMENSION_LABELS[k]}" for k in dim_keys)

    system_prompt = (
        "你是 TestDaF / 德语 C1 写作评分专家。请根据德福官方评分标准，对以下学生作文打分。\n"
        "每个维度按 1（优秀）到 5（不及格）打分。\n"
        "请严格输出如下 JSON（不要 markdown 代码块）：\n"
        "{\n"
        '  "gesamteindruck": 2,\n'
        '  "aufgabenbezug": 2,\n'
        '  "textaufbau": 3,\n'
        '  "satzstrukturen": 3,\n'
        '  "wortschatz": 2,\n'
        '  "tdn": 4,\n'
        '  "tdn_label": "TDN 4",\n'
        '  "kommentar": "请用德语写一段 80-150 词的评语，说明优点和不足。"\n'
        "}\n"
        "评语必须用德语撰写。\n"
        "维度评分参考：\n"
        "1=非常优秀 2=较好 3=一般 4=较弱 5=完全不足\n"
    )

    user_prompt = (
        f"作文题目要求：\n{prompt_info}\n\n"
        f"学生作文正文：\n{student_text}\n\n"
        f"请对以下 {len(dim_keys)} 个维度分别打分 (1-5)：\n{dim_list}"
    )

    client = TextGenerationClient(model=QWEN_TEXT_MODEL, base_url=DASHSCOPE_BASE_URL)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        raw = client.generate_text(api_key=api_key, messages=messages, max_tokens=1500)
    except Exception as exc:
        return {
            "error": f"LLM 调用失败: {exc}",
            "tdn": 0,
            "tdn_label": "—",
            "dimensionen": {},
            "kommentar": "",
        }

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            result, _ = json.JSONDecoder().raw_decode(cleaned)
            parsed = result
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                except json.JSONDecodeError:
                    parsed = {}
            else:
                parsed = {}

    dimensionen = {}
    for k in dim_keys:
        val = int(parsed.get(k, 3))
        dimensionen[k] = max(1, min(5, val))

    tdn = int(parsed.get("tdn", 0))
    tdn_label = parsed.get("tdn_label", "—")
    kommentar = parsed.get("kommentar", "")

    return {
        "tdn": tdn,
        "tdn_label": tdn_label,
        "dimensionen": dimensionen,
        "kommentar": kommentar,
    }
