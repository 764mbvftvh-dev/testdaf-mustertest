from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STUDENTS_DIR = PROJECT_ROOT / "students"
QUESTION_BANK_DIR = PROJECT_ROOT / "question_bank"
STUDENT_ATTEMPTS_DIR = PROJECT_ROOT / "student_attempts"
GRADING_RESULTS_DIR = PROJECT_ROOT / "grading_results"

SESSION_COOKIE = "student_session"

READING_TDN = {
    (24, 30): (5, "TDN 5"),
    (20, 23): (4, "TDN 4"),
    (14, 19): (3, "TDN 3"),
    (0, 13):   (0, "U3"),
}

LISTENING_TDN = {
    (19, 25): (5, "TDN 5"),
    (15, 18): (4, "TDN 4"),
    (10, 14): (3, "TDN 3"),
    (0, 9):    (0, "U3"),
}

DIMENSION_LABELS = {
    "gesamteindruck": "整体印象 Gesamteindruck",
    "aufgabenbezug": "内容完成 Aufgabenbezug",
    "textaufbau": "篇章结构 Textaufbau",
    "satzstrukturen": "句型多样 Satzstrukturen",
    "wortschatz": "词汇丰富 Wortschatz",
}

DIMENSION_DESCRIPTIONS = {
    "gesamteindruck": {
        1: "流畅自然，一气呵成，毫无阅读障碍。",
        2: "绝大部分通顺，偶有生硬处但不影响整体。",
        3: "个别处需重读，但不影响整体把握。",
        4: "多处跳跃或矛盾，需反复阅读。",
        5: "大量断裂，思路混乱，几乎无法理解。",
    },
    "aufgabenbezug": {
        1: "所有要点充分论述，图表准确，论证有据。",
        2: "所有要点已覆盖，图表基本准确，论证较充分。",
        3: "个别要点缺失或论述偏浅，图表信息偶有遗漏。",
        4: "多个要点缺失，图表描述不准确，论证薄弱。",
        5: "严重偏离主题，大部分要点未涉及。",
    },
    "textaufbau": {
        1: "引论-过渡-结论层次分明，逻辑脉络清晰。",
        2: "结构完整，过渡稍显生硬，逻辑可循。",
        3: "结构基本可辨但缺少过渡，段落划分欠合理。",
        4: "结构混乱，缺少引论或结论，段落跳跃。",
        5: "无结构可言，全文堆砌，无段落逻辑。",
    },
    "satzstrukturen": {
        1: "主从复合句灵活搭配，句式变换丰富，连接多样。",
        2: "主从复合句为主，有一定变换，连接手段基本恰当。",
        3: "以简单句为主，偶有从句，连接词重复使用。",
        4: "几乎全是简单句，连接手段匮乏。",
        5: "仅主句堆砌，无从句，无连接手段。",
    },
    "wortschatz": {
        1: "词汇精准多样，学术词汇丰富，动词变换灵活。",
        2: "词汇基本恰当，有一定多样性，搭配基本正确。",
        3: "词汇基本够用但重复较多，学术表达有限。",
        4: "词汇贫乏，大量重复用词，多处搭配错误。",
        5: "词汇严重不足，大量用词错误，母语直译。",
    },
}

SECTION_LABELS = {
    "reading": ("📖", "阅读 Leseverstehen"),
    "listening": ("🎧", "听力 Hörverstehen"),
    "writing": ("✍️", "写作 Schriftlicher Ausdruck"),
}

TASK_LABELS = {
    "aufgabe_1": "Aufgabe 1",
    "aufgabe_2": "Aufgabe 2",
    "aufgabe_3": "Aufgabe 3",
}
