"""Shared generation utilities — JSON parsing, evidence reordering, helper builders."""

import json
import re


def parse_json(content: str, *, label: str = "JSON") -> dict:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            result, _ = json.JSONDecoder().raw_decode(cleaned)
            return result
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if not match:
                raise RuntimeError(f"无法从 API 响应中解析{label}")
            return json.loads(match.group(0))


def reorder_by_evidence(payload: dict, items_key: str, text_key: str, *, start_number: int) -> dict:
    items = payload.get(items_key, [])
    text = payload.get(text_key, "")
    if not items or not text:
        return payload

    anchored: list[tuple[int, dict]] = []
    unanchored: list[dict] = []
    for item in items:
        evidence = str(item.get("evidence", ""))
        pos = text.find(evidence) if evidence else -1
        if pos >= 0:
            anchored.append((pos, item))
        else:
            unanchored.append(item)

    anchored.sort(key=lambda entry: entry[0])
    reordered = [item for _, item in anchored] + unanchored
    for idx, item in enumerate(reordered):
        item["number"] = start_number + idx

    payload[items_key] = reordered
    return payload


def gendered_speakers_text(genders: dict[str, str], *, role_hint: str = "学生、教授、职员等") -> str:
    parts = []
    for sid, gender in genders.items():
        label = "女性" if gender == "female" else "男性"
        parts.append(f"说话人 {sid} 必须是{label}角色")
    return "；".join(parts) + f"。请自动决定合适的身份（如{role_hint}）。"


def build_two_voice_map(speaker_a_voice: str, speaker_b_voice: str) -> dict[str, str]:
    if speaker_a_voice != speaker_b_voice:
        return {"A": speaker_a_voice, "B": speaker_b_voice}
    fallback = "Ethan" if speaker_a_voice != "Ethan" else "Cherry"
    return {"A": speaker_a_voice, "B": fallback}
